"""
04_llm_inference.py
任务：在 1.2k test 数据集上进行 0/1 推理。
"""
import time
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

CONFIG = {
    "test_path": "/root/autodl-tmp/dataset/test-00000-of-00001-5372924f059fe767.parquet", 
    "model_local_path": "/root/autodl-tmp/model_origin/qwen",
    "log_file": "./04_qwen_zeroshot_results.txt",
    "device": "cuda" if torch.cuda.is_available() else "cpu"
}

def extract_label(text):
    if '1' in text or '正' in text: return 1
    if '0' in text or '负' in text: return 0
    return 0

if __name__ == "__main__":
    test_df = pd.read_parquet(CONFIG["test_path"])
    y_true, y_pred = test_df['label'].tolist(), []
    
    tokenizer = AutoTokenizer.from_pretrained(CONFIG["model_local_path"], local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(
        CONFIG["model_local_path"], device_map="auto", torch_dtype=torch.bfloat16, local_files_only=True
    )
    model.eval()

    total_tokens, t0 = 0, time.time()
    with torch.no_grad():
        for text in tqdm(test_df['text'], desc=f"Evaluating on {len(test_df)} Test Rows"):
            messages = [{"role": "system", "content": "情感分析：好评输出1，差评输出0。"},{"role": "user", "content": text}]
            inputs = tokenizer(tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True), return_tensors="pt").to(CONFIG["device"])
            outputs = model.generate(**inputs, max_new_tokens=5, do_sample=False, pad_token_id=tokenizer.eos_token_id)
            gen_ids = outputs[0][inputs.input_ids.shape[1]:]
            total_tokens += len(gen_ids)
            y_pred.append(extract_label(tokenizer.decode(gen_ids, skip_special_tokens=True)))
    test_time = time.time() - t0

    acc = accuracy_score(y_true, y_pred)
    p, r, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')
    log_text = (f"=== 04. Qwen2.5-7B (Zero-shot) ===\n"
                f"耗时: {test_time:.2f} s | 速度: {total_tokens/test_time if test_time>0 else 0:.2f} Tokens/s\n"
                f"Accuracy: {acc:.4f} | Precision: {p:.4f} | Recall: {r:.4f} | F1: {f1:.4f}\n\n")
    print(log_text)
    with open(CONFIG["log_file"], "a", encoding="utf-8") as f: f.write(log_text)