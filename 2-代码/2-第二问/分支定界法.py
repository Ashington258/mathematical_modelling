import math

# 参数
c_p = [4, 18]  # 零配件购买成本
c_d = [2, 3]  # 零配件检测成本
c_d_f = 3  # 成品检测成本
c_a_f = 5  # 成品拆解成本
c_s = 6  # 调换成本
p_c = [0.1, 0.1]  # 零配件次品率
p_f = 0.1  # 成品次品率
s_f = 56  # 成品售价
n_c = 1  # 零配件数量


# 成本函数
def compute_cost(x, y, z):
    n_f = n_c * (1 - p_c[0] * x[0]) * (1 - p_c[1] * x[1])
    C_p_c = n_c * sum(c_p[i] for i in range(2))
    C_d_c = n_c * sum(x[i] * c_d[i] for i in range(2))
    C_d_f = c_d_f * y * n_f
    C_a_f = c_a_f * p_f * z * n_f
    C_s = c_s * p_f * y * n_f
    S = s_f * n_f
    Z = C_p_c + C_d_c + (C_d_f + C_a_f + C_s - S)
    return Z


# 初始化最优解和待处理列表
best_cost = float("inf")
best_path = None
nodes = [([0, 0], 0, 0)]  # 初始化节点列表 (x, y, z)

# 分支定界法
while nodes:
    x, y, z = nodes.pop(0)  # 取出一个节点进行处理
    # 计算当前节点的成本
    current_cost = compute_cost(x, y, z)

    # 更新最优解
    if current_cost < best_cost:
        best_cost = current_cost
        best_path = (x[0], x[1], y, z)

    # 如果该路径已经全部决策（x、y、z 全是 0 或 1），不再分裂
    if len(nodes) < 2:
        # 分裂节点
        for i in range(4):
            if i < 2:  # 修改 x 的决策变量
                new_x = x[:]
                new_x[i] = 1 - x[i]
                nodes.append((new_x, y, z))
            elif i == 2:  # 修改 y 的决策变量
                new_y = 1 - y
                nodes.append((x, new_y, z))
            elif i == 3:  # 修改 z 的决策变量
                new_z = 1 - z
                nodes.append((x, y, new_z))

# 输出最优解
print(
    f"最优决策路径: x1={best_path[0]}, x2={best_path[1]}, y={best_path[2]}, z={best_path[3]} => 最小总成本: {best_cost}"
)
