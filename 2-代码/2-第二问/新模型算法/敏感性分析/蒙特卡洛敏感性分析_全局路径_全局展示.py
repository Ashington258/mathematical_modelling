import os
import json
import numpy as np
import matplotlib.pyplot as plt
from itertools import product

# Set the working directory to the script directory
os.chdir(os.path.dirname(__file__))
print("Current working directory:", os.getcwd())


# Load data from a JSON file
def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# Calculate the profit for a decision path
def calculate_profit(
    n_c,
    p_c_1,
    p_c_2,
    c_p_1,
    c_p_2,
    c_d_1,
    c_d_2,
    p_f,
    c_s_f,
    c_d_f,
    s_f,
    c_s,
    c_a_f,
    decision,
):
    x_1, x_2, y, z = decision
    effective_parts = n_c * (1 - x_1 * p_c_1) * (1 - x_2 * p_c_2)
    n_f = effective_parts * (1 - p_f)
    C_c_p = n_c * (c_p_1 + c_p_2)
    C_c_d = n_c * (x_1 * c_d_1 + x_2 * c_d_2)
    C_d_f = c_d_f * y * n_f * (1 - p_f)
    C_a_f = c_a_f * z * n_f * p_f
    C_s = c_s * y * n_f * p_f
    C_s_f = c_s_f * n_f
    S = s_f * n_f
    Z = C_c_p + C_c_d + C_d_f + C_a_f + C_s + C_s_f - S
    return -Z


# Perform Monte Carlo sensitivity analysis on all decisions for a case
def monte_carlo_sensitivity_on_decisions(all_data, n_simulations=100):
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))  # Adjust subplot layout as needed
    axes = axes.flatten()  # Flatten if using more than one row
    decisions = list(product([0, 1], repeat=4))  # Generate all decision combinations

    for idx, case_data in enumerate(all_data["scenarios"]):
        p_c_1_samples = np.random.uniform(0, 0.1, n_simulations)
        max_profits = []

        for decision in decisions:
            profits = []
            for p_c_1 in p_c_1_samples:
                profit = calculate_profit(
                    100,
                    p_c_1,
                    case_data["part_2_defect_rate"],
                    case_data["part_1_purchase_price"],
                    case_data["part_2_purchase_price"],
                    case_data["part_1_detection_cost"],
                    case_data["part_2_detection_cost"],
                    case_data["product_defect_rate"],
                    case_data["assembly_cost"],
                    case_data["product_detection_cost"],
                    case_data["market_price"],
                    case_data["replacement_loss"],
                    case_data["disassembly_cost"],
                    decision,
                )
                profits.append(profit)
            max_profits.append(max(profits))
            normalized_profits = [
                (profit / max(max_profits)) * 100 for profit in profits
            ]  # Normalize
            axes[idx].scatter(
                p_c_1_samples,
                normalized_profits,
                alpha=0.5,
                label=f"Decision: {decision}",
            )

        axes[idx].set_title(f'Case {case_data["case"]}')
        axes[idx].set_xlabel("Part 1 Defect Rate (p_c_1)")
        axes[idx].set_ylabel("Normalized Profit (%)")
        axes[idx].legend()
        axes[idx].grid(True)

    plt.tight_layout()
    plt.show()


# Load data from JSON
data_path = "./data.json"
data = load_data_from_json(data_path)

# Perform sensitivity analysis on each case
monte_carlo_sensitivity_on_decisions(data, 100)
