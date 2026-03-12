import torch
import torch.nn as nn
import torch.nn.functional as F

class UserTower(nn.Module):
    def __init__(
        self,
        numeric_dim,    
        ordinal_dim,
        cuisine_vocab_size,
        bert_dim,
        hidden_dim,

        # vocab sizes
        dress_vocab,
        ambience_vocab,
        transport_vocab,
        marital_vocab,
        hijos_vocab,
        interest_vocab,
        personality_vocab,
        religion_vocab,
        activity_vocab,
    ):
        super().__init__()

        # ===== Nominal embeddings =====
        self.dress_emb = nn.Embedding(dress_vocab, 8)
        self.ambience_emb = nn.Embedding(ambience_vocab, 8)
        self.transport_emb = nn.Embedding(transport_vocab, 8)
        self.marital_emb = nn.Embedding(marital_vocab, 4)
        self.hijos_emb = nn.Embedding(hijos_vocab, 4)
        self.interest_emb = nn.Embedding(interest_vocab, 8)
        self.personality_emb = nn.Embedding(personality_vocab, 8)
        self.religion_emb = nn.Embedding(religion_vocab, 4)
        self.activity_emb = nn.Embedding(activity_vocab, 8)

        # ===== Cuisine encoder =====
        self.cuisine_emb = nn.Embedding(cuisine_vocab_size, 32)

        # Calculate nominal dimension: (6 fields * 8) + (3 fields * 4) = 48 + 12 = 60
        nominal_dim = (8 * 6) + (4 * 3) 

        # Final calculated input dimension
        self.input_dim = numeric_dim + ordinal_dim + 32 + bert_dim + nominal_dim

        self.mlp = nn.Sequential(
            nn.Linear(self.input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def encode_cuisine(self, ids, mask):
        emb = self.cuisine_emb(ids)  # (B, L, D)
        emb = emb * mask.unsqueeze(-1)
        
        sum_emb = emb.sum(1)
        # Use a small epsilon to prevent division by zero
        mask_sum = mask.sum(1, keepdim=True)
        
        # Only divide where mask_sum > 0, otherwise return zeros
        mean_emb = torch.where(
            mask_sum > 0, 
            sum_emb / mask_sum.clamp(min=1e-9), 
            torch.zeros_like(sum_emb)
        )
        return mean_emb

    def forward(self, x):
        nom = torch.cat([
            self.dress_emb(x["dress_preference_id"]),
            self.ambience_emb(x["ambience_id"]),
            self.transport_emb(x["transport_id"]),
            self.marital_emb(x["marital_status_id"]),
            self.hijos_emb(x["hijos_id"]),
            self.interest_emb(x["interest_id"]),
            self.personality_emb(x["personality_id"]),
            self.religion_emb(x["religion_id"]),
            self.activity_emb(x["activity_id"]),
        ], dim=1)

        cuisine_vec = self.encode_cuisine(
            x["cuisine_ids"], x["cuisine_mask"]
        )

        feats = torch.cat([
            x["numeric_feats"],
            x["ordinal_feats"],
            cuisine_vec,
            x["bert_emb"],
            nom
        ], dim=1)

        # print(f"Feats : {feats}")

        for tensor in feats:
            if torch.isnan(tensor).any():
                # Find the exact row and column
                nan_ind = torch.isnan(tensor).nonzero(as_tuple=True)
                print(f"\n❌ NAN DETECTED in UserTower feature: '{nan_ind}'")
                # print(f"Row indices: {nan_rows[:5].tolist()}") # show first 5
                # print(f"Column indices: {nan_cols[:5].tolist()}")
                
                # If it's numeric/ordinal, we can check the raw values
                # if name in ["numeric_feats", "ordinal_feats"]:
                #     print(f"Raw data sample at error: {tensor[nan_rows[0]]}")
                
                # # Stop the training to prevent weight corruption
                # raise ValueError(f"NaN found in {name}")
        
        final = F.normalize(self.mlp(feats), dim=1)



        # print(f"Final : {final}")
        return final
    


class PlaceTower(nn.Module):
    def __init__(
        self,
        numeric_dim,
        ordinal_dim,
        cuisine_vocab_size,
        bert_dim,
        hidden_dim,
        smoking_vocab,
        rambience_vocab,
        parking_vocab
    ):
        super().__init__()

        self.smoking_emb = nn.Embedding(smoking_vocab, 4)
        self.rambience_emb = nn.Embedding(rambience_vocab, 8)
        self.parking_emb = nn.Embedding(parking_vocab, 4)

        self.cuisine_emb = nn.Embedding(cuisine_vocab_size, 32)

        # 4 (smoking) + 8 (ambience) + 4 (parking) = 16
        nominal_dim = 16

        self.input_dim = numeric_dim + ordinal_dim + 32 + bert_dim + nominal_dim

        self.mlp = nn.Sequential(
            nn.Linear(self.input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def encode_cuisine(self, ids, mask):
        emb = self.cuisine_emb(ids)  # (B, L, D)
        emb = emb * mask.unsqueeze(-1)
        
        sum_emb = emb.sum(1)
        # Use a small epsilon to prevent division by zero
        mask_sum = mask.sum(1, keepdim=True)
        
        # Only divide where mask_sum > 0, otherwise return zeros
        mean_emb = torch.where(
            mask_sum > 0, 
            sum_emb / mask_sum.clamp(min=1e-9), 
            torch.zeros_like(sum_emb)
        )
        return mean_emb

    def forward(self, x):
        nom = torch.cat([
            self.smoking_emb(x["smoking_area_id"]),
            self.rambience_emb(x["rambience_id"]),
            self.parking_emb(x["parking_lot_id"]),
        ], dim=1)

        cuisine_vec = self.encode_cuisine(
            x["cuisine_ids"], x["cuisine_mask"]
        )

        feats = torch.cat([
            x["numeric_feats"],
            x["ordinal_feats"],
            cuisine_vec,
            x["bert_emb"],
            nom
        ], dim=1)

        # print(f"Feats : {feats}")


        final = F.normalize(self.mlp(feats), dim=1)
        # print(f"Final : {final}")
        return final
    

class TwoTowerModel(nn.Module):
    def __init__(self, user_tower, place_tower):
        super().__init__()
        self.user_tower = user_tower
        self.place_tower = place_tower

    def forward(self, user_batch, place_batch):
        user_emb = self.user_tower(user_batch)
        place_emb = self.place_tower(place_batch)
        # STRICT CHECK
        if torch.isnan(user_emb).any():
            # Find exactly which index is bad
            bad_idx = torch.isnan(user_emb).any(dim=1).nonzero()
            print(f"CRITICAL: User Embedding has NaN at indices: {bad_idx}")
            # Check the raw input for those indices
            print(f"Sample raw input for bad index: {user_batch['numeric_feats'][bad_idx[0]]}")
            
        if torch.isnan(place_emb).any():
            print(f"CRITICAL: Place Embedding has NaN!")
        return user_emb, place_emb