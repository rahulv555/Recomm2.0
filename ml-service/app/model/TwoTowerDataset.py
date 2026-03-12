
from torch.utils.data import Dataset
import torch
import torch.nn as nn
import numpy as np


class TwoTowerDataset(Dataset):
    def __init__(self, conn):
        
        self.data = self._load(conn)

    def _load(self, conn):
        cur = conn.cursor()
        cur.execute("""
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
        """)

        rows = cur.fetchall()
        conn.commit()
        conn.close()
       
        return rows

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        r = self.data[idx]

        return {
            "user": {
                "height_norm": torch.tensor(r[2], dtype=torch.float32),
                "weight_norm": torch.tensor(r[3], dtype=torch.float32),
                "age_norm": torch.tensor(r[4], dtype=torch.float32),
                "budget_ord": torch.tensor(r[5], dtype=torch.float32),
                "drink_level_ord": torch.tensor(r[6], dtype=torch.float32),
                "is_smoker": torch.tensor(r[7], dtype=torch.float32),
                "bert_emb": np.array(r[8], dtype=np.float32),
                "cuisine_ids": r[9],

                "dress_preference_id": r[10],
                "ambience_id": r[11],
                "transport_id": r[12],
                "marital_status_id": r[13],
                "hijos_id": r[14],
                "interest_id": r[15],
                "personality_id": r[16],
                "religion_id": r[17],
                "activity_id": r[18],
            },
            "place": {
                "price_ord": torch.tensor(r[19], dtype=torch.float32),
                "alcohol_ord": torch.tensor(r[20], dtype=torch.float32),
                "is_open": torch.tensor(r[21], dtype=torch.float32),
                "rating_bayes": torch.tensor(r[22], dtype=torch.float32),
                "food_bayes": torch.tensor(r[23], dtype=torch.float32),
                "service_bayes": torch.tensor(r[24], dtype=torch.float32),
                "rating_min": torch.tensor(r[25], dtype=torch.float32),
                "food_min": torch.tensor(r[26], dtype=torch.float32),
                "service_min": torch.tensor(r[27], dtype=torch.float32),
                "rating_max": torch.tensor(r[28], dtype=torch.float32),
                "food_max": torch.tensor(r[29], dtype=torch.float32),
                "service_max": torch.tensor(r[30], dtype=torch.float32),
                "rating_count": torch.tensor(r[31], dtype=torch.float32),
                "food_count": torch.tensor(r[32], dtype=torch.float32),
                "service_count": torch.tensor(r[33], dtype=torch.float32),
                "bert_emb": np.array(r[34], dtype=np.float32),
                "cuisine_ids": r[35],

                "smoking_area_id": r[36],
                "rambience_id": r[37],
                "parking_lot_id": r[38],
            },
            "label": float(r[39])
        }
    

def collate_fn(batch):
    out = {"user": {}, "place": {}}

    # === USER TOWER PROCESSING ===
    # Groups: [height, weight, age]
    out["user"]["numeric_feats"] = torch.tensor([
        [b["user"]["height_norm"], b["user"]["weight_norm"], b["user"]["age_norm"]] 
        for b in batch
    ], dtype=torch.float32)

    # Groups: [budget, drink, smoker]
    out["user"]["ordinal_feats"] = torch.tensor([
        [b["user"]["budget_ord"], b["user"]["drink_level_ord"], b["user"]["is_smoker"]] 
        for b in batch
    ], dtype=torch.float32)

    out["user"]["bert_emb"] = torch.tensor(np.array([b["user"]["bert_emb"] for b in batch]))
    
    u_ids, u_mask = pad_cuisine([b["user"]["cuisine_ids"] for b in batch])
    out["user"]["cuisine_ids"] = u_ids
    out["user"]["cuisine_mask"] = u_mask

    for k in ["dress_preference_id", "ambience_id", "transport_id", "marital_status_id", 
              "hijos_id", "interest_id", "personality_id", "religion_id", "activity_id"]:
        out["user"][k] = torch.tensor([b["user"][k] for b in batch], dtype=torch.long)

    # === PLACE TOWER PROCESSING ===
    # Groups: [price, alcohol, open]
    out["place"]["ordinal_feats"] = torch.tensor([
        [b["place"]["price_ord"], b["place"]["alcohol_ord"], b["place"]["is_open"]] 
        for b in batch
    ], dtype=torch.float32)

    # Groups: [rating_bayes ... service_count] (12 features)
    out["place"]["numeric_feats"] = torch.tensor([
        [
            b["place"]["rating_bayes"], b["place"]["food_bayes"], b["place"]["service_bayes"],
            b["place"]["rating_min"], b["place"]["food_min"], b["place"]["service_min"],
            b["place"]["rating_max"], b["place"]["food_max"], b["place"]["service_max"],
            b["place"]["rating_count"], b["place"]["food_count"], b["place"]["service_count"]
        ] for b in batch
    ], dtype=torch.float32)

    out["place"]["bert_emb"] = torch.tensor(np.array([b["place"]["bert_emb"] for b in batch]))
    
    p_ids, p_mask = pad_cuisine([b["place"]["cuisine_ids"] for b in batch])
    out["place"]["cuisine_ids"] = p_ids
    out["place"]["cuisine_mask"] = p_mask

    for k in ["smoking_area_id", "rambience_id", "parking_lot_id"]:
        out["place"][k] = torch.tensor([b["place"][k] for b in batch], dtype=torch.long)

    out["label"] = torch.tensor([b["label"] for b in batch], dtype=torch.float32)
    return out



def pad_cuisine(batch_lists, pad_id=0):
    max_len = max(len(x) for x in batch_lists)

    ids = torch.zeros(len(batch_lists), max_len, dtype=torch.long)
    mask = torch.zeros(len(batch_lists), max_len, dtype=torch.float32)

    for i, seq in enumerate(batch_lists):
        if len(seq) == 0:
            continue
        ids[i, :len(seq)] = torch.tensor(seq, dtype=torch.long)
        mask[i, :len(seq)] = 1.0

    return ids, mask


class UserEmbeddingDataset(Dataset):
    def __init__(self, conn):
        cur = conn.cursor()
        # Get unique user profiles
        cur.execute("""
            SELECT userID, height_norm, weight_norm, age_norm, 
                   budget_ord, drink_level_ord, is_smoker, bert_embedding, 
                   cuisine_ids, dress_preference_id, ambience_id, transport_id, 
                   marital_status_id, hijos_id, interest_id, personality_id, 
                   religion_id, activity_id 
            FROM user_profiles
        """)
        self.data = cur.fetchall()
        cur.close()

    def __len__(self): return len(self.data)

    def __getitem__(self, idx):
        r = self.data[idx]
        return {
            "id": r[0],
            "features": {
                "height_norm": r[1], "weight_norm": r[2], "age_norm": r[3],
                "budget_ord": r[4], "drink_level_ord": r[5], "is_smoker": r[6],
                "bert_emb": np.array(r[7], dtype=np.float32),
                "cuisine_ids": r[8], "dress_preference_id": r[9],
                "ambience_id": r[10], "transport_id": r[11], "marital_status_id": r[12],
                "hijos_id": r[13], "interest_id": r[14], "personality_id": r[15],
                "religion_id": r[16], "activity_id": r[17]
            }
        }

class PlaceEmbeddingDataset(Dataset):
    def __init__(self, conn):
        cur = conn.cursor()
        # Get unique place profiles
        cur.execute("""
            SELECT placeID, price_ord, alcohol_ord, is_open,
                   rating_bayes, food_bayes, service_bayes,
                   rating_min, food_min, service_min,
                   rating_max, food_max, service_max,
                   rating_count, food_count, service_count,
                   bert_embedding, cuisine_ids, smoking_area_id,
                   rambience_id, parking_lot_id
            FROM places
        """)
        self.data = cur.fetchall()
        cur.close()

    def __len__(self): return len(self.data)

    def __getitem__(self, idx):
        r = self.data[idx]
        return {
            "id": r[0],
            "features": {
                "price_ord": r[1], "alcohol_ord": r[2], "is_open": r[3],
                "rating_bayes": r[4], "food_bayes": r[5], "service_bayes": r[6],
                "rating_min": r[7], "food_min": r[8], "service_min": r[9],
                "rating_max": r[10], "food_max": r[11], "service_max": r[12],
                "rating_count": r[13], "food_count": r[14], "service_count": r[15],
                "bert_emb": np.array(r[16], dtype=np.float32), "cuisine_ids": r[17],
                "smoking_area_id": r[18], "rambience_id": r[19], "parking_lot_id": r[20]
            }
        }
    

def user_collate_fn(batch):
    out = {"ids": [b["id"] for b in batch], "features": {}}
    feats = [b["features"] for b in batch]
    
    out["features"]["numeric_feats"] = torch.tensor([[f["height_norm"], f["weight_norm"], f["age_norm"]] for f in feats], dtype=torch.float32)
    out["features"]["ordinal_feats"] = torch.tensor([[f["budget_ord"], f["drink_level_ord"], f["is_smoker"]] for f in feats], dtype=torch.float32)
    out["features"]["bert_emb"] = torch.tensor(np.array([f["bert_emb"] for f in feats]))
    
    ids, mask = pad_cuisine([f["cuisine_ids"] for f in feats])
    out["features"]["cuisine_ids"], out["features"]["cuisine_mask"] = ids, mask

    for k in ["dress_preference_id", "ambience_id", "transport_id", "marital_status_id", "hijos_id", "interest_id", "personality_id", "religion_id", "activity_id"]:
        out["features"][k] = torch.tensor([f[k] for f in feats], dtype=torch.long)
    return out

def place_collate_fn(batch):
    out = {"ids": [b["id"] for b in batch], "features": {}}
    feats = [b["features"] for b in batch]

    out["features"]["ordinal_feats"] = torch.tensor([[f["price_ord"], f["alcohol_ord"], f["is_open"]] for f in feats], dtype=torch.float32)
    out["features"]["numeric_feats"] = torch.tensor([[f["rating_bayes"], f["food_bayes"], f["service_bayes"], f["rating_min"], f["food_min"], f["service_min"], f["rating_max"], f["food_max"], f["service_max"], f["rating_count"], f["food_count"], f["service_count"]] for f in feats], dtype=torch.float32)
    out["features"]["bert_emb"] = torch.tensor(np.array([f["bert_emb"] for f in feats]))
    
    ids, mask = pad_cuisine([f["cuisine_ids"] for f in feats])
    out["features"]["cuisine_ids"], out["features"]["cuisine_mask"] = ids, mask

    for k in ["smoking_area_id", "rambience_id", "parking_lot_id"]:
        out["features"][k] = torch.tensor([f[k] for f in feats], dtype=torch.long)
    return out