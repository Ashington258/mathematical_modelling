import itertools
import pandas as pd
import matplotlib.pyplot as plt


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
        # 示例收益计算（根据项目实际逻辑进行调整）
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
        results.append((path, reward))

    return results


# 将决策路径转换为可视化的数据格式
def paths_to_dataframe(results):
    paths = []
    rewards = []
    for path, reward in results:
        paths.append(list(path))
        rewards.append(reward)

    # 创建一个包含路径和收益的DataFrame
    df = pd.DataFrame(paths, columns=[f"decision_{i+1}" for i in range(16)])
    df["reward"] = rewards
    return df


# 绘制每种决策路径下的收益散点图，并标记最大值
def plot_reward_scatter(df):
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(df)), df["reward"], alpha=0.5)

    # 标记最大值
    max_reward_index = df["reward"].idxmax()
    max_reward_value = df["reward"].max()
    plt.scatter(
        max_reward_index,
        max_reward_value,
        color="red",
        label=f"Max Reward: {max_reward_value}",
    )

    plt.title("Scatter Plot of Rewards for Each Decision Path")
    plt.xlabel("Decision Path Index")
    plt.ylabel("Reward")
    plt.legend()
    plt.grid(True)
    plt.show()


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

# 绘制收益散点图，并标记最大值
plot_reward_scatter(df)
