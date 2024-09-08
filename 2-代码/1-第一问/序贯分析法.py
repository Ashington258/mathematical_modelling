import math
import numpy as np

# 参数设置
p0 = 0.10  # 标称次品率
p1 = 0.15  # 假设的较高次品率
alpha = 0.05  # 显著性水平
beta = 0.10  # 检验功效

# 计算对数界限
A = (1 - beta) / alpha
B = beta / (1 - alpha)
logA = math.log(A)
logB = math.log(B)

# 计算对数似然比的系数
log_p1_p0 = math.log(p1 / p0)
log_1_p1_1_p0 = math.log((1 - p1) / (1 - p0))


# 模拟抽样检测
def sequential_probability_ratio_test(samples):
    S_n = 0  # 累积对数似然比
    for i, sample in enumerate(samples):
        if sample == 1:  # 次品
            S_n += log_p1_p0
        else:  # 合格品
            S_n += log_1_p1_1_p0

        print(
            f"Sample {i+1}: {'Defective' if sample == 1 else 'Non-defective'}, S_n = {S_n:.4f}"
        )

        if S_n >= logA:
            print("Reject the batch (次品率超过标称值，拒收零配件)")
            return False
        elif S_n <= logB:
            print("Accept the batch (次品率不超过标称值，接收零配件)")
            return True

    print("Continue sampling (继续抽样)")
    return None


# 示例数据（实际应从实际检测中获得）
# 1 表示次品，0 表示合格品
samples = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0]

# 运行序贯概率比检验
result = sequential_probability_ratio_test(samples)

if result is None:
    print("需要更多数据以作出最终决策。")
