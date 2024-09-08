 from scipy.stats import binom

# 设置参数
p_nominal = 0.10  # 标称次品率
alpha = 0.05      # 第一类错误的风险，用于95%置信度拒收
beta = 0.10       # 第二类错误的风险，用于90%置信度接收

# 初始化变量
n_95 = 20  # 从较高的样本量开始以寻找更稳健的结果
n_90 = 20

# 计算95%置信度拒收的最小n和对应的k
while True:
    k_95 = binom.ppf(1 - alpha, n_95, p_nominal)
    if binom.sf(k_95, n_95, p_nominal) <= alpha:
        break
    n_95 += 1

# 计算90%置信度接收的最小n和对应的k
while True:
    k_90 = binom.ppf(beta, n_90, p_nominal)
    if binom.cdf(k_90, n_90, p_nominal) >= 1 - beta:
        break
    n_90 += 1

n_95, int(k_95), n_90, int(k_90)
