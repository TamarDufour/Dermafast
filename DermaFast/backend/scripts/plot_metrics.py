import matplotlib.pyplot as plt
import numpy as np

def calculate_metrics(tp, fp, fn):
    """Calculates precision, recall, and f1-score."""
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

def main():
    """Main function to calculate and plot metrics."""
    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    
    # Data from confusion matrices
    # Each dict contains: tn, fp, fn, tp
    confusion_matrices = [
        {'tn': 152, 'fp': 183, 'fn': 8, 'tp': 212},   # Threshold 0.1
        {'tn': 197, 'fp': 138, 'fn': 18, 'tp': 202},  # Threshold 0.2
        {'tn': 225, 'fp': 110, 'fn': 36, 'tp': 184},  # Threshold 0.3
        {'tn': 246, 'fp': 89, 'fn': 62, 'tp': 158},   # Threshold 0.4
        {'tn': 278, 'fp': 57, 'fn': 94, 'tp': 126},   # Threshold 0.5
        {'tn': 299, 'fp': 36, 'fn': 135, 'tp': 85}    # Threshold 0.6
    ]
    
    precisions = []
    recalls = []
    f1_scores = []
    
    for cm in confusion_matrices:
        precision, recall, f1 = calculate_metrics(cm['tp'], cm['fp'], cm['fn'])
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)
        
    plt.figure(figsize=(10, 6))
    plt.plot(thresholds, precisions, marker='o', linestyle='-', label='Precision')
    plt.plot(thresholds, recalls, marker='o', linestyle='-', label='Recall')
    plt.plot(thresholds, f1_scores, marker='o', linestyle='-', label='F1-Score')
    
    plt.title('Precision, Recall, and F1-Score vs. Threshold')
    plt.xlabel('Threshold')
    plt.ylabel('Score')
    plt.xticks(thresholds)
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 1.1)
    
    # Save the plot to a file
    output_filename = 'metrics_vs_threshold.png'
    plt.savefig(output_filename)
    print(f"Plot saved to {output_filename}")
    
    plt.show()

if __name__ == "__main__":
    main()
