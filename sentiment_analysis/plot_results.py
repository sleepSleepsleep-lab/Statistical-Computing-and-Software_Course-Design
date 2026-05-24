# -*- coding: utf-8 -*-
"""
论文可视化脚本：五模型情感分析对比图表 (DPI=500)
所有图表保存为 PDF 矢量格式，适配 LaTeX 编译
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

output_dir = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(output_dir, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["SimHei", "Microsoft YaHei", "Arial", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "mathtext.default": "regular",
    "figure.dpi": 200,
    "savefig.dpi": 500,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
    "savefig.format": "pdf",
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#444444",
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 3.5,
    "ytick.major.size": 3.5,
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "legend.fontsize": 10,
    "legend.framealpha": 0.85,
    "legend.edgecolor": "#cccccc",
    "legend.fancybox": True,
    "figure.facecolor": "white",
    "axes.facecolor": "#fcfcfc",
})

MODELS_SHORT = ["SVM", "Bi-LSTM", "BERT", "Qwen\nZero-shot", "Qwen\nLoRA"]
MODELS_ONELINE = ["SVM", "Bi-LSTM", "BERT", "Qwen Zero-shot", "Qwen LoRA"]

C = {
    "svm":        "#4472C4",
    "lstm":       "#ED7D31",
    "bert":       "#70AD47",
    "qwen_zero":  "#9B59B6",
    "qwen_lora":  "#C00000",
    "best_hl":    "#FFF2CC",
    "metric_a":   "#4472C4",
    "metric_b":   "#C44E52",
}
COLORS = [C["svm"], C["lstm"], C["bert"], C["qwen_zero"], C["qwen_lora"]]
C_EDGE = ["#2B579A", "#C55A11", "#4F8A26", "#723B8E", "#8A0000"]

accuracy  = [0.8933, 0.8983, 0.9517, 0.9000, 0.9567]
precision = [0.8974, 0.8945, 0.9568, 0.9251, 0.9633]
recall    = [0.8914, 0.9062, 0.9474, 0.8734, 0.9507]
f1        = [0.8944, 0.9003, 0.9521, 0.8985, 0.9570]
train_t   = [0.32,   4.05,   184.66, 0,      1414.10]
infer_t   = [0.02,   0.02,   1.06,   43.84,  7.19]

best_idx = 4


def save(name):
    path = os.path.join(output_dir, name)
    plt.savefig(path, dpi=500)
    print(f"[OK] {name}")
    plt.close()


def style_ax(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#555555")
    ax.spines["bottom"].set_color("#555555")
    ax.tick_params(colors="#444444")
    ax.grid(axis="y", alpha=0.25, linestyle=(0, (3, 4)), color="#aaaaaa", zorder=0)


def label_bars(ax, bars, fmt="{:.4f}", offset=0.004, fontsize=8.5):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., h + offset,
                fmt.format(h), ha="center", va="bottom",
                fontsize=fontsize, fontweight="bold", color="#333333")


def fig_d1_performance():
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    x = np.arange(len(MODELS_SHORT))
    w = 0.30
    gap = 0.02

    b1 = ax.bar(x - w/2 - gap, accuracy, w, label="Accuracy",
                color=C["metric_a"], edgecolor="white", linewidth=0.5, zorder=3)
    b2 = ax.bar(x + w/2 + gap, f1, w, label="F1-Score",
                color=C["metric_b"], edgecolor="white", linewidth=0.5, zorder=3)

    label_bars(ax, b1, offset=0.002, fontsize=7.5)
    label_bars(ax, b2, offset=0.002, fontsize=7.5)

    ax.axvspan(best_idx - 0.45, best_idx + 0.45, facecolor=C["best_hl"],
               alpha=0.35, zorder=0)
    ax.annotate("Best", xy=(best_idx, 0.955), fontsize=9, fontweight="bold",
                color="#8B0000", ha="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#fff2cc",
                          edgecolor="#B8860B", alpha=0.9))

    ax.set_xticks(x)
    ax.set_xticklabels(MODELS_SHORT, fontsize=10.5)
    ax.set_ylabel("Score", fontsize=12, fontweight="bold", color="#333333")
    ax.set_ylim(0.865, 0.965)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.3f"))
    ax.legend(loc="lower right", frameon=True, fontsize=10.5,
              handlelength=1.2, handleheight=0.7)
    style_ax(ax)
    fig.tight_layout()
    save("fig_d1_performance.pdf")


def fig_d2_train_time():
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    x = np.arange(len(MODELS_SHORT))
    td = [train_t[0], train_t[1], train_t[2], 0, train_t[4]]
    bars = ax.bar(x, [v if v > 0 else 1e-5 for v in td],
                  color=COLORS, edgecolor="white", linewidth=0.6, zorder=3, width=0.55)

    for i, (bar, t) in enumerate(zip(bars, td)):
        if t == 0:
            ax.text(bar.get_x() + bar.get_width()/2, 2,
                    "Zero-shot\n---", ha="center", va="bottom",
                    fontsize=8.5, fontstyle="italic", color="#888888", fontweight="bold")
        else:
            offset = max(t * 0.08, 1)
            ax.text(bar.get_x() + bar.get_width()/2, t + offset,
                    f"{t:.2f} s", ha="center", va="bottom",
                    fontsize=9, fontweight="bold", color="#333333")

    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(MODELS_SHORT, fontsize=10.5)
    ax.set_ylabel("Training Time (s, log scale)", fontsize=12, fontweight="bold", color="#333333")
    ax.set_ylim(0.15, 3500)
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    style_ax(ax)
    fig.tight_layout()
    save("fig_d2_train_time.pdf")


def fig_d3_infer_time():
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    x = np.arange(len(MODELS_SHORT))
    bars = ax.bar(x, infer_t, color=COLORS, edgecolor="white", linewidth=0.6,
                  zorder=3, width=0.55)

    for bar, t in zip(bars, infer_t):
        offset = max(t * 0.08, 0.3)
        ax.text(bar.get_x() + bar.get_width()/2, t + offset,
                f"{t:.2f} s", ha="center", va="bottom",
                fontsize=9, fontweight="bold", color="#333333")

    speed_labels = ["60,000", "60,000", "1,132", "27", "167"]
    for i, (bar, t) in enumerate(zip(bars, infer_t)):
        time_label_y = t + max(t * 0.08, 0.3)
        ax.text(bar.get_x() + bar.get_width()/2, time_label_y * 1.9,
                f"{speed_labels[i]} samp/s", ha="center", va="bottom",
                fontsize=7, fontstyle="italic", color="#666666", fontweight="bold")

    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(MODELS_SHORT, fontsize=10.5)
    ax.set_ylabel("Inference Time (s, log scale)", fontsize=12, fontweight="bold", color="#333333")
    ax.set_ylim(0.015, 200)
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    style_ax(ax)
    fig.tight_layout()
    save("fig_d3_infer_time.pdf")


def fig_d4_tradeoff():
    fig, ax = plt.subplots(figsize=(8.0, 5.2))
    sizes = [220, 220, 380, 320, 420]
    edge_colors = C_EDGE
    for i in range(5):
        tx = train_t[i] if train_t[i] > 0 else 0.8
        ax.scatter(tx, f1[i], s=sizes[i], c=COLORS[i],
                   edgecolors=edge_colors[i], linewidth=1.5,
                   zorder=6, alpha=0.93)

    pareto_idx = [0, 2, 4]
    pareto_x = [train_t[0] if train_t[0] > 0 else 0.8, train_t[2], train_t[4]]
    pareto_y = [f1[0], f1[2], f1[4]]
    ax.plot(pareto_x, pareto_y, color="#777777", linewidth=1.5,
            linestyle="--", marker="o", markersize=0, alpha=0.6, zorder=2)
    ax.annotate("Pareto Frontier", xy=(pareto_x[1], pareto_y[1]),
                xytext=(35, -28), textcoords="offset points",
                fontsize=8.5, fontstyle="italic", color="#666666",
                arrowprops=dict(arrowstyle="->", color="#999999", lw=1.0))

    offsets = [(15, -15), (20, -18), (20, -15), (15, -22), (25, -15)]
    for i in range(5):
        tx_ = train_t[i] if train_t[i] > 0 else 0.8
        ax.annotate(MODELS_ONELINE[i], (tx_, f1[i]),
                    textcoords="offset points", xytext=offsets[i],
                    fontsize=9.5, fontweight="bold", color=COLORS[i])

    ax.set_xscale("log")
    ax.set_xlabel("Training Time (s, log scale)", fontsize=12, fontweight="bold", color="#333333")
    ax.set_ylabel("F1-Score", fontsize=12, fontweight="bold", color="#333333")
    ax.set_ylim(0.878, 0.964)
    ax.set_xlim(0.15, 3800)
    style_ax(ax)
    fig.tight_layout()
    save("fig_d4_tradeoff.pdf")


def fig_d5_precision_recall():
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    x = np.arange(len(MODELS_SHORT))
    w = 0.30
    gap = 0.02

    b1 = ax.bar(x - w/2 - gap, precision, w, label="Precision",
                color=C["metric_a"], edgecolor="white", linewidth=0.5, zorder=3)
    b2 = ax.bar(x + w/2 + gap, recall, w, label="Recall",
                color=C["metric_b"], edgecolor="white", linewidth=0.5, zorder=3)

    label_bars(ax, b1, offset=0.002)
    label_bars(ax, b2, offset=0.002)

    for i in range(5):
        diff = precision[i] - recall[i]
        top_y = max(precision[i], recall[i]) + 0.010
        sign = "+" if diff > 0 else ""
        ax.annotate(f"P-R={sign}{diff:.4f}", xy=(x[i], top_y),
                    fontsize=7, ha="center", va="bottom",
                    color="#333333",
                    fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2",
                              facecolor="#ffffff",
                              edgecolor="#888888",
                              alpha=0.9, linewidth=0.5))

    ax.set_xticks(x)
    ax.set_xticklabels(MODELS_SHORT, fontsize=10.5)
    ax.set_ylabel("Score", fontsize=12, fontweight="bold", color="#333333")
    ax.set_ylim(0.845, 0.978)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.3f"))
    ax.legend(loc="lower right", frameon=True, fontsize=10.5,
              handlelength=1.2, handleheight=0.7)
    fig.tight_layout()
    save("fig_d5_precision_recall.pdf")


def fig_d6_waterfall():
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    x = np.arange(len(MODELS_SHORT))

    bars = ax.bar(x, f1, color=COLORS, edgecolor="white", linewidth=0.8,
                  width=0.50, zorder=3)

    for i, bar in enumerate(bars):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.002,
                f"{f1[i]:.4f}", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color="#1a1a1a")

    for i in range(len(f1) - 1):
        mid_x = (x[i] + x[i+1]) / 2
        mid_y = (f1[i] + f1[i+1]) / 2
        delta = f1[i+1] - f1[i]
        sign = "+" if delta > 0 else ""
        color_d = "#1a7a1a" if delta > 0 else "#b71c1c"
        ax.plot([x[i] + 0.28, x[i+1] - 0.28], [f1[i], f1[i+1]],
                color="#777777", linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
        ax.annotate(f"{sign}{delta:.4f}", xy=(mid_x, mid_y),
                    fontsize=8.5, fontweight="bold", color=color_d,
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                              edgecolor=color_d, alpha=0.9, linewidth=0.7))

    ax.axhline(y=f1[0], color=C["svm"], linewidth=1.0, linestyle="--",
               alpha=0.5, zorder=1)
    ax.text(4.2, f1[0] + 0.001, f"SVM baseline ({f1[0]:.4f})",
            fontsize=8, color=C["svm"], fontstyle="italic", alpha=0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(MODELS_SHORT, fontsize=10.5)
    ax.set_ylabel("F1-Score", fontsize=12, fontweight="bold", color="#333333")
    ax.set_ylim(0.875, 0.960)
    style_ax(ax)
    fig.tight_layout()
    save("fig_d6_waterfall.pdf")


def fig_d7_radar():
    categories = ["Accuracy", "Precision", "Recall", "F1-Score"]
    N = len(categories)
    data = np.array([
        [0.8933, 0.8974, 0.8914, 0.8944],
        [0.8983, 0.8945, 0.9062, 0.9003],
        [0.9517, 0.9568, 0.9474, 0.9521],
        [0.9000, 0.9251, 0.8734, 0.8985],
        [0.9567, 0.9633, 0.9507, 0.9570],
    ])
    data_norm = (data - 0.87) / (0.97 - 0.87)

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7.0, 7.0), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    for i in range(5):
        vals = data_norm[i].tolist() + data_norm[i].tolist()[:1]
        ax.fill(angles, vals, alpha=0.08, color=COLORS[i])
        ax.plot(angles, vals, "o-", linewidth=1.3, color=COLORS[i],
                markersize=5, label=MODELS_ONELINE[i])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10.5, fontweight="bold")
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.890", "0.910", "0.930", "0.950", "0.970"], fontsize=7.5, color="#888888")
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.12),
              frameon=True, fontsize=9.5, ncol=1)
    ax.grid(True, alpha=0.3, linestyle="--")
    fig.tight_layout()
    save("fig_d7_radar.pdf")


def fig_d8_dual_axis_time():
    fig, ax1 = plt.subplots(figsize=(8.2, 4.8))
    x = np.arange(len(MODELS_SHORT))
    w = 0.35

    td_plot = [train_t[0], train_t[1], train_t[2], 0.5, train_t[4]]
    b1 = ax1.bar(x - w/2, td_plot, w, label="Training Time (s)",
                 color=C["metric_a"], edgecolor="white", linewidth=0.5, zorder=3)
    ax1.set_ylabel("Training Time (s)", fontsize=11, fontweight="bold", color=C["metric_a"])
    ax1.set_yscale("log")
    ax1.set_ylim(0.15, 3500)
    ax1.tick_params(axis="y", colors=C["metric_a"])

    ax2 = ax1.twinx()
    b2 = ax2.bar(x + w/2, infer_t, w, label="Inference Time (s)",
                 color=C["metric_b"], edgecolor="white", linewidth=0.5, zorder=3)
    ax2.set_ylabel("Inference Time (s)", fontsize=11, fontweight="bold", color=C["metric_b"])
    ax2.set_yscale("log")
    ax2.set_ylim(0.01, 200)
    ax2.tick_params(axis="y", colors=C["metric_b"])

    for i, (t_r, t_i) in enumerate(zip(td_plot, infer_t)):
        ax1.text(x[i] - w/2, t_r * 1.4 if t_r > 0 else 0.8, f"{train_t[i]:.1f}s",
                 ha="center", fontsize=7.5, fontweight="bold", color=C["metric_a"])
        ax2.text(x[i] + w/2, t_i * 1.3, f"{infer_t[i]:.2f}s",
                 ha="center", fontsize=7.5, fontweight="bold", color=C["metric_b"])

    ax1.set_xticks(x)
    ax1.set_xticklabels(MODELS_SHORT, fontsize=10)
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax1.grid(axis="y", alpha=0.2, linestyle=(0, (3, 4)), color="#aaaaaa", zorder=0)
    fig.tight_layout()
    save("fig_d8_dual_time.pdf")


def fig_d9_model_size():
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    params = [0.0, 2.0, 110, 7000, 7000 + 3.4]
    markers = [180, 200, 380, 550, 580]

    for i in range(5):
        ax.scatter(params[i], f1[i], s=markers[i], c=COLORS[i],
                   edgecolors="#333333", linewidth=1.0, zorder=5, alpha=0.9)

    for i in range(5):
        offset = (15, 0.001) if i != 3 else (-35, -0.003)
        ax.annotate(MODELS_ONELINE[i], (params[i], f1[i]),
                    textcoords="offset points", xytext=offset,
                    fontsize=9, fontweight="bold", color=COLORS[i])

    ax.set_xscale("symlog", linthresh=1)
    ax.set_xlabel("Model Parameters (Millions, log scale)", fontsize=11,
                  fontweight="bold", color="#333333")
    ax.set_ylabel("F1-Score", fontsize=11, fontweight="bold", color="#333333")
    ax.set_ylim(0.882, 0.964)
    ax.set_xlim(left=-0.5, right=11000)
    style_ax(ax)
    fig.tight_layout()
    save("fig_d9_model_size.pdf")


if __name__ == "__main__":
    fig_d1_performance()
    fig_d2_train_time()
    fig_d3_infer_time()
    fig_d4_tradeoff()
    fig_d5_precision_recall()
    fig_d6_waterfall()
    fig_d7_radar()
    fig_d8_dual_axis_time()
    fig_d9_model_size()
    print(f"\nAll 9 figures saved to: {output_dir}")
    print("DPI: 500 | Format: PDF Vector")
