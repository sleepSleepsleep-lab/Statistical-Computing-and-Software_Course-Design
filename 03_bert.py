"""
03_bert.py
优化：加入 EarlyStopping，收敛/过拟合时自动停止，确保训练时间公平可比。
"""
import time
import pandas as pd
from datasets import Dataset
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, EarlyStoppingCallback
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

CONFIG = {
    "train_path": "/root/autodl-tmp/dataset/train-00000-of-00001-02f200ca5f2a7868.parquet",
    "dev_path": "/root/autodl-tmp/dataset/validation-00000-of-00001-405befbaa3bcf1a2.parquet",
    "test_path": "/root/autodl-tmp/dataset/test-00000-of-00001-5372924f059fe767.parquet",
    "model_local_path": "/root/autodl-tmp/model_origin/bert",
    "log_file": "./03_bert_results.txt",
    "max_length": 128, "batch_size": 32, "max_epochs": 20, "lr": 2e-5, "early_stop_patience": 3
}

def compute_metrics(pred):
    labels, preds = pred.label_ids, pred.predictions.argmax(-1)
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    return {'accuracy': accuracy_score(labels, preds), 'precision': p, 'recall': r, 'f1': f1}

if __name__ == "__main__":
    tokenizer = BertTokenizer.from_pretrained(CONFIG["model_local_path"], local_files_only=True)
    model = BertForSequenceClassification.from_pretrained(CONFIG["model_local_path"], num_labels=2, local_files_only=True)
    tokenize_func = lambda e: tokenizer(e["text"], padding="max_length", truncation=True, max_length=CONFIG["max_length"])

    train_ds = Dataset.from_pandas(pd.read_parquet(CONFIG["train_path"])[['text', 'label']]).map(tokenize_func, batched=True)
    dev_ds = Dataset.from_pandas(pd.read_parquet(CONFIG["dev_path"])[['text', 'label']]).map(tokenize_func, batched=True)
    test_ds = Dataset.from_pandas(pd.read_parquet(CONFIG["test_path"])[['text', 'label']]).map(tokenize_func, batched=True)

    training_args = TrainingArguments(
        output_dir="./bert_outputs", num_train_epochs=CONFIG["max_epochs"],
        per_device_train_batch_size=CONFIG["batch_size"], per_device_eval_batch_size=CONFIG["batch_size"],
        learning_rate=CONFIG["lr"], eval_strategy="epoch", save_strategy="epoch", 
        load_best_model_at_end=True, metric_for_best_model="accuracy",
        warmup_step=0.1, weight_decay=0.01,
        logging_strategy="epoch", report_to="none"
    )

    trainer = Trainer(
        model=model, args=training_args, train_dataset=train_ds, eval_dataset=dev_ds, 
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=CONFIG["early_stop_patience"])]
    )

    t0 = time.time()
    trainer.train()
    train_time = time.time() - t0

    t1 = time.time()
    metrics = trainer.predict(test_ds).metrics 
    test_time = time.time() - t1

    # 【核心修改区】：提取 Trainer 自动生成的 test_ 前缀指标，并统一排版
    actual_epochs = int(trainer.state.epoch) if trainer.state.epoch is not None else CONFIG["max_epochs"]
    log_text = (f"=== 03. BERT Fine-Tuning (Epochs: {actual_epochs}) ===\n"
                f"训练耗时: {train_time:.2f} s | 测试耗时: {test_time:.2f} s\n"
                f"Accuracy: {metrics['test_accuracy']:.4f} | Precision: {metrics['test_precision']:.4f} | Recall: {metrics['test_recall']:.4f} | F1-Score: {metrics['test_f1']:.4f}\n\n")
    print(log_text)
    with open(CONFIG["log_file"], "a", encoding="utf-8") as f: f.write(log_text)