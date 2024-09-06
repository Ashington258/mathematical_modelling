from pulp import LpProblem, LpMinimize, LpVariable, lpSum

# 定义问题
model = LpProblem("Optimal_Decision", LpMinimize)

# 定义决策变量
x1 = LpVariable("x1", cat="Binary")
x2 = LpVariable("x2", cat="Binary")
y = LpVariable("y", cat="Binary")
z = LpVariable("z", cat="Binary")

# 参数（示例值）
c1, c2, cf = 4, 18, 6
d1, d2, df = 2, 3, 3
pf = 0.1
l = 6
r = 5

# 目标函数
model += (c1 + x1 * d1) + (c2 + x2 * d2) + cf + y * df + (1 - y) * pf * l + z * pf * r

# 解决问题
model.solve()

# 输出结果
for v in model.variables():
    print(f"{v.name} = {v.varValue}")

print(f"Total Cost = {model.objective.value()}")
