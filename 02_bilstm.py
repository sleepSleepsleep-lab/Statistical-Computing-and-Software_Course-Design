"""
02_bilstm.py
优化：加入 EarlyStopping，收敛/过拟合时自动停止，确保训练时间公平可比。
"""
import time
import pandas as pd
import jieba
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from collections import Counter
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

CONFIG = {
    "train_path": "/root/autodl-tmp/dataset/train-00000-of-00001-02f200ca5f2a7868.parquet",
    "dev_path": "/root/autodl-tmp/dataset/validation-00000-of-00001-405befbaa3bcf1a2.parquet",
    "test_path": "/root/autodl-tmp/dataset/test-00000-of-00001-5372924f059fe767.parquet",
    "log_file": "./02_bilstm_results.txt",
    "max_length": 128, "vocab_size": 15000, "embed_dim": 128, "hidden_dim": 128,
    "batch_size": 64, "max_epochs": 50, "lr": 1e-3, "early_stop_patience": 5,
    "device": "cuda" if torch.cuda.is_available() else "cpu"
}

class ChnSentiDataset(Dataset):
    def __init__(self, df, vocab, max_len):
        self.labels = torch.tensor(df['label'].values, dtype=torch.long)
        self.texts = torch.tensor([[vocab.get(w, 1) for w in list(jieba.cut(str(t)))][:max_len] + [0]*max(0, max_len-len(list(jieba.cut(str(t))))) for t in df['text']], dtype=torch.long)
    def __len__(self): return len(self.labels)
    def __getitem__(self, idx): return self.texts[idx], self.labels[idx]

class BiLSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(0.5) # 优化点：50% 的神经元随机失活
        self.fc = nn.Linear(hidden_dim * 2, 2)
    def forward(self, x):
        embedded = self.embedding(x)
        _, (hidden, _) = self.lstm(embedded)
        out = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        return self.fc(self.dropout(out)) # 在全连接层前使用 Dropout

class EarlyStopping:
    """早停机制：验证集 loss 连续 patience 轮不下降则停止"""
    def __init__(self, patience=5, min_delta=0.0):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = float("inf")
        self.early_stop = False
    def __call__(self, val_loss):
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
        return self.early_stop

if __name__ == "__main__":
    train_df, dev_df, test_df = pd.read_parquet(CONFIG["train_path"]), pd.read_parquet(CONFIG["dev_path"]), pd.read_parquet(CONFIG["test_path"])

    counter = Counter()
    for text in train_df['text']: counter.update(jieba.cut(str(text)))
    vocab = {w: i+2 for i, (w, _) in enumerate(counter.most_common(CONFIG["vocab_size"]))}
    vocab['<PAD>'], vocab['<UNK>'] = 0, 1

    train_loader = DataLoader(ChnSentiDataset(train_df, vocab, CONFIG["max_length"]), batch_size=CONFIG["batch_size"], shuffle=True)
    dev_loader = DataLoader(ChnSentiDataset(dev_df, vocab, CONFIG["max_length"]), batch_size=CONFIG["batch_size"])
    test_loader = DataLoader(ChnSentiDataset(test_df, vocab, CONFIG["max_length"]), batch_size=CONFIG["batch_size"])

    model = BiLSTMClassifier(len(vocab), CONFIG["embed_dim"], CONFIG["hidden_dim"]).to(CONFIG["device"])
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=CONFIG["lr"])

    best_val_acc = 0.0
    best_model_state = None
    early_stopper = EarlyStopping(patience=CONFIG["early_stop_patience"])
    
    t0 = time.time()
    for epoch in range(CONFIG["max_epochs"]):
        model.train()
        train_loss = 0.0
        for texts, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(texts.to(CONFIG["device"]))
            loss = criterion(outputs, labels.to(CONFIG["device"]))
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        model.eval()
        val_preds, val_labels = [], []
        val_loss = 0.0
        with torch.no_grad():
            for texts, labels in dev_loader:
                outputs = model(texts.to(CONFIG["device"]))
                val_loss += criterion(outputs, labels.to(CONFIG["device"])).item()
                val_preds.extend(torch.argmax(outputs, dim=1).cpu().numpy())
                val_labels.extend(labels.numpy())
        val_acc = accuracy_score(val_labels, val_preds)
        avg_val_loss = val_loss / len(dev_loader)
        print(f"Epoch {epoch+1:2d} | Train Loss: {train_loss/len(train_loader):.4f} | Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.4f}")
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
        
        if early_stopper(avg_val_loss):
            print(f"EarlyStopping triggered at epoch {epoch+1} (best val acc: {best_val_acc:.4f})")
            break
    actual_epochs = epoch + 1
    train_time = time.time() - t0

    model.load_state_dict(best_model_state)
    model.eval()
    test_preds, test_labels = [], []
    t1 = time.time()
    with torch.no_grad():
        for texts, labels in test_loader:
            test_preds.extend(torch.argmax(model(texts.to(CONFIG["device"])), dim=1).cpu().numpy())
            test_labels.extend(labels.numpy())
    test_time = time.time() - t1

    acc = accuracy_score(test_labels, test_preds)
    p, r, f1, _ = precision_recall_fscore_support(test_labels, test_preds, average='binary')
    log_text = (f"=== 02. Bi-LSTM (Best Val Acc: {best_val_acc:.4f}, Epochs: {actual_epochs}) ===\n"
                f"训练耗时: {train_time:.2f} s | 测试耗时: {test_time:.2f} s\n"
                f"Accuracy: {acc:.4f} | Precision: {p:.4f} | Recall: {r:.4f} | F1: {f1:.4f}\n\n")
    print(log_text)
    with open(CONFIG["log_file"], "a", encoding="utf-8") as f: f.write(log_text)