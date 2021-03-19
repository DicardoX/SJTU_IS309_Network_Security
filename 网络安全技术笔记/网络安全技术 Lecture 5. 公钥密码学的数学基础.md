# 网络安全技术 Lecture 5. 公钥密码学的数学基础



## 1. 数字定理`Number Theory`

### 1.1 模（同余）

- **整数 $a$ 与 $b$ 对模 $n$ 同余：$a \equiv b \ (\bmod n)$**
- 性质：
  - $a \equiv a \ (\bmod n)$
  - $a \equiv b \ (\bmod n)$  $\Leftrightarrow$ $b \equiv a \ (\bmod n)$  
  - $a \equiv b \ (\bmod n)$ + $b \equiv c \ (\bmod n)$  $\Rightarrow$  $a \equiv c \ (\bmod n)$  
  - $a \equiv b \ (\bmod n)$  $\Leftrightarrow$  $a \bmod n = b \bmod n$ 
  - **Reduction**：$(a + b) \bmod n = (a \bmod n + b \bmod n) \bmod n$  
    - <font color=blue>注意</font>：对减法/乘法同样适用
  - 若 $(a + b) \equiv (a + c) \ (\bmod n)$，则 $b \equiv c \ (\bmod n)$ 
  - 若 $ab \equiv ac \ (\bmod n)$，则仅当 $a$ 与 $n$ 互素时，才有 $b \equiv c \ (\bmod n)$ 
- **模逆元**：$ab \bmod n = 1$ $\Rightarrow$  $a$ 是 $b$ 模 $n$ 的逆元
  - $a$ 可以表示为 $b^{-1} \bmod n$ 
  - **定理：存在 $b \bmod n$ 的逆元  $\Leftrightarrow$  $b$ 和 $n$ 互素 **

-------

### 1.2 素数分解`Prime Factorization`

- 任何正整数 $a$ 可以被唯一地分解为：$a = p_1^{\alpha_1} p_2^{\alpha_2}... p_t^{\alpha_t}$ ，其中 $p_1 > p_2 > ... > p_t$ 为素数，$\alpha_i$ 为自然数
- **最大公约数** (GCD)：
  - 若 $GCD(a, b) = 1$，则称 $a$ 和 $b$ 为互素
  - **如何计算GCD？** 简单方法：分别对 $a$ 和 $b$ 进行素数分解，再求最大公共部分（问题：大整数难以分解）

----------

### 1.3 欧几里得算法 `Euclidean Algorithm` 

- 用来更快速地解决GCD问题

<img src="./cut/截屏2021-03-16 下午9.00.42.png" alt="avatar " style="zoom:80%;" />

- **欧几里得定理**：$gcd(a, b) = gcd(b, a \bmod b)$

----------

### 1.4 扩展欧几里得算法`Extented Euclidean Algorithm`

- 用来解决**整数x、y的求值问题：$ax + by = gcd(a, b)$**

  **欧几里得算法的逆过程**

<img src="./cut/截屏2021-03-17 上午8.09.50.png" alt="avatar " style="zoom:80%;" />

- 因此，$gcd(911, 999) = 1 = -193 \times 911 + 176 \times 999$

- **利用扩展欧几里得算法求模逆元**：

  <img src="./cut/截屏2021-03-17 上午8.21.45.png" alt="avatar" style="zoom:80%;" />

--------

### 1.5 欧拉 $\phi$ 函数 `The Euler phi Function`

- 对于 $n \geq 1$，$\phi(n)$ 表示处于区间 $[1, n]$ 内且与 $n$ 互素的整数的数量
  - 性质一（**可乘性** ）：若 $gcd(m, n)=1$，则 $\phi(mn)=\phi(m) \times \phi(n)$ 
  - 性质二（**素数底整数幂性**）：对于一个素数 $p$ 和一个整数 $e \geq 1$，$\phi(p^e) = p^{e-1}(p-1)$  
  - 性质三（**一般分解性质**）：令 $n=p_1^{e_1}p_2^{e_2}...p_k^{e_k}$，其中 $p_1, p_2, ...., pk$ 是素数且 $e_i$ 是正整数，则： $\phi(n)=n(1-1/p_1)(1-1/p_2)...(1-1/p_k)$

-----------

### 1.6 费马小定理`Fermat's Little Theorem`

- **费马小定理**：令 $p$ 为一个素数，任何不能被 $p$ 整除的整数 $a$ 满足：$a^{p-1} \equiv 1(\bmod p)$.
  - **推论**：若 $a$ 不能被 $p$ 整除且 $n \equiv m \ (\bmod p-1)$，则 $a^n \equiv a^m \ (\bmod p)$ 
  - 推论（**欧拉定理**）：令 $n$ 为正数，则对任何与 $n$ 互素的整数 $a$ 都有：$a^{\phi(n)} \equiv 1 \ (\bmod n)$ 
  - $\star$ **推论**：对整数 $a$ 和正整数 $k$ ，$n$，若 $a$ 和 $n$ 互素，则：$a^k \bmod n = a^{k \bmod \phi(n)} \bmod n$ 

--------

### 1.7 模指数`Modular Exponentiation`

- $a^e \bmod n$ 被定义为 $a$ 的 $e$ 次连乘对 $n$ 的模
- 方法一：**重复模乘法**（使用**1.1**节中的**Reduction**性质）

<img src="./cut/截屏2021-03-17 下午4.44.27.png" alt="avatar" style="zoom:60%;" />

- 方法二：**平方-乘算法**：**将大指数按平方关系逐层拆解，再利用Reduction性质逐层求解，最后将										结果相乘再取模**

<img src="./cut/截屏2021-03-17 下午4.47.59.png" alt="avatar" style="zoom:60%;" />

​		平方-乘算法的伪代码（基于 $e$ 的二进制表示）：

<img src="./cut/截屏2021-03-17 下午4.57.35.png" alt="avatar" style="zoom:50%;" />

-----------



## 2. 群理论`Group Theory`

### 2.1 群的定义

- 令 $G$ 为非空集合，$\circ$ 为二元运算符，集合 $G$ 上的二元运算 $\circ$ 从 $G \times G$ 映射到 $G$ 
- 当满足以下条件时，$(G, \circ)$ 是群：
  - **封闭性 (closed)**：对于任何 $a, b \in G$，$a \circ b \in G$
  - **结合律 (associative)**：对任何 $a, b, c \in G$，$(a \circ b) \circ c = a \circ (b \circ c)$ 
  - **存在单位元 (identity element)**：$G$ 中存在一个单位元 $e$ ，满足对任何 $a \in G$，$a \circ e = e \circ a = a$
  - **存在逆元 (inverse)**：对任意 $a \in G$，都存在 $a^{-1} \in G$ 满足 $a \circ a^{-1} = a^{-1} \circ a = e$（**逆元可以为自己**）

- **阿贝尔群 (Abelian Group)**：若 $\circ$ 也满足交换律，即对任何 $a, b \in G$，$a \circ b = b \circ a$，则 $(G, \circ)$ 被称为阿贝尔群
- **乘法群的性质**：$Z_n = \{0, 1, 2, 3, ..., n-1\}$
  - 性质：**仅当 $n$ 是素数时，$Z_n \backslash \{0\}$ 构成群**（模 $n$）
  - 推广：**对任何正整数 $n$ ，集合 $Z_n^* = \{a \in Z_n | gcd(a, n) = 1\}$构成群**

--------

### 2.2 循环群`Cyclic Groups`

- 定义：$(G, \circ)$ 是循环群的条件是：**存在元素 $g \in G$满足对任何 $a \in G$，都存在整数 $i$ 使得 $a = g^i \ (\bmod n)$**。 $g$ 被称为 $G$ 的**生成元**或**基本元**，也被称为 $n$ 的**原根**
- $Z_n^*$ 至少含有一个生成元  $\Leftrightarrow$  当且仅当 $n = 2, 4, p^k, 2p^k$，其中 $p$ 是一个奇素数且 $k \geq 1$ 
- 性质：令 $G$ 为循环群，**秩 $m$ 代表 $|G| = m$**，$g \in G$ 是生成元，则：
  - $g^m = e$，$e$ 为单位元
  - 对任何非负整数 $x, y$，有：$g^{xy} = g^{yx}$
  - 对任何非负整数 $x$ 和元素 $h \in G$，有 $h^x = h^{x \bmod m}$















