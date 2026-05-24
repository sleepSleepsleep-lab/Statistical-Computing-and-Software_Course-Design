"""
download_data.py
下载 ChnSentiCorp 中文情感分析数据集
"""
import os
from datasets import load_dataset

DATASET_DIR = "./dataset"
os.makedirs(DATASET_DIR, exist_ok=True)

print("正在从 HuggingFace 下载 ChnSentiCorp 数据集...")
ds = load_dataset("seamew/ChnSentiCorp")

for split in ["train", "validation", "test"]:
    filename_map = {
        "train": "train-00000-of-00001-02f200ca5f2a7868.parquet",
        "validation": "validation-00000-of-00001-405befbaa3bcf1a2.parquet",
        "test": "test-00000-of-00001-5372924f059fe767.parquet",
    }
    path = os.path.join(DATASET_DIR, filename_map[split])
    ds[split].to_parquet(path)
    print(f"  [{split}] 已保存 -> {path}  ({len(ds[split])} 条)")

print(f"\n数据集下载完成，共 {sum(len(ds[s]) for s in ds)} 条。")
