# 中文情感分析：五模型对比实验

基于 ChnSentiCorp 数据集的中文情感分析（二分类），对比 SVM、Bi-LSTM、BERT、Qwen2.5-7B Zero-shot、Qwen2.5-7B LoRA 五种方法。

## 项目结构

```
├── 01_svm.py              # SVM 基线模型
├── 02_bilstm.py           # Bi-LSTM 模型
├── 03_bert.py             # BERT 微调
├── 04_llm_inference.py    # Qwen2.5-7B 零样本推理
├── 05_llm_lora.py         # Qwen2.5-7B LoRA 微调
├── plot_results.py        # 结果可视化
├── download_data.py       # 数据集下载脚本
├── requirements.txt       # 依赖包
└── dataset/               # 数据集目录
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 下载数据集

```bash
python download_data.py
```

### 3. 运行实验

按顺序运行各模型脚本：

```bash
python 01_svm.py
python 02_bilstm.py
python 03_bert.py
python 04_llm_inference.py
python 05_llm_lora.py
```

> 注意：03_bert.py、04_llm_inference.py、05_llm_lora.py 首次运行时会自动从 HuggingFace 下载预训练模型，需要稳定的网络连接和约 15GB 磁盘空间。

### 4. 生成可视化图表

```bash
python plot_results.py
```

图表将保存至 `./figures/` 目录（PDF 矢量格式，500 DPI）。

## 实验数据量

| 数据集   | 样本数 |
| -------- | ------ |
| 训练集   | 9,600  |
| 验证集   | 1,200  |
| 测试集   | 1,200  |

## 实验结果

| 模型             | Accuracy | Precision | Recall | F1-Score | 训练耗时  | 推理耗时 |
| ---------------- | -------- | --------- | ------ | -------- | --------- | -------- |
| SVM              | 0.8933   | 0.8974    | 0.8914 | 0.8944   | 0.32 s    | 0.02 s   |
| Bi-LSTM          | 0.8983   | 0.8945    | 0.9062 | 0.9003   | 4.05 s    | 0.02 s   |
| BERT             | 0.9517   | 0.9568    | 0.9474 | 0.9521   | 184.66 s  | 1.06 s   |
| Qwen Zero-shot   | 0.9000   | 0.9251    | 0.8734 | 0.8985   | ---       | 43.84 s  |
| Qwen LoRA        | 0.9567   | 0.9633    | 0.9507 | 0.9570   | 1414.10 s | 7.19 s   |

## 硬件要求

- SVM / Bi-LSTM / BERT：CPU 即可，BERT 建议 4GB+ VRAM
- Qwen 模型（LoRA 微调）：建议 16GB+ VRAM（如 NVIDIA RTX 3080 / A4000）
