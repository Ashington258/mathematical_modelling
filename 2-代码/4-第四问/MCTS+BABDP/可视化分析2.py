import itertools
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import random


class BAMDPState:
    def __init__(self, path, parts, semi_products, final_product, n_c, prior_beliefs):
        self.path = path
        self.parts = parts
        self.semi_products = semi_products
        self.final_product = final_product
        self.n_c = n_c
        self.prior_beliefs = prior_beliefs

    def reward(self):
        reward = 0
        for decision in self.path:
            reward += 10 if decision == 1 else -5  # 示例逻辑，选择1得10分，选择0扣5分
        return reward


def generate_all_decision_paths():
    return list(itertools.product([0, 1], repeat=5))  # 使用更短的路径以便于可视化


def evaluate_all_paths(root_state):
    decision_paths = generate_all_decision_paths()
    results = []
    for path in decision_paths:
        state = BAMDPState(
            path,
            root_state.parts,
            root_state.semi_products,
            root_state.final_product,
            root_state.n_c,
            root_state.prior_beliefs,
        )
        reward = state.reward()
        results.append((path, reward))
    return results


def paths_to_dataframe(results):
    paths = []
    rewards = []
    for path, reward in results:
        paths.append(list(path))
        rewards.append(reward)
    df = pd.DataFrame(paths, columns=[f"decision_{i+1}" for i in range(len(paths[0]))])
    df["reward"] = rewards
    return df


def visualize_results(df):
    fig = px.scatter_matrix(
        df,
        dimensions=[f"decision_{i+1}" for i in range(5)],
        color="reward",
        title="Decision Paths vs. Reward",
    )
    fig.show()


def visualize_decision_tree(results):
    G = nx.DiGraph()
    labels = {}
    node_colors = []
    for path, reward in results:
        for i in range(len(path)):
            node_path = path[:i]
            node_label = ".".join(str(x) for x in node_path)
            child_label = node_label + (".1" if path[i] == 1 else ".0")
            if node_label not in G:
                G.add_node(node_label)
            if child_label not in G:
                G.add_node(child_label)
            G.add_edge(node_label, child_label)
            labels[node_label] = node_label
            node_colors.append(reward)
    pos = nx.drawing.nx_pydot.graphviz_layout(G, prog="dot")
    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        labels=labels,
        node_size=500,
        node_color=node_colors,
        cmap=plt.cm.Blues,
        font_size=8,
        font_color="white",
    )
    plt.title("Decision Tree Visualization")
    plt.show()


# 代码逻辑继续…
parts = [
    {"defect_rate": 0.10, "purchase_price": 2, "inspection_cost": 4.0} for _ in range(8)
]
semi_products = [
    {
        "defect_rate": 0.10,
        "assembly_cost": 8.0,
        "inspection_cost": 4.0,
        "disassembly_cost": 6.0,
    }
    for _ in range(3)
]
final_product = {
    "defect_rate": 0.10,
    "assembly_cost": 8.0,
    "inspection_cost": 6.0,
    "disassembly_cost": 10.0,
    "market_price": 200,
    "exchange_loss": 40.0,
}
n_c = 3
prior_beliefs = [0.1, 0.1, 0.1]
initial_state = BAMDPState([], parts, semi_products, final_product, n_c, prior_beliefs)
results = evaluate_all_paths(initial_state)
df = paths_to_dataframe(results)
visualize_results(df)
visualize_decision_tree(results)
