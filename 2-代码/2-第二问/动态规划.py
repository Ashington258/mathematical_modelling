from pulp import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD

# 定义参数
T = 3  # 最大迭代次数
c1, c2, cf = 4, 18, 6
d1, d2, df = 2, 3, 3
pf = 0.1
l = 6
r = 5

# 初始化问题
model = LpProblem("Optimal_Decision_Repeated", LpMinimize)

# 定义变量
x1 = {t: LpVariable(f"x1_{t}", cat="Binary") for t in range(1, T + 1)}
x2 = {t: LpVariable(f"x2_{t}", cat="Binary") for t in range(1, T + 1)}
y = {t: LpVariable(f"y_{t}", cat="Binary") for t in range(1, T + 1)}
z = {t: LpVariable(f"z_{t}", cat="Binary") for t in range(1, T + 1)}

# 目标函数
cost_terms = []
for t in range(1, T + 1):
    cost_terms.extend(
        [
            c1 + x1[t] * d1,
            c2 + x2[t] * d2,
            cf + y[t] * df + (1 - y[t]) * pf * l + z[t] * pf * r,
        ]
    )
model += lpSum(cost_terms)

# 约束条件（示例）
for t in range(1, T):
    model += z[t] <= x1[t + 1]  # 如果在 t 次拆解，则 t+1 次必须检测零配件1
    model += z[t] <= x2[t + 1]  # 如果在 t 次拆解，则 t+1 次必须检测零配件2

# 求解问题
model.solve(PULP_CBC_CMD())

# 输出结果
for v in model.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Cost = {model.objective.value()}")
