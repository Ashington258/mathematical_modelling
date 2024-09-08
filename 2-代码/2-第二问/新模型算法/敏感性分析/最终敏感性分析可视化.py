import os
import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from itertools import product
from plotly.colors import qualitative

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
    decisions = list(product([0, 1], repeat=4))  # Generate all decision combinations
    decision_colors = (
        qualitative.Plotly
    )  # Use Plotly's built-in qualitative color scheme

    # Ensure there are enough colors for the decisions
    if len(decisions) > len(decision_colors):
        decision_colors *= len(decisions) // len(decision_colors) + 1

    # Create subplot grid
    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=[
            f'Case {case_data["case"]}' for case_data in all_data["scenarios"]
        ],
    )

    for idx, case_data in enumerate(all_data["scenarios"]):
        p_c_1_samples = np.random.uniform(0, 0.1, n_simulations)
        max_profits = []

        for decision, color in zip(decisions, decision_colors):
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
            row = idx // 3 + 1
            col = idx % 3 + 1
            fig.add_trace(
                go.Scatter(
                    x=p_c_1_samples,
                    y=normalized_profits,
                    mode="markers",
                    marker=dict(color=color),
                    name=(f"Decision: {decision}" if idx == 0 else ""),
                    showlegend=(idx == 0),
                ),
                row=row,
                col=col,
            )

        fig.update_xaxes(title_text="Part 1 Defect Rate (p_c_1)", row=row, col=col)
        fig.update_yaxes(title_text="Normalized Profit (%)", row=row, col=col)

    fig.update_layout(
        title="Monte Carlo Sensitivity Analysis on Decisions",
        legend_title_text="Decisions",
        height=800,
        width=1200,
        margin=dict(l=50, r=50, t=50, b=50),
        showlegend=True,
    )

    fig.show()


# Load data from JSON
data_path = "./data.json"
data = load_data_from_json(data_path)

# Perform sensitivity analysis on each case
monte_carlo_sensitivity_on_decisions(data, 100)
