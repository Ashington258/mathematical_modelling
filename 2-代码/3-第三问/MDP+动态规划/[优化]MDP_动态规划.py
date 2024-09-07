import numpy as np
from itertools import product
from joblib import Parallel, delayed

# 定义问题中的常量
NUM_COMPONENTS = 8
NUM_HALF_PRODUCTS = 3
NUM_FINAL_PRODUCTS = 1
DISCOUNT_FACTOR = 0.9
MAX_ITERATIONS = 1000
CONVERGENCE_THRESHOLD = 1e-4

# 定义成本和收益（根据表2）
components = [
    {"defect_rate": 0.1, "purchase_cost": 2, "inspection_cost": 1},
    {"defect_rate": 0.1, "purchase_cost": 8, "inspection_cost": 1},
    # 省略剩余的部分以节省空间
]

half_products = [
    {
        "defect_rate": 0.1,
        "assembly_cost": 8,
        "inspection_cost": 4,
        "disassembly_cost": 6,
    },
    # 省略剩余的部分以节省空间
]

final_product = {
    "defect_rate": 0.1,
    "assembly_cost": 8,
    "inspection_cost": 6,
    "disassembly_cost": 10,
    "market_price": 200,
    "exchange_loss": 40,
}

# 定义动作空间和状态空间
actions = list(product(["inspect", "not_inspect"], repeat=NUM_COMPONENTS)) + list(
    product(
        ["inspect", "not_inspect", "disassemble"],
        repeat=NUM_HALF_PRODUCTS + NUM_FINAL_PRODUCTS,
    )
)
states = list(
    product([0, 1], repeat=NUM_COMPONENTS + NUM_HALF_PRODUCTS + NUM_FINAL_PRODUCTS)
)


# 定义奖励函数
def reward(state, action):
    # 计算零配件的检测成本
    component_cost = sum(
        c["inspection_cost"] if act == "inspect" else 0
        for c, act in zip(components, action[:NUM_COMPONENTS])
    )

    # 计算半成品和成品的检测/拆解成本
    half_product_cost = sum(
        (
            hp["inspection_cost"]
            if act == "inspect"
            else (hp["disassembly_cost"] if act == "disassemble" else 0)
        )
        for hp, act in zip(
            half_products, action[NUM_COMPONENTS : NUM_COMPONENTS + NUM_HALF_PRODUCTS]
        )
    )

    final_cost = (
        final_product["inspection_cost"]
        if action[-1] == "inspect"
        else (final_product["disassembly_cost"] if action[-1] == "disassemble" else 0)
    )

    # 销售收益减去检测和调换损失
    sales_revenue = final_product["market_price"] * (1 - final_product["defect_rate"])
    expected_cost = (
        final_product["inspection_cost"]
        + final_product["exchange_loss"] * final_product["defect_rate"]
    )

    if action[-1] == "sell" and state[-1] == 1:  # 只有合格的成品才卖
        return (
            sales_revenue
            - expected_cost
            - component_cost
            - half_product_cost
            - final_cost
        )
    else:
        return -component_cost - half_product_cost - final_cost


# 定义状态转移概率函数
def transition_probability(state, action, next_state):
    if action[-1] == "assemble":
        assembly_success = 1 - final_product["defect_rate"]
        return assembly_success if next_state[-1] == 1 else 1 - assembly_success
    elif action[-1] == "disassemble":
        return 1.0 if next_state == state else 0.0
    return 1.0 if next_state == state else 0.0


# 并行化计算每个状态的值
def compute_state_value(s, V, states, actions):
    state = states[s]
    return max(
        reward(state, a)
        + DISCOUNT_FACTOR
        * np.clip(
            sum(
                transition_probability(state, a, next_state)
                * V[states.index(next_state)]
                for next_state in states
            ),
            -1e10,
            1e10,
        )
        for a in actions
    )


# 初始化值函数
V = np.zeros(len(states))

# 值迭代算法
for iteration in range(MAX_ITERATIONS):
    delta = 0
    print(f"Iteration {iteration + 1} starting...")

    # 使用 joblib 并行计算状态值
    new_V = Parallel(n_jobs=-1)(
        delayed(compute_state_value)(s, V, states, actions) for s in range(len(states))
    )

    delta = np.max(np.abs(V - new_V))
    V = new_V

    print(f"Iteration {iteration + 1} completed. Max delta: {delta:.6f}")
    if delta < CONVERGENCE_THRESHOLD:
        print(f"Converged after {iteration + 1} iterations.")
        break

# 输出最优策略
policy = {}
for s, state in enumerate(states):
    best_action = max(
        actions,
        key=lambda a: reward(state, a)
        + DISCOUNT_FACTOR
        * np.clip(
            sum(
                transition_probability(state, a, next_state)
                * V[states.index(next_state)]
                for next_state in states
            ),
            -1e10,
            1e10,
        ),
    )
    policy[state] = best_action

print("Optimal Policy:")
for state, action in policy.items():
    print(f"State {state}: {action}")
