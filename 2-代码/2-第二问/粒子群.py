import numpy as np
from pyswarm import pso

# 参数定义（以情况1为例）
c_p1, c_p2 = 4, 18  # 零配件的购买单价
c_d1, c_d2 = 2, 3  # 零配件的检测成本
c_d_f = 3  # 成品检测成本
c_a_f = 5  # 成品拆解成本
c_s = 6  # 调换成本
p_c1, p_c2 = 0.1, 0.1  # 零配件的次品率
p_f = 0.1  # 成品的次品率
s_f = 56  # 成品售价
n_c = 100  # 零配件的数量

# 决策变量的界定（0或1）
lb = [0, 0, 0, 0]  # 决策变量下界
ub = [1, 1, 1, 1]  # 决策变量上界


# 目标函数
def cost_function(x):
    x1, x2, y, z = (
        int(round(x[0])),
        int(round(x[1])),
        int(round(x[2])),
        int(round(x[3])),
    )

    # 零配件购买成本
    C_cp = n_c * (c_p1 + c_p2)

    # 零配件检测成本
    C_cd = n_c * (x1 * c_d1 + x2 * c_d2)

    # 成品数量 n^f
    n_f = n_c * (1 - (x1 * p_c1 + x2 * p_c2))

    # 成品检测成本
    C_df = c_d_f * y * n_f

    # 成品拆解成本
    C_af = c_a_f * p_f * z * n_f

    # 调换成本
    C_s = c_s * p_f * y * n_f

    # 成品利润
    S = s_f * n_f

    # 总成本目标函数
    Z = C_cp + C_cd + (C_df + C_af + C_s - S)
    return Z


# 粒子群优化求解 (确保搜索维度为4)
best_cost, best_pos = pso(
    cost_function, lb, ub, swarmsize=50, maxiter=100, phip=0.5, phig=0.5, omega=0.5
)

# 检查best_pos的类型
try:
    print(f"best_pos: {best_pos}, 类型: {type(best_pos)}")  # 打印best_pos及其类型

    if isinstance(best_pos, (list, np.ndarray)):
        x1_opt, x2_opt, y_opt, z_opt = [int(round(i)) for i in best_pos]
        print(f"最优解：x1 = {x1_opt}, x2 = {x2_opt}, y = {y_opt}, z = {z_opt}")
    else:
        print("Error: best_pos is not iterable.")

    print(f"最小化总成本：{best_cost}")

except TypeError as e:
    print(f"Error: {e}")
    print(f"best_pos返回值：{best_pos}")
