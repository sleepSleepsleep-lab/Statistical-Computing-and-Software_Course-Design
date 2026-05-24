"""
01_svm.py
SVM 中文情感分析基线模型
"""
import time
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

CONFIG = {
    "train_path": "./dataset/train-00000-of-00001-02f200ca5f2a7868.parquet",
    "dev_path": "./dataset/validation-00000-of-00001-405befbaa3bcf1a2.parquet",
    "test_path": "./dataset/test-00000-of-00001-5372924f059fe767.parquet",
    "log_file": "./01_svm_results.txt"
}

def load_and_cut(path):
    df = pd.read_parquet(path)
    df['cut_text'] = df['text'].apply(lambda x: " ".join(jieba.cut(str(x))))
    return df

if __name__ == "__main__":
    print("加载数据与分词中...")
    train_df = load_and_cut(CONFIG["train_path"])
    dev_df = load_and_cut(CONFIG["dev_path"])
    test_df = load_and_cut(CONFIG["test_path"])
    full_train_df = pd.concat([train_df, dev_df], ignore_index=True)

    print("训练 SVM 中...")
    t0 = time.time()
    tfidf = TfidfVectorizer(max_features=10000)
    X_train = tfidf.fit_transform(full_train_df['cut_text'])
    model = LinearSVC(C=1.0, max_iter=2000)
    model.fit(X_train, full_train_df['label'])
    train_time = time.time() - t0

    print("测试 SVM 中...")
    t1 = time.time()
    y_pred = model.predict(tfidf.transform(test_df['cut_text']))
    test_time = time.time() - t1

    acc = accuracy_score(test_df['label'], y_pred)
    p, r, f1, _ = precision_recall_fscore_support(test_df['label'], y_pred, average='binary')

    log_text = (f"=== 01. SVM (Optimized Baseline) ===\n"
                f"训练数据: {len(full_train_df)} | 测试数据: {len(test_df)}\n"
                f"训练耗时: {train_time:.2f} s | 测试耗时: {test_time:.2f} s\n"
                f"Accuracy: {acc:.4f} | Precision: {p:.4f} | Recall: {r:.4f} | F1-Score: {f1:.4f}\n\n")
    print(log_text)
    with open(CONFIG["log_file"], "a", encoding="utf-8") as f:
        f.write(log_text)
