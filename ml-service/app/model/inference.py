import joblib
from sentence_transformers import SentenceTransformer
from functools import partialmethod
from transformers import logging as transformers_logging
from tqdm import tqdm
import torch
import numpy as np
import pandas as pd
from app.dbquery import execute_db_query
import app.redisutils.redis_utils as rd
from app.model.TwoTowerDataset import collate_fn, pad_cuisine
from app.model.bert_embedding import build_user_text_groups
from .contrastive_loss import ContrastiveLoss
from .model import TwoTowerModel, UserTower, PlaceTower

class Recommender:
    def __init__(self, model_path, encoder_dir, scalers_dir):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = model_path
        #Load the Two-Tower Model
        tower_checkpoint = torch.load(f"{model_path}/twotower/twotower_model.pt")
        config = tower_checkpoint["config"]
        self.checkpoint = torch.load(f"{model_path}/twotower/best_checkpoint_with_val.pt", map_location=self.device)
        user_tower = UserTower(**config["user_tower"]).to(self.device)
        place_tower = PlaceTower(**config["place_tower"]).to(self.device)
        self.model = TwoTowerModel(user_tower, place_tower).to(self.device)
        self.model.load_state_dict(self.checkpoint['model'])
        self.model.eval()

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-5)
        if 'optimizer' in self.checkpoint:
            self.optimizer.load_state_dict(self.checkpoint['optimizer'])

        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=5)
        self.scheduler.load_state_dict(self.checkpoint["scheduler"])

        # Load Encoders, Maps, Scalers
        self.dress_preference_le = joblib.load(f"{encoder_dir}/dress_preference_le.joblib")
        self.userambience_le = joblib.load(f"{encoder_dir}/userambience_le.joblib")
        self.transport_le = joblib.load(f"{encoder_dir}/transport_le.joblib")
        self.marital_le = joblib.load(f"{encoder_dir}/marital_le.joblib")
        self.hijos_le = joblib.load(f"{encoder_dir}/hijos_le.joblib")
        self.interest_le = joblib.load(f"{encoder_dir}/interest_le.joblib")
        self.personality_le = joblib.load(f"{encoder_dir}/personality_le.joblib")
        self.religion_le = joblib.load(f"{encoder_dir}/religion_le.joblib")
        self.activity_le = joblib.load(f"{encoder_dir}/activity_le.joblib")
        self.usercuisine_le = joblib.load(f"{encoder_dir}/usercuisine_le.joblib")

        self.heightscaler = joblib.load(f"{scalers_dir}/height_scaler.joblib")
        self.weightscaler = joblib.load(f"{scalers_dir}/weight_scaler.joblib")
        self.agescaler = joblib.load(f"{scalers_dir}/age_scaler.joblib")

        #Maps for ordinal vars
        self.drinklevel_map = {
            'abstemious': 0,
            'social drinker': 1,
            'casual drinker': 2
        }
        self.budget_map = {
            'low': 0,
            'medium': 1,
            'high': 2
        }

        # USAGE
        # userprofile_data['drink_level_ord'] = userprofile_data['drink_level'].map(drinklevel_map)
        # userprofile_data['drink_level_ord'] = userprofile_data['drink_level_ord'] / 3

        #BOOLEAN COLUMN USAGE 
        # userprofile_data['is_smoker'] = (userprofile_data['smoker'] == 'true').astype(int)


                
        # Load BERT (SentenceTransformer is the easiest way to get the embedding)
        transformers_logging.set_verbosity_error()
        tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)
        self.bert_model = SentenceTransformer(f'{model_path}/all-MiniLM-L6-v2')

    def reload_weights(self, checkpoint_path: str = None):
        """Reload model weights (and optimizer/scheduler) from disk.

        This allows you to refresh a running Recommender instance without
        recreating it (e.g., after incremental retraining has saved a new
        checkpoint).
        """
        path = checkpoint_path or f"{self.model_path}/twotower/best_checkpoint_runtime.pt"
        self.checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(self.checkpoint['model'])
        self.model.eval()

        if 'optimizer' in self.checkpoint:
            self.optimizer.load_state_dict(self.checkpoint['optimizer'])

        if 'scheduler' in self.checkpoint:
            self.scheduler.load_state_dict(self.checkpoint['scheduler'])


    def retrain_on_new_interactions(self):
        self.reload_weights()
        new_data_query = """
            SELECT
                u.userID,
                p.placeID,
                u.height_norm, u.weight_norm, u.age_norm,
                u.budget_ord, u.drink_level_ord, u.is_smoker,
                u.bert_embedding,
                u.cuisine_ids,
                u.dress_preference_id,
                u.ambience_id,
                u.transport_id,
                u.marital_status_id,
                u.hijos_id,
                u.interest_id,
                u.personality_id,
                u.religion_id,
                u.activity_id,

                p.price_ord, p.alcohol_ord, p.is_open,
                p.rating_bayes, p.food_bayes, p.service_bayes,
                p.rating_min, p.food_min, p.service_min,
                p.rating_max, p.food_max, p.service_max,
                p.rating_count, p.food_count, p.service_count,
                p.bert_embedding,
                p.cuisine_ids,
                p.smoking_area_id,
                p.rambience_id,
                p.parking_lot_id,

                i.rating
            FROM interactions i
            JOIN user_profiles u ON i.userID = u.userID
            JOIN places p ON i.placeID = p.placeID
            WHERE i.trained = FALSE
        """

        # Execute this query and Create a dataset with just these rows

        rows = execute_db_query(new_data_query)
        if not rows or len(rows) < 2:
            print("Not enough new interactions to form a contrastive batch.")
            return  
        # Mimicing __get__item__
        batch_data = []
        for r in rows:
            item = {
                "user": {
                    "height_norm": r[2], "weight_norm": r[3], "age_norm": r[4],
                    "budget_ord": r[5], "drink_level_ord": r[6], "is_smoker": r[7],
                    "bert_emb": np.array(r[8], dtype=np.float32),
                    "cuisine_ids": r[9],
                    "dress_preference_id": r[10], "ambience_id": r[11],
                    "transport_id": r[12], "marital_status_id": r[13],
                    "hijos_id": r[14], "interest_id": r[15],
                    "personality_id": r[16], "religion_id": r[17], "activity_id": r[18],
                },
                "place": {
                    "price_ord": r[19], "alcohol_ord": r[20], "is_open": r[21],
                    "rating_bayes": r[22], "food_bayes": r[23], "service_bayes": r[24],
                    "rating_min": r[25], "food_min": r[26], "service_min": r[27],
                    "rating_max": r[28], "food_max": r[29], "service_max": r[30],
                    "rating_count": r[31], "food_count": r[32], "service_count": r[33],
                    "bert_emb": np.array(r[34], dtype=np.float32),
                    "cuisine_ids": r[35],
                    "smoking_area_id": r[36], "rambience_id": r[37], "parking_lot_id": r[38],
                },
                "label": float(r[39])
            }
            batch_data.append(item)

        #collate
        batch = collate_fn(batch_data)
        user_input = {k: v.to(self.device) for k, v in batch["user"].items()}
        place_input = {k: v.to(self.device) for k, v in batch["place"].items()}
        labels = batch["label"].to(self.device)

        criterion = ContrastiveLoss(temperature=0.1)

        self.model.train()
        epochs = 3
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            user_emb, place_emb = self.model(user_input, place_input)
            loss = criterion(user_emb, place_emb, labels)
            
            loss.backward()
            self.optimizer.step()
            print(f"Incremental Epoch {epoch+1}/3 - Loss: {loss.item():.4f}")

        # 5. Save the state_dict back to the checkpoint
        torch.save({
            "model": self.model.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "scheduler" : self.scheduler.state_dict()
        }, f"{self.model_path}/twotower/best_checkpoint_runtime.pt")
        
        self.model.eval()
        print("Retraining successful. Model saved.")

        # self.checkpoint = torch.load(f"{self.model_path}/twotower/best_checkpoint_runtime.pt", map_location=self.device)
        # self.model.load_state_dict(self.checkpoint['model'])
        # self.model.eval()

        # self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-5)
        # if 'optimizer' in self.checkpoint:
        #     self.optimizer.load_state_dict(self.checkpoint['optimizer'])

        # self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=5)
        # self.scheduler.load_state_dict(self.checkpoint["scheduler"])


        #Set trained true in DB
        execute_db_query("UPDATE interactions SET trained = TRUE WHERE trained = FALSE")

        rd.sync_untrained_count()


    def _prepare_model_input(self, df):
        try:
            self.reload_weights()

            # Handle Numeric Scaling
            height_norm = self.heightscaler.transform(df[['height']])[0][0]
            weight_norm = self.weightscaler.transform(df[['weight']])[0][0]
            age_norm = self.agescaler.transform(df[['age']])[0][0]

            # Handle Ordinal Mapping
            budget_ord = self.budget_map.get(df['budget'].iloc[0], 0)
            drink_ord = self.drinklevel_map.get(df['drink_level'].iloc[0], 0)
            budget_ord = budget_ord/3.0
            drink_ord = drink_ord/3.0

            is_smoker = 1.0 if df['smoker'].iloc[0].lower() == 'true' else 0.0

            #BERT Embedding
            lifestyle, social, preference, cuisine = build_user_text_groups(df.iloc[0])
            print(lifestyle)
            print(social)
            print(preference)
            print(cuisine)

            lifestyle_e = self.bert_model.encode(lifestyle, normalize_embeddings=True)
            social_e = self.bert_model.encode(social, normalize_embeddings=True)
            preference_e = self.bert_model.encode(preference, normalize_embeddings=True)
            cuisine_e = self.bert_model.encode(cuisine, normalize_embeddings=True)

            bert_emb = np.concatenate(
                [lifestyle_e, social_e, preference_e, cuisine_e]
            )  # shape: (1536,)

            # Handle Cuisines
            raw_cuisines = df['rcuisine'].iloc[0] # list of strings
            print(f"raw_cuisines : {raw_cuisines}")
            cuisine_ids = [self.usercuisine_le.transform([c])[0] for c in raw_cuisines]
            ids_tensor, mask_tensor = pad_cuisine([cuisine_ids]) # Use your existing function


            nominals = {
                "dress_preference_id": self.dress_preference_le.transform([df["dress_preference"].iloc[0]])[0],
                "ambience_id": self.userambience_le.transform([df["ambience"].iloc[0]])[0],
                "transport_id": self.transport_le.transform([df["transport"].iloc[0]])[0],
                "marital_status_id": self.marital_le.transform([df["marital_status"].iloc[0]])[0],
                "hijos_id": self.hijos_le.transform([df["hijos"].iloc[0]])[0],
                "interest_id": self.interest_le.transform([df["interest"].iloc[0]])[0],
                "personality_id": self.personality_le.transform([df["personality"].iloc[0]])[0],
                "religion_id": self.religion_le.transform([df["religion"].iloc[0]])[0],
                "activity_id": self.activity_le.transform([df["activity"].iloc[0]])[0],
            }
        

            # Handle Nominal (Label Encoders)

            # Construct the batch matching your collate_fn logic
            user_batch = {
                "numeric_feats": torch.tensor([[height_norm, weight_norm, age_norm]], dtype=torch.float32),
                "ordinal_feats": torch.tensor([[budget_ord, drink_ord, is_smoker]], dtype=torch.float32),
                "bert_emb": torch.tensor([bert_emb], dtype=torch.float32),
                "cuisine_ids": ids_tensor.to(self.device),
                "cuisine_mask": mask_tensor.to(self.device),
                "dress_preference_id": torch.tensor([nominals["dress_preference_id"]], dtype=torch.long),
                "ambience_id": torch.tensor([nominals["ambience_id"]], dtype=torch.long),
                "transport_id": torch.tensor([nominals["transport_id"]], dtype=torch.long),
                "marital_status_id": torch.tensor([nominals["marital_status_id"]], dtype=torch.long),
                "hijos_id": torch.tensor([nominals["hijos_id"]], dtype=torch.long),
                "interest_id": torch.tensor([nominals["interest_id"]], dtype=torch.long),
                "personality_id": torch.tensor([nominals["personality_id"]], dtype=torch.long),
                "religion_id": torch.tensor([nominals["religion_id"]], dtype=torch.long),
                "activity_id": torch.tensor([nominals["activity_id"]], dtype=torch.long),
            }
            
            # Also return the processed values to update the DB
            processed_values = {
                "height_norm": float(height_norm), "weight_norm": float(weight_norm), "age_norm": float(age_norm),
                "budget_ord": float(budget_ord), "drink_level_ord": float(drink_ord), "is_smoker": float(is_smoker),
                "bert_embedding": bert_emb.tolist(), "cuisine_ids": cuisine_ids,
                **nominals
            }
            
            return user_batch, processed_values
        except Exception as e:
            print(f"Failed at _prepare_model_inputg : {e}")
        
        
    def update_single_user_embedding(self, user_id: str):
        # Pull raw data from Postgres
        try:
            cols = [
                "userID", "smoker", "drink_level", "budget", 
                "dress_preference", "ambience", "transport", 
                "marital_status", "hijos", "age",
                "interest", "personality", "religion", "activity","weight","height","rcuisine"
            ]

            query = f"SELECT {', '.join(cols)} FROM user_profiles WHERE userID = '{user_id}'"
            raw_data = execute_db_query(query) # Returns list of tuples
            
            if not raw_data:
                return None

            df = pd.DataFrame(raw_data, columns=cols) 

            # user_batch for training, processed for storing in DB
            user_batch, processed = self._prepare_model_input(df)

            # 3. Run through UserTower (Inference)
            with torch.no_grad():
                user_vector = self.model.user_tower({k: v.to(self.device) for k, v in user_batch.items()})
                nn_vector = user_vector.cpu().numpy().flatten().astype(np.float32).tolist()
                # Convert to numpy and flatten

            # Update Database and Redis
            # Update Postgres so the vector is persistent


            update_cols = ["cuisine_ids","drink_level_ord","budget_ord","is_smoker","dress_preference_id",
                            "ambience_id","transport_id","marital_status_id","hijos_id","interest_id","personality_id",
                            "religion_id","activity_id","height_norm","weight_norm","age_norm","bert_embedding","nn_embedding"              
            ]

            all_updates = {**processed, "nn_embedding": nn_vector}

            clean_updates = {}
            for k, v in all_updates.items():
                if hasattr(v, 'item'): # Catches numpy scalars (int64, float32)
                    clean_updates[k] = v.item()
                elif isinstance(v, np.ndarray): # Catches numpy arrays (embeddings)
                    clean_updates[k] = v.tolist()
                elif isinstance(v, list):
                    clean_updates[k] = [x.item() if hasattr(x, 'item') else x for x in v]
                else:
                    clean_updates[k] = v

            set_clause = ", ".join([f"{k} = %s" for k in clean_updates.keys()])
            values = list(clean_updates.values()) + [user_id]
            
            execute_db_query(
                f"UPDATE user_profiles SET {set_clause} WHERE userID = %s", 
                tuple(values)
            )

            # Update Redis JSON 
            rd.store_user_embedding(user_id, np.array(nn_vector, dtype=np.float32))

            print("User embedding updated")

            return nn_vector
        except Exception as e:
            print(f"Failed at update_single_user_embedding : {e}")