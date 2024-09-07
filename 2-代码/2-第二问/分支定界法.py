import json
from queue import PriorityQueue


# 从JSON文件读取数据
def load_data_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


# 从指定情形中获取参数
def get_parameters(data, case_name):
    for case in data["cases"]:
        if case["name"] == case_name:
            return case
    raise ValueError(f"Case '{case_name}' not found in the data.")


# 计算成本函数
def calculate_cost(c_p, c_d, c_d_f, c_a_f, c_s, p_c, p_f, s_f, n_c, x, y, z):
    n_f = n_c * (1 - p_c[0] * x[0]) * (1 - p_c[1] * x[1])
    C_p_c = n_c * sum(c_p[i] for i in range(2))
    C_d_c = n_c * sum(x[i] * c_d[i] for i in range(2))
    C_d_f = c_d_f * y * n_f
    C_a_f = c_a_f * p_f * z * n_f
    C_s = c_s * p_f * y * n_f
    S = s_f * n_f
    Z = C_p_c + C_d_c + (C_d_f + C_a_f + C_s - S)
    return Z


# 分支定界法寻找最优路径
def branch_and_bound(params):
    # 读取参数
    c_p = params["c_p"]
    c_d = params["c_d"]
    c_d_f = params["c_d_f"]
    c_a_f = params["c_a_f"]
    c_s = params["c_s"]
    p_c = params["p_c"]
    p_f = params["p_f"]
    s_f = params["s_f"]
    n_c = params["n_c"]

    # 优先队列用于存储待处理的节点，按当前最小成本优先
    pq = PriorityQueue()
    pq.put((0, [0, 0], 0, 0))  # 初始节点 (估计成本, x, y, z)

    # 初始化最优路径和最小成本
    best_path = None
    min_cost = float("inf")
    iteration = 0

    while not pq.empty():
        iteration += 1
        # 从队列中取出当前最优的节点
        current_cost, x, y, z = pq.get()
        print(
            f"Iteration {iteration}: Current node -> x={x}, y={y}, z={z}, Estimated Cost = {current_cost}"
        )

        # 如果当前节点的成本已经大于或等于已知最小成本，剪枝
        if current_cost >= min_cost:
            print(
                f"Iteration {iteration}: Node pruned as cost {current_cost} >= {min_cost}"
            )
            continue

        # 计算当前节点的实际成本
        actual_cost = calculate_cost(
            c_p, c_d, c_d_f, c_a_f, c_s, p_c, p_f, s_f, n_c, x, y, z
        )
        print(f"Iteration {iteration}: Actual Cost = {actual_cost}")

        # 如果是一个完整的解，且比当前最优解更好，更新最优解
        if len(x) == 2 and isinstance(y, int) and isinstance(z, int):
            if actual_cost < min_cost:
                min_cost = actual_cost
                best_path = (x[0], x[1], y, z)
                print(
                    f"Iteration {iteration}: Found new best path -> x1={x[0]}, x2={x[1]}, y={y}, z={z}, Cost = {min_cost}"
                )
            continue

        # 分支扩展：对未确定的变量进行分支
        if len(x) < 2:  # 分支 x1, x2
            pq.put((actual_cost, x + [0], y, z))
            pq.put((actual_cost, x + [1], y, z))
            print(
                f"Iteration {iteration}: Branching on x -> New nodes added for x={x + [0]} and x={x + [1]}"
            )
        elif y is None:  # 分支 y
            pq.put((actual_cost, x, 0, z))
            pq.put((actual_cost, x, 1, z))
            print(
                f"Iteration {iteration}: Branching on y -> New nodes added for y=0 and y=1"
            )
        elif z is None:  # 分支 z
            pq.put((actual_cost, x, y, 0))
            pq.put((actual_cost, x, y, 1))
            print(
                f"Iteration {iteration}: Branching on z -> New nodes added for z=0 and z=1"
            )

    # 输出最优决策路径和最小成本
    print(
        f"最优决策路径: x1={best_path[0]}, x2={best_path[1]}, y={best_path[2]}, z={best_path[3]} => 最小总成本: {min_cost}"
    )


# 主函数
if __name__ == "__main__":
    # 从JSON文件中读取数据
    data = load_data_from_json(
        "F:/1.Project/2.Ongoing_Projects/mathematical_modelling/2-代码/2-第二问/data.json"
    )  # 替换为实际JSON文件路径

    # 用户选择使用的情形
    selected_case = "Case 1"  # 用户可以修改此处选择不同的情形

    # 获取选定情形的参数
    params = get_parameters(data, selected_case)

    # 通过分支定界法寻找最优决策路径
    branch_and_bound(params)
