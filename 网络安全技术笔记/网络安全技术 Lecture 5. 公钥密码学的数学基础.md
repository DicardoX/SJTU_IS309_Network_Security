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

-------



## 3 Prime

### 3.1 重要概念

- **安全参数 **(*Security Parameter*) $\lambda$ ：
  - 衡量整个系统里各种算法的时间复杂度
- **有效算法** (*Efficient Algorithms*)：
  - 可以在多项式时间内被计算出来的算法
- **可忽略概率**(*Negligible Probability*)：
  - e.g. $f(n) = 2^{-n}$ 
  - 一种函数，攻击者的成功概率是对应安全参数的可忽略函数，则说明是可忽略概率，被认为不会发生

----



### 3.2 素数生成

- 算法流程：

  - 输入：长度 *n*，参数 *t*
  - 输出：一个 *n-bit* 的素数
  - 先取一个 *n - 1* 长度的0-1串，在前面补个1，循环 *t* 次，期间若 *p* 是素数（通过运行**素数检测**），返回；否则返回 *failure*

- *t* 的取值应该如何？

  - (*Bertrand's postulate*) 对任何 *n > 1*，*n-bit* 整数是素数的概率至少为 *1 / 3n* 

  - 在素数生成算法中，令$t = 3n^2$，则返回 *failure* 的概率：

    ​						$(1 - 1 / 3n)^t = ((1 - 1 / 3n)^{3n})^n \leq (e^{-1})^n = e^{-n}$

    为可忽略概率

- 素数检测 (*Miller-Rabin Primality Test*) (*Page. 37*)：

  - 有效算法

  - 算法流程：

    - 输入：整数 *N*，参数 $1^t$ 
    - 输出：*N* 是否为素数的判定
    - 首先，若 *N* 为偶数或[完全数](https://baike.baidu.com/item/完全数/370913?fr=aladdin)，返回"合数"
    - 通过不断除2计算：$N - 1 = 2^r u$，$r \geq 1$ and *u* 是奇数
    - 迭代 *t* 次：
    - 若满足以下，则为合数，只要又一次不满足，直接返回，说明为素数
    - $a^u \neq 1$ 可以去除
  
  <img src="/Users/dicardo/Desktop/网络安全技术笔记/cut/截屏2021-03-23 下午1.49.29.png" alt="avatar" style="zoom:50%;" />
  
  - 返回“素数”
  
- 输出分析：
  
    - 若 *N* 为奇素数，则算法总是输出“素数”
    - 若 *N* 为偶数或者素指数 (*prime power*)，则算法总是输出“合数”
    - 若 *N* 为奇合数，且不为素指数，则算法输出 “素数”（错误）的概率可以忽略（最多 $2^{-t}$）

------



## 4 密码学困难假设`Cryptographic Hadrness Assumptions`

### 4.1 大整数分解假设 `The Factoring Assumption`

- *GenModulus* 模生成算法：
  - 多项式算法
  - 输入：$1^n$（ ***n* 指示输出的长度为 *n-bit*** ）
  - 输出：*(N, p, q)*：*N = pq*，且 *p*、*q* 的均为 *n-bit* 的素数
- $Factor_{A, GenModulus}(n)$分解算法流程：
  - 运行 $GenModulus(1^n)$ 算法来获得 *(N, p, q)*，攻击者 *A* 被给予 *N*
  - 攻击者 *A* 输出 *p'*，*q'* > 1
  - 若 *N = p'q'*，输出 1；否则，输出 0
- **大整数 (素数) 分解假设的定义**：大整数 (素数) 分解相较于 *GenModulus* 模生成更难，对于所有PPT算法 *A*，都存在一个可忽略的函数 *negl* 满足：$Pr[Factor_{A, GenModulus}(n) = 1] \leq negl(n)$
- **由上述 *GenModulus* 模生成算法生成的大整数分解问题很难**

---



### 4.2 *RSA* 假设`RSA Assumption`

- *GenRSA* RSA生成算法：
  - 多项式算法
  - 输入：安全参数 $1^n$（ ***n* 指示输出的长度为 *n-bit*** ）
  - 输出：*(N, e, d)*，其中 *N* 是两个 *n-bit* 的素数，$e$ 和 $d$ 满足：
    - $(N, p, q) \leftarrow GenModulus(1^n)$ ：模生成算法
    - $\phi(N) := (p-1)(q-1)$ （**由 *N = pq* 且 *p*、*q* 为素数推导**）
    - 选择 *e* 使得：$gcd(e, \phi(N)) = 1$
    - 计算 *e* 的逆元 *d*：$ed = 1 \bmod \phi(N)$，即 $d := e^{-1} \bmod \phi(N)$ 
  - 算法失效的可能性为可忽略概率
- $RSAInv_{A, GenRSA}(n)$ 算法流程：
  - 运行 $GenRSA(1^n)$ 以获得 *(N, e, d)*，随机选择一个 $y \in Z_N^*$
  - 攻击者 *A* 被给予 *(N, e, y)*
  - 攻击者 *A* 输出 $x \in Z_N^*$
  - 若 $x^e = y \bmod N$，输出1；否则，输出0
- **RSA假设的定义**：*RSA* 问题相较于 *GenRSA* RSA生成更难，对于所有PPT算法 *A*，都存在一个可忽略的函数 *negl* 满足：$Pr[RSAInv_{A, GenRSA}(n) = 1] \leq negl(n)$
- **由上述 *GenRSA* RSA生成算法生成的RSA问题很难**
- <font color=blue>注意：</font> **若解决大整数分解问题，则可以解决 *RSA-inv* 问题** （否则由 *N* 无法求出 $\phi(N)$。若能求出，则可以假设 *x* 与 *y* 互素，进而使用欧拉定理的推论对 $x^e = y \bmod N$ 进行简化，为 $x^{e \bmod \phi(N) = d} = y \bmod N$，进而求出 *d* ，再利用平方-乘等模指数算法解决 *RSA* 问题）。因此，**大整数分解问题更难**，**大整数假设更弱（更适合作为策略的依赖）**。
- **问题**：假设 *PKE* (Public-Key Cryptography，公钥加密) 策略 *A* 的安全性依赖于 *RSA* 假设的困难性，*PKE* 策略 *B* 的安全性依赖于大整数分解假设的困难性，应该选择哪个策略？**由于大整数假设更弱，故应该选择大整数分解假设**。（？）

------



### 4.3 离散对数假设`The Discrete Logarithm Assumption`

- *GenGroup* 算法：
  - 通用、多项式、群生成算法
  - 输入：安全参数$1^n$（ ***n* 指示输出的长度为 *n-bit*** ），参数 *l(n)*
  - 输出：**循环群 *G* 的描述**，**序** *q* ($||q||=n$)，以及**生成元** $g \in G$ 
    - **循环群的描述**指示有多少个群里的元素被表示为比特串（假设每个群元素都被表示成一个独特的比特串）
    - 需要一个有效算法来计算群内的操作，以及验证一个比特串是否为群 *G* 内的元素
      - $h := g^x$：若 *x* 很大（如 *q - 1*），如何计算 *h* ？计算逆元（先模 *q*，再求逆元）
  - 具体步骤：
    - 生成一个唯一的 *n-bit* 素数 *q*
    - 生成一个 *l-bit* 素数 *p* 满足：*q | (p - 1)*（*q* 整除 *p - 1*）
    - 随机选择唯一的 $h \in Z_p^*$ 且 $h \neq 1$ 
    - 设置 $g := h^{\frac{p - 1}{q}} \bmod p$
    - 返回 *p*、*q*、*g*（*G* 是序为 *q* 的 $Z_p^*$ 的子集）
- 离散对数的定义：
  - 在循环群中，存在唯一 $x \in Z_q$，满足 $h = g^x$，则 *x* 被称为 *h* 对于 *g* 的离散对数，写作 $x = \log_gh$
- $DLog_{A, GenGroup}(n)$算法流程：
  - 运行 $GenGroup(1^n)$ 群生成算法以获得 *(G, q, g)*，选择一个唯一的元素 $h \in G$
  - 攻击者 *A* 被给予 *(G, q, g, h)*
  - 攻击者 *A* 输出 $x \in Z_q$
  - 若 $g^x = h$，输出1；否则，输出0
- **离散对数假设的定义**：离散对数问题相较于 *GenGroup* 群生成算法更难，对于所有PPT算法 *A*，都存在一个可忽略的函数 *negl* 满足：$Pr[DLog_{A, GenGroup}(n) = 1] \leq negl(n)$
- **由上述 *GenGroup* 群生成算法生成的离散对数问题很难**

--------



### 4.4 DH假设 `The Diffie-Hellman Assumption`

##### 4.4.1 CDH假设 (*Computable Diffie-Hellman Assumption*)

- 考虑如下对群生成算法 *GenGroup*，攻击者算法 *A* 和安全参数 *n* 的 **可计算DH** (*CDH*，*Computable Diffie-Hellman*) 实验：
- $CDH_{A, GenGroup}(n)$ 算法流程：
  - 运行 $GenGroup(1^n)$ 群生成算法以获得 *(G, q, g)*，选择唯一序号 $x_1, x_2 \in Z_q$，设置 $h_1 = g^{x_1}, h_2 = g^{x_2}$
  - 攻击者 *A* 被给予 $(G, q, g, h_1, h_2)$
  - 攻击者输出 $h \in G$
  - 若 $h = g^{x_1x_2}$，输出1；否则，输出0

- **CDH假设的定义**：*CDH* 问题相较于 *GenGroup* 群生成算法更难，对于所有PPT算法 *A*，都存在一个可忽略的函数 *negl* 满足：$Pr[CDH_{A, GenGroup}(n) = 1] \leq negl(n)$
- **由上述 *GenGroup* 群生成算法生成的CDH问题很难**

##### 4.4.2 DDH假设 (*Decisional Diffie-Hellman Assumption*)

- 考虑如下对群生成算法 *GenGroup*，攻击者算法 *A* 和安全参数 *n* 的 **决定性DH** (*DDH*，*Decisional Diffie-Hellman*) 实验：

- $DDH_{A, GenGroup}(n)$ 算法流程：
  - 运行 $GenGroup(1^n)$ 群生成算法以获得 *(G, q, g)*，选择唯一序号 $x_1, x_2 \in Z_q$，设置 $h_1 = g^{x_1}, h_2 = g^{x_2}$
  - 选择一个随机 *bit* $b \in \{0, 1\}$:
    - 若 $b = 0$：随机选择一个唯一的 $h \in G$
    - 若 $b = 1$：设置 $h = g^{x_1x_2}$
  - 攻击者 *A* 被给予 $(G, q, g, h_1, h_2, h)$
  - 攻击者输出一个 *bit*  $b' \in \{0, 1\}$
  - 若 $b' = b$，认为攻击者 *A* 成功。攻击者 *A* 在实验中的优势被定义为：$Adv_{A, DDH, GenGroup} = |Pr[b'=b] - 1/2|$ 

- **DDH假设的定义**：*DDH* 问题相较于 *GenGroup* 群生成算法更难，对于所有PPT算法 *A*，都存在一个可忽略的函数 *negl* 满足：$Adv_{A, DDH, GenGroup} \leq negl(n)$
- **由上述 *GenGroup* 群生成算法生成的DDH问题很难**

##### 4.4.3 两类DH假设和DLog假设的比较

- *CDH* 问题推出 *DDH* 问题，即 **CDH问题更难**，**CDH假设更弱**，**更适合作为策略的依赖**
- *DLog* 问题推出 *CDH* 问题，即 **DLog问题更难**，**DLog假设更弱**，**更适合作为策略的依赖**
- 问题难度排序：*DLog*  $\Rightarrow$  *CDH*  $\Rightarrow$  *DDH*	（降序）
- 假设强弱排序：*DLog*  $\Rightarrow$  *CDH*  $\Rightarrow$  *DDH*	（升序）

---------







