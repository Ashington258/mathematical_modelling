import itertools
import plotly.express as px
import pandas as pd

# 参数定义，根据表格
parts = [
    {"defect_rate": 0.10, "purchase_price": 2, "detection_cost": 1},  # 零配件1
    {"defect_rate": 0.10, "purchase_price": 8, "detection_cost": 1},  # 零配件2
    {"defect_rate": 0.10, "purchase_price": 12, "detection_cost": 2},  # 零配件3
    {"defect_rate": 0.10, "purchase_price": 2, "detection_cost": 1},  # 零配件4
    {"defect_rate": 0.10, "purchase_price": 8, "detection_cost": 1},  # 零配件5
    {"defect_rate": 0.10, "purchase_price": 12, "detection_cost": 2},  # 零配件6
    {"defect_rate": 0.10, "purchase_price": 8, "detection_cost": 1},  # 零配件7
    {"defect_rate": 0.10, "purchase_price": 12, "detection_cost": 2},  # 零配件8
]

semi_products = [
    {
        "defect_rate": 0.10,
        "assembly_cost": 8,
        "detection_cost": 4,
        "disassembly_cost": 6,
    },  # 半成品1
    {
        "defect_rate": 0.10,
        "assembly_cost": 8,
        "detection_cost": 4,
        "disassembly_cost": 6,
    },  # 半成品2
    {
        "defect_rate": 0.10,
        "assembly_cost": 8,
        "detection_cost": 4,
        "disassembly_cost": 6,
    },  # 半成品3
]

final_product = {
    "defect_rate": 0.10,
    "assembly_cost": 8,
    "detection_cost": 6,
    "disassembly_cost": 10,
    "market_price": 200,
    "replacement_cost": 40,
}

# 假设的零配件总数量
n_c = 100  # 零配件总数量（假设值，可以调整）

# 初始化变量
best_profit = float("-inf")  # 初始化为负无穷大
best_decision = None  # 初始化最优决策路径为空
profits = []  # 存储每种组合的收益
decisions_list = []  # 存储每种决策组合

# 穷举所有决策组合 (2^16 = 65536种)
for idx, decisions in enumerate(
    itertools.product([0, 1], repeat=16)
):  # 8个零配件检测 + 3个半成品检测 + 3个半成品拆解 + 成品检测 + 成品拆解
    x = decisions[:8]  # 零配件检测决策
    y = decisions[8:11]  # 半成品检测决策
    z = decisions[11:14]  # 半成品拆解决策
    y_final, z_final = decisions[14], decisions[15]  # 成品检测和拆解决策

    # 日志消息输出
    print(f"Processing decision {idx + 1}/{2**16}: {decisions}")

    # 计算零配件购买和检测成本
    C_c_p = sum(part["purchase_price"] * n_c for part in parts)
    C_c_d = sum(x[i] * parts[i]["detection_cost"] * n_c for i in range(8))

    # 计算半成品相关成本，确保索引不超出范围
    C_s = 0  # 初始化
    C_d_s = 0  # 初始化
    C_a_s = 0  # 初始化
    semi_indices = [(0, 1, 2), (3, 4, 5), (6, 7)]  # 正确的索引组

    for j, indices in enumerate(semi_indices):
        try:
            if len(indices) == 2:
                i, i1 = indices
                C_s += (
                    semi_products[j]["assembly_cost"]
                    * n_c
                    * (
                        (1 - x[i] * parts[i]["defect_rate"])
                        * (1 - x[i1] * parts[i1]["defect_rate"])
                    )
                )
                C_d_s += (
                    semi_products[j]["detection_cost"]
                    * y[j]
                    * (
                        n_c
                        * (1 - x[i] * parts[i]["defect_rate"])
                        * (1 - x[i1] * parts[i1]["defect_rate"])
                        - z[j] * semi_products[j]["defect_rate"] * n_c
                    )
                )
                C_a_s += (
                    semi_products[j]["disassembly_cost"]
                    * z[j]
                    * semi_products[j]["defect_rate"]
                    * n_c
                )
            else:
                i, i1, i2 = indices
                C_s += (
                    semi_products[j]["assembly_cost"]
                    * n_c
                    * (
                        (1 - x[i] * parts[i]["defect_rate"])
                        * (1 - x[i1] * parts[i1]["defect_rate"])
                        * (1 - x[i2] * parts[i2]["defect_rate"])
                    )
                )
                C_d_s += (
                    semi_products[j]["detection_cost"]
                    * y[j]
                    * (
                        n_c
                        * (1 - x[i] * parts[i]["defect_rate"])
                        * (1 - x[i1] * parts[i1]["defect_rate"])
                        * (1 - x[i2] * parts[i2]["defect_rate"])
                        - z[j] * semi_products[j]["defect_rate"] * n_c
                    )
                )
                C_a_s += (
                    semi_products[j]["disassembly_cost"]
                    * z[j]
                    * semi_products[j]["defect_rate"]
                    * n_c
                )

        except IndexError as e:
            print(f"Index error at semi-product {j+1} with indices {indices}: {e}")
            break  # 跳出当前循环

    # 继续进行只有在没有索引错误时
    else:
        # 计算成品数量
        effective_semi_products = [
            n_c * (1 - semi_products[j]["defect_rate"]) for j in range(3)
        ]
        n_f = min(effective_semi_products) * (1 - final_product["defect_rate"])

        # 计算成品相关成本
        C_d_f = (
            final_product["detection_cost"]
            * y_final
            * (n_f - z_final * final_product["defect_rate"] * n_f)
        )
        C_a_f = (
            final_product["disassembly_cost"]
            * z_final
            * final_product["defect_rate"]
            * n_f
        )
        C_s_f = final_product["assembly_cost"] * n_f
        C_r = (
            final_product["replacement_cost"]
            * y_final
            * final_product["defect_rate"]
            * n_f
        )

        # 计算利润
        S = final_product["market_price"] * n_f * (1 - final_product["defect_rate"])

        # 计算目标函数 (总成本)
        Z = C_c_p + C_c_d + C_s + C_d_s + C_a_s + C_d_f + C_a_f + C_s_f + C_r - S

        # 检查并记录有效的利润值
        if Z == float("inf") or Z == float("-inf") or Z != Z:
            print(f"Invalid Z value encountered: {Z} at decision {decisions}")
            continue

        profit = -Z  # 收益为负的目标函数值
        profits.append(profit)
        decisions_list.append(decisions)

        # 更新最优决策路径
        if profit > best_profit:
            best_profit = profit
            best_decision = decisions

# 创建 DataFrame 用于 Plotly 绘图
df = pd.DataFrame(
    {
        "Decision Index": range(len(profits)),
        "Profit": profits,
        "Decision Path": decisions_list,
    }
)

# 绘制交互式散点图
fig = px.scatter(
    df,
    x="Decision Index",
    y="Profit",
    title="Interactive Scatter Plot of Profits",
    hover_data=["Decision Path"],  # 在悬停时显示决策路径
    labels={"Decision Index": "Decision Path Index", "Profit": "Profit"},
)

# 标记最优点
fig.add_scatter(
    x=[profits.index(best_profit)],
    y=[best_profit],
    mode="markers",
    marker=dict(color="red", size=10),
    name="Optimal Decision",
)

fig.show()

# 输出最优决策路径和对应的收益
if best_decision is not None:
    print(f"最优决策路径: {best_decision} -> 最终收益: {best_profit:.2f}")
else:
    print("未找到有效的最优决策路径。")
