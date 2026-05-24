"""
05_llm_lora.py
Qwen2.5-7B LoRA 微调中文情感分析 (含 EarlyStopping)
"""
import time
import pandas as pd
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, EarlyStoppingCallback
from peft import LoraConfig, get_peft_model, TaskType
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

CONFIG = {
    "train_path": "./dataset/train-00000-of-00001-02f200ca5f2a7868.parquet",
    "dev_path": "./dataset/validation-00000-of-00001-405befbaa3bcf1a2.parquet",
    "test_path": "./dataset/test-00000-of-00001-5372924f059fe767.parquet",
    "model_name": "Qwen/Qwen2.5-7B-Instruct",
    "log_file": "./05_qwen_lora_results.txt",
    "max_length": 128, "batch_size": 16, "max_epochs": 20, "lr": 1e-4, "early_stop_patience": 3
}

def compute_metrics(pred):
    labels, preds = pred.label_ids, pred.predictions.argmax(-1)
    p, r, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    return {'accuracy': accuracy_score(labels, preds), 'precision': p, 'recall': r, 'f1': f1}

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(CONFIG["model_name"])
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForSequenceClassification.from_pretrained(
        CONFIG["model_name"], num_labels=2, device_map="auto",
        torch_dtype=torch.bfloat16
    )
    base_model.config.pad_token_id = tokenizer.pad_token_id

    peft_config = LoraConfig(
        task_type=TaskType.SEQ_CLS, r=16, lora_alpha=32,
        target_modules=["q_proj", "v_proj"], lora_dropout=0.05
    )
    model = get_peft_model(base_model, peft_config)

    tokenize_func = lambda e: tokenizer(e["text"], padding="max_length", truncation=True,
                                        max_length=CONFIG["max_length"])
    train_ds = Dataset.from_pandas(pd.read_parquet(CONFIG["train_path"])[['text', 'label']]).map(tokenize_func, batched=True)
    dev_ds = Dataset.from_pandas(pd.read_parquet(CONFIG["dev_path"])[['text', 'label']]).map(tokenize_func, batched=True)
    test_ds = Dataset.from_pandas(pd.read_parquet(CONFIG["test_path"])[['text', 'label']]).map(tokenize_func, batched=True)

    training_args = TrainingArguments(
        output_dir="./qwen_lora_outputs", num_train_epochs=CONFIG["max_epochs"],
        per_device_train_batch_size=CONFIG["batch_size"],
        per_device_eval_batch_size=CONFIG["batch_size"],
        gradient_accumulation_steps=2,
        learning_rate=CONFIG["lr"], bf16=True,
        eval_strategy="epoch", save_strategy="epoch",
        load_best_model_at_end=True, metric_for_best_model="accuracy",
        warmup_step=0.05,
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

    actual_epochs = int(trainer.state.epoch) if trainer.state.epoch is not None else CONFIG["max_epochs"]
    log_text = (f"=== 05. Qwen2.5-7B (LoRA, Epochs: {actual_epochs}) ===\n"
                f"训练耗时: {train_time:.2f} s | 测试耗时: {test_time:.2f} s\n"
                f"Accuracy: {metrics['test_accuracy']:.4f} | Precision: {metrics['test_precision']:.4f} | "
                f"Recall: {metrics['test_recall']:.4f} | F1-Score: {metrics['test_f1']:.4f}\n\n")
    print(log_text)
    with open(CONFIG["log_file"], "a", encoding="utf-8") as f:
        f.write(log_text)
