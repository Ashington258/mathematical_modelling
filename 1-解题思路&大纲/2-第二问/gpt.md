请根据我建立的模型，对目标函数设计算法进行求解


```markdown

## 目标函数：

### 简化的目标函数

1. **零配件购买成本**：
   \[
   C^c_p = n^c \sum_{i=1}^{2} c_{pi}^c
   \]
   
2. **零配件检测成本**：
   \[
   C^c_d = n^c \sum_{i=1}^{2} x_i c_{di}^c
   \]
   
3. **成品检测成本**：
   \[
   C_d^f = c_d^f y \left( n^c - x p^c n^c \right) = c_d^f y n^c \left( 1 - x p^c \right)
   \]
   
4. **成品拆解成本**：
   \[
   C_a^f = c_a^f p^f z n^f = c_a^f p^f z n^c \left( 1 - x p^c \right)
   \]
   
5. **调换成本**：
   \[
   C_s = c_s p^f y n^c \left( 1 - x p^c \right)
   \]
   
6. **成品数量**：
   \[
   n^f = n^c (1 - x p^c)
   \]
   
7. **利润**：
   \[
   S = s^f n^c (1 - x p^c)
   \]
   
**假设**$n_1^c = n_2^c =...= n^c$
### 总成本目标函数

根据以上各项成本的更新公式，更新后的总成本目标函数为：

\[
\min Z = n^c \left( \sum_{i=1}^{2} c_{pi}^c + \sum_{i=1}^{2} x_i c_{di}^c \right) + n^c \left( c_d^f y + c_a^f p^f z + c_s p^f y - s^f \right) \left( 1 - x p^c \right)
\]


## 变量声明

**参数说明**
| 符号                             | 说明             |
| :------------------------------- | :--------------- |
| $c^c_{p1},c^c_{p2},...,c^c_{pi}$ | 零配件的单价     |
| $c^c_{d1},c^c_{d2},...,c^c_{di}$ | 零配件的检测成本 |
| $c^f_d$                          | 成品检测成本     |
| $c^f_a$                          | 成品拆解成本     |
| $c_s$                            | 调换成本         |
| $p^c_1,p^c_2,...,p^c_i$          | 零配件的次品率   |
| $p^f$                            | 成品的次品率     |
| $s^f$                            | 成品售价         |
| $n_1^c,n_2^c,...,n_i^c$          | 零配件的数量     |
| $n^f$                            | 成品的数量       |

**决策变量**

| 符号              | 说明                 |
| :---------------- | :------------------- |
| $x_1,x_2,...,x_i$ | 是否对零配件进行检测 |
| $y$               | 是否对成品进行检测   |
| $z$               | 是否对成品进行拆解   |
```


