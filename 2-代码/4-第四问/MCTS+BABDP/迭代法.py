'''
Author: Ashington ashington258@proton.me
Date: 2024-09-08 18:23:07
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-08 18:23:13
FilePath: \mathematical_modelling\2-代码\4-第四问\MCTS+BABDP\迭代法.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import itertools
import plotly.express as px


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
    import pandas as pd

    df = pd.DataFrame(paths, columns=[f"decision_{i+1}" for i in range(16)])
    df["reward"] = rewards
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


# 初始状态
initial_state = BAMDPState([], parts, semi_products, final_product, n_c, prior_beliefs)

# 使用穷举法评估所有路径
results = evaluate_all_paths(initial_state)

# 转换为DataFrame以便可视化
df = paths_to_dataframe(results)

# 绘制相关性散点图
visualize_results(df)
