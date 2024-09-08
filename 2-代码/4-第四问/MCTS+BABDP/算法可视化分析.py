import itertools
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


# 假设 BAMDPState 是表示当前状态的类，允许根据路径进行决策和计算收益
class BAMDPState:
    def __init__(self, path, parts, semi_products, final_product, n_c, prior_beliefs):
        self.path = path  # 当前路径
        self.parts = parts  # 零配件列表
        self.semi_products = semi_products  # 半成品列表
        self.final_product = final_product  # 成品信息
        self.n_c = n_c  # 一些与状态相关的计数器或参数
        self.prior_beliefs = prior_beliefs  # 先验信息

    def reward(self):
        # 在这里计算路径的收益，使用self.path来计算
        reward = 0
        for decision in self.path:
            if decision == 1:
                reward += 10  # 示例逻辑，选择了这个决策会有一定收益
        return reward


# 使用穷举法生成所有可能的决策路径
def generate_all_decision_paths():
    return list(itertools.product([0, 1], repeat=16))


# 计算所有路径的收益并存储结果
def evaluate_all_paths(root_state):
    decision_paths = generate_all_decision_paths()
    results = []

    for path in decision_paths:
        # 更新state为当前路径下的决策
        state = BAMDPState(
            list(path),
            root_state.parts,
            root_state.semi_products,
            root_state.final_product,
            root_state.n_c,
            root_state.prior_beliefs,
        )
        reward = state.reward()  # 计算当前路径的收益
        probability = np.random.uniform(
            0, 1
        )  # 伪造的蒙特卡洛概率值，实际应根据具体模型计算
        results.append((path, reward, probability))

    return results


# 将决策路径转换为可视化的数据格式
def paths_to_dataframe(results):
    paths = []
    rewards = []
    probabilities = []
    for path, reward, probability in results:
        paths.append(list(path))
        rewards.append(reward)
        probabilities.append(probability)

    # 创建一个包含路径、收益和概率的DataFrame
    df = pd.DataFrame(paths, columns=[f"decision_{i+1}" for i in range(16)])
    df["reward"] = rewards
    df["probability"] = probabilities
    return df


# 绘制相关性散点图
def visualize_results(df):
    fig = px.scatter_matrix(
        df,
        dimensions=[f"decision_{i+1}" for i in range(16)],  # 决策作为维度
        color="reward",  # 用收益值作为颜色标注
        title="各决策路径与收益的相关性散点图",
    )
    fig.show()


# 可视化蒙特卡洛概率图模型
def visualize_monte_carlo(df):
    fig = px.scatter(
        df,
        x="probability",
        y="reward",
        color="reward",
        title="蒙特卡洛概率与收益的散点图",
        labels={"probability": "Probability", "reward": "Reward"},
    )
    fig.show()


# 可视化决策路径的平行坐标图
def visualize_decision_space(df):
    fig = px.parallel_coordinates(
        df,
        dimensions=[f"decision_{i+1}" for i in range(16)] + ["reward"],
        color="reward",
        title="决策路径与收益的平行坐标图",
    )
    fig.show()


# 零件信息和初始状态（示例数据）
parts = [
    {"defect_rate": 0.10, "purchase_price": 2, "inspection_cost": 4.0},  # 零配件 1
    {"defect_rate": 0.10, "purchase_price": 8, "inspection_cost": 4.0},  # 零配件 2
    {"defect_rate": 0.10, "purchase_price": 12, "inspection_cost": 4.0},  # 零配件 3
    {"defect_rate": 0.10, "purchase_price": 2, "inspection_cost": 0.0},  # 零配件 4
    {"defect_rate": 0.10, "purchase_price": 8, "inspection_cost": 0.0},  # 零配件 5
    {"defect_rate": 0.10, "purchase_price": 12, "inspection_cost": 0.0},  # 零配件 6
    {"defect_rate": 0.10, "purchase_price": 8, "inspection_cost": 0.0},  # 零配件 7
    {"defect_rate": 0.10, "purchase_price": 12, "inspection_cost": 0.0},  # 零配件 8
]

semi_products = [
    {
        "defect_rate": 0.10,
        "assembly_cost": 8.0,
        "inspection_cost": 4.0,
        "disassembly_cost": 6.0,
    },  # 半成品 1
    {
        "defect_rate": 0.10,
        "assembly_cost": 8.0,
        "inspection_cost": 4.0,
        "disassembly_cost": 6.0,
    },  # 半成品 2
    {
        "defect_rate": 0.10,
        "assembly_cost": 8.0,
        "inspection_cost": 4.0,
        "disassembly_cost": 6.0,
    },  # 半成品 3
]

final_product = {
    "defect_rate": 0.10,
    "assembly_cost": 8.0,
    "inspection_cost": 6.0,
    "disassembly_cost": 10.0,
    "market_price": 200,
    "exchange_loss": 40.0,
}

# 先验信息和其他状态参数
n_c = 3  # 示例值
prior_beliefs = [0.1, 0.1, 0.1]  # 示例值

# 创建初始状态
initial_state = BAMDPState([], parts, semi_products, final_product, n_c, prior_beliefs)

# 使用穷举法评估所有路径
results = evaluate_all_paths(initial_state)

# 转换为DataFrame以便可视化
df = paths_to_dataframe(results)

# 绘制相关性散点图
visualize_results(df)

# 可视化蒙特卡洛概率模型
visualize_monte_carlo(df)

# 可视化决策空间
visualize_decision_space(df)
