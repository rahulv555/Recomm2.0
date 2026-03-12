# def contrastive_loss(user_emb, place_emb, temperature=0.07):
#     logits = user_emb @ place_emb.T / temperature
#     labels = torch.arange(len(user_emb), device=user_emb.device)
#     return nn.CrossEntropyLoss()(logits, labels)
import torch
import torch.nn as nn
import torch.nn.functional as F

class ContrastiveLoss(nn.Module): 
    def __init__(self, temperature=0.07):
        super().__init__()
        self.temperature = temperature
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, user_embeddings, place_embeddings, labels=None):
        """
        user_embeddings: (Batch, Hidden)
        place_embeddings: (Batch, Hidden)
        labels: Optional weights (if 0, interaction didn't happen)
        """
        # Calculate Cosine Similarity Matrix (B, B)
        # Since embeddings are F.normalized, matmul is equivalent to cosine similarity
        logits = torch.matmul(user_embeddings, place_embeddings.T) / self.temperature # similiarity matrix
        # Prevent exploding logits
        # logits = torch.clamp(logits, -50, 50)

        # The diagonal represents the true pairs (positives)
        batch_size = user_embeddings.size(0)
        targets = torch.arange(batch_size, device=user_embeddings.device)
        
        # If you have explicit labels (e.g., 0 or 1), you can mask the loss
        if labels is not None:
            # Only calculate loss for high-rating or positive interactions
            pos_mask = labels > 0 
            if pos_mask.sum() == 0:
                return torch.tensor(0.0, requires_grad=True, device=user_embeddings.device)
            logits_u2p = logits[pos_mask]
            logits_p2u = logits.T[pos_mask]

            targets = targets[pos_mask]

            loss_u2p = self.criterion(logits_u2p, targets)
            loss_p2u = self.criterion(logits_p2u, targets)
        else:
            loss_u2p = self.criterion(logits, targets)
            loss_p2u = self.criterion(logits.T, targets)

        loss = (loss_u2p + loss_p2u) / 2

        return loss