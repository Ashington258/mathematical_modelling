"""
Author: Ashington ashington258@proton.me
Date: 2024-09-08 02:59:17
LastEditors: Ashington ashington258@proton.me
LastEditTime: 2024-09-08 02:59:23
FilePath: \mathematical_modelling\2-代码\3-第三问\MDP+动态规划\cupy_test\cupy_test.py
Description: 请填写简介
联系方式:921488837@qq.com
Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
"""

import cupy as cp

# 测试 CuPy 是否正常工作
a = cp.array([1, 2, 3])
b = cp.array([4, 5, 6])
print(cp.dot(a, b))
