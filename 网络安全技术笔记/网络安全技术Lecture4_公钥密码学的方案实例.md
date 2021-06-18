# 网络安全技术 Lecture 4 公钥密码学的方案实例

## 1 公钥加密策略

### 1.1 *RSA*加密策略

-  *GenRSA* 算法：
  
  - 输入：安全参数 $1^n$（ ***n* 指示输出的长度为 *n-bit*** ）
  - 输出：*(N, e, d)*，其中 *N* 是两个 *n-bit* 的素数，$e$ 和 $d$ 满足：
    - $(N, p, q) \leftarrow GenModulus(1^n)$ ：模生成算法
    - $\phi(N) := (p-1)(q-1)$
    - 选择 *e* 使得：$gcd(e, \phi(N)) = 1$
    - 计算 *e* 的逆元 *d*：$ed = 1 \bmod \phi(N)$，即 $d := e^{-1} \bmod \phi(N)$ 
  
- *RSA* 加密策略：**确定性加密策略**，因此一定不满足 *CPA* 安全

  - $KeyGen(1^\lambda) \rightarrow (pk, \ sk)$：
    - 输入 $1^\lambda$，算法运行 $GenRSA(1^\lambda)$ 算法获得 *(N, e, d)*，输出**公钥** *pk := (N, e)* 和**私钥** *sk := (N, d)*
  - $Enc(pk, \ m) \rightarrow c$：
    - 输入公钥 *pk = (N, e)* 和明文 $m \in Z^*_N$，输出密文 $c := m^e \bmod N$
  - $Dec(sk, \ c) \rightarrow m$：
    - 输入私钥 *sk = (N, d)* 和密文 $c \in Z^*_N$，输出明文 $m := c^d \bmod N$

  **正确性**：对任何 $(pk, \ sk) \leftarrow KeyGen(1^\lambda)$，任意 $m \in Z^*_N$，我们有： $Dec(sk, \ Enc(pk, \ m)) = Dec(sk, \, m^e \bmod N) =  (m^e \bmod N)^d \bmod N = m^{ed} \bmod N \\ = m^{ed \bmod \phi(N)} \bmod N = m \bmod N$ 

  

- 注意：已知公钥 *(N, e)*，无法通过扩展欧几里得算法计算私钥 *(N, d)*，原因是已知 *N* 无法求出 $\phi(N)$ ，由大整数分解困难假设可证

- 可不可以随便挑 $m \in [0, n-1]$ 就使用RSA加密？

  - 可以，**基于大整数分解难题**，碰巧取到 $m$ 与 *N* 不互素的概率为可忽略，因为 $N$ 是两个大素数的积
  
-  ***RSA* 加密策略不满足 *CPA* 安全**：

    -  由于公钥加密且为确定性加密算法，当被攻击者将挑战密文 $c^*$ 提供给攻击者 $A$ 时，攻击者 $A$ 可以利用已经被公开的确定性加密算法 $c = m^e \bmod N$，公开的公钥 $(N, e)$，分别选择之前向被攻击者提供的两个长度不同的明文 $m_1^*$ 和 $m_2^*$ 进行自我学习，而确定性加密算法意味着相同的明文输入一定有相同的密文输出，得到与挑战密文相同的即对应了被攻击者选择的 $b$

-  ***RSA* 加密策略不满足 *CCA* 安全**：

    -  由公钥加密的性质，攻击者 $A$ 首先获得一对被加密的消息和密文：$c = m^e \bmod N$，而这意味着在确定性的解密算法中，$m = c^d \bmod N$

        ~~选择密文 $2c$，询问解码机 $Dec(sk, c)$ 得到 $m' = (2c)^d \bmod N$，注意到由于 *RSA* 方案中 $M = Z^*_N$ 是乘法群，因此 $c$ 也一定位于该乘法群中（且 $2$ 几乎一定与 $N$ 互素，因此 $2$ 位于该乘法群中），于是 $2c$ 也位于该乘法群中。因此有：$m' / m = 2^d \bmod N$，即 $d = \log_2(m' / m \bmod N)$，即求得该 *RSA* 加密方案的私钥。~~

---------



### 1.2 *EI Gamal* 加密策略

- *GenGroup* 算法：
  
  - 通用、多项式、群生成算法
  - 输入：安全参数$1^n$（ ***n* 指示输出的长度为 *n-bit*** ），参数 *l(n)*
  - 输出：**循环群 *G* 的描述**，**序** *q* ($||q||=n$)，以及**生成元** $g \in G$ 
  
- *EI Gamal* 加密策略：**概率性加密策略**

  - $KeyGen(1^\lambda) \rightarrow (pk, \ sk)$：
    - 输入 $1^\lambda$，算法运行 $GenGroup(1^\lambda)$ 算法获得 *(G, q, g)*，然后随机选择一个 $x \in Z_q$，计算 $h := g^x$，输出**公钥** *pk := (G, q, g, h)* 和**私钥** *sk := (G, q, g, x)*
  - $Enc(pk, \ m) \rightarrow c$：
    - 输入公钥 *pk = (G, q, g, h)* 和明文 $m \in G$，算法随机选择唯一的 $y \in Z_q$，输出密文 $(g^y, m ·h^y)$
  - $Dec(sk, \ c) \rightarrow m$：
    - 输入私钥 *sk = (G, q, g, x)* 和密文 $c = (c_1, c_2) \in G^2$，输出明文 $m := c_2 / c_1^x$

  **正确性**：对任何 $(pk, \ sk) \leftarrow KeyGen(1^\lambda)$，任意 $m \in G$，我们有：

  $Dec(sk, Enc(pk, m)) = Dec(sk, (g^y, m · h^y)) = m · h^y / (g^y)^x =  m · (h / g^x) ^y = m$

- **安全性证明**：

  - 定理：**若与 *GenGroup* 算法相关的 *DDH* 问题是困难的，那么 *El Gamal* 加密满足 *CPA* 不可区分性，即 *CPA* 安全**。

    **证明**：(主要思路**反证法**，若 *EI Gamal* 加密不安全，那么 *DDH* 困难问题假设不成立)

    记 *EI Gamal* 加密方案为 $\Pi$，假设 $\Pi$ 不满足 *CPA* 安全，那么存在一个**概率多项式时间 *PPT* 算法 *A***，对 $\Pi$ 环境下的 $(pk, (c_1, c_2))$，以可观的概率 $\varepsilon(\lambda)$ 赢得挑战，即 $Adv_{\Pi, A}^{CPA} =| Pr[b' = b] - 1 / 2| = |\varepsilon(\lambda) - 1/2| > negl(\lambda)$，我们可以构造一个 *PPT* 算法 *B* 来以不可忽略的概率解决与 *GenGroup* 相关的 *DDH* 问题。

    现在再引入一个加密方案 $\hat\Pi$：

    - 密钥生成算法与 *EI Gamal* 加密保持一致
    - $Enc(pk, \ m) \rightarrow c$：
      - 输入公钥 *pk = (G, q, g, h)* 和明文 $m \in G$，算法随机选择唯一的 $y, z \in Z_q$，输出密文 $(g^y, m ·g^z)$
    - $Dec(sk, \ c) \rightarrow m$：无解密算法

    **由于 $\Pi$ 中的密文 *c* 等价于完全随机挑选**，与 *m* 无关，因此攻击者 *A* 赢得该 $\hat\Pi$ 对应的 *CPA* 挑战的优势为：

    $Adv_{\Pi, A}^{CPA} = | Pr[b' = b] - 1 / 2| = 0$

    因此，**任意 *PPT* 算法 *A* 赢得该 $\hat\Pi$ 对应的 *CPA* 挑战的概率均为0.5**。

    **由先前的定义可知：$\varepsilon(\lambda)$ 与 1/2 明显不同，即 $|\varepsilon(\lambda) - 1/2| > negl(\lambda)$** 。**在此基础上，我们可以构造一个判别器，来解决 *DDH* 问题**。

    **判别器 *D* 算法**如下（**结合EI Gamal的思想基于DDH算法进行构造**）：

    - 输入 $(G, q, g, g_1, g_2, g_3)$，设置公钥 $pk = (G, q, g, g_1)$，运行 *A (pk)* 得到两个明文 $m_0$，$m_1$（原因是CPA可以由攻击者选择明文），随机挑选一个 *bit* $b \leftarrow \{0, 1\}$，设置 $c_1 := g_2$ 和 $c_2 := m_b · g_3$
    - 将 $c = (c_1, c_2)$ 交给攻击者 *A*，得到一个 *bit* *b'*
    - 若 *b = b'*，则输出1；否则，输出0

    注意到，**判别器输出1的概率即为攻击者 *A* 赢得 $\hat\Pi$ 的 *CPA* 挑战的概率** ，即：

    $Pr[D(G, q, g, g_1, g_2, g_3) = 1] = Pr[b' = b]$

    此时**根据 $g_3$ 取值的不同，可以分为两种情况**：

    - $g_1 = g^x$，$g_2 = g^y$，$g_3 = g^z$，则：$Pr[D(G, q, g, g^x, g^y, g^z) = 1] = Pr[b' = b] = 1 / 2$

      （**因为此时满足 $\hat\Pi$ 中的密文形式，即： $(g_2, m_b · g_3) = (g^y, m_b · g^z)$**）

    - $g_1 = g^x$，$g_2 = g^y$，$g_3 = g^{xy}$，则：$Pr[D(G, q, g, g^x, g^y, g^{xy}) = 1] = Pr[b' = b] = \varepsilon(\lambda)$ 

      （**因为此时满足 $\Pi$ 中的密文形式，即： $(g_2, m · g_3) = (g^y, m_b · h^y)$， 其中 $h = g^x$**）

    因此有：

    $| Pr[D(G, q, g, g^x, g^y, g^z) = 1] - Pr[D(G, q, g, g^x, g^y, g^{xy}) = 1]| = | \varepsilon(\lambda) - 1/2 | > negl(\lambda)$ 

    **与 *DDH* 困难假设相矛盾，即证**。（上述不等式的含义即对应了 *DDH* 算法中的随机选取或指定 $h = g^{x_1x_2}$）

- #### 对照 PKE 的 CCA 模型，说明 El Gamal 加密方案不是 CCA 安全的。

  **Answer**：

  记 *EI Gamal* 加密方案为 $\Pi$，攻击者 *A*，我们证明 $\Pi$ 在 *A* 下不满足 *CCA* 安全。攻击者 *A* 的算法如下：

  在 *CCA* 的挑战阶段，攻击者 *A* 选择长度相同的明文：$m^*_0 = x$，$m^*_1 = y$，并将明文对 $(m^*_0, \ m^*_1)$ 发送给被攻击者，被攻击者选择一个特殊的比特 $b \in \{0, 1\}$ ，以此为依据选择使用哪一个明文，并计算 $c^* \leftarrow Enc(pk, m_b^*)$ ，将挑战密文 $c^* = (c_1, \ c_2)$ 提供给攻击者 $A$ 。

  攻击者 *A* 随机选择一个唯一的 $z \in Z_q$，将挑战密文 $c^*$ 的 $c_2$ 乘以 *z*，得到一个**新的密文** $c_{new} = (c_1, c_2 · z)$，并用该密文询问解码机 *decryption oracle*，将得到的结果除以 *z*，则要么是 $m^*_0$ 要么是 $m^*_1$，对应了在挑战阶段被攻击者选择加密的明文。

  在上述算法下，攻击者 *A* 会以不可忽略的优势赢得基于 *EI Gamal* 加密方案下的 *CCA* 挑战，即 $\Pi$ 在 *A* 下不满足 *CCA* 安全。
  
  **核心思想是针对挑战密文 $c^*$ 中不会在解密时进行 $x$ 次方操作的 $c_2$ 进行常数修改，用这个修改后的密文 $c'^*$ 来访问解码机，获取对应的明文 $m'^*$，再直接除该常数即可得到挑战密文对应的明文**。   

------



## 2 数字签名策略

- 注意！**数字签名中的消息相当于是公开状态**，因为虽然使用了私钥签名，但**任何人都可以使用公钥认证来解出明文**

### 2.1 *RSA* 签名

- *RSA* 签名策略：
  
  - $KeyGen(1^\lambda) \rightarrow (pk, \ sk)$
    - 输入 $1^\lambda$，算法运行 $GenRSA(1^\lambda)$ 算法获得 *(N, e, d)*，输出**公钥** *pk := (N, e)* 和**私钥** *sk := (N, d)*
  - $Sign(sk, \ m) \rightarrow \sigma$
    - 输入**私钥** *sk = (N, d)* 和**消息** $m \in Z^*_N$，算法输出**签名** $\sigma := m^d \bmod N$ 
  - $Verify(pk, \ m, \ \sigma) \rightarrow 1 / 0$ 
    - 输入**公钥** $pk = (N, e)$，**消息** $m \in Z^*_N$ 和**签名** $\sigma \in Z^*_N$，若 $m = \sigma^e \bmod N$，算法输出1；否则，输出0
  
  **正确性**：对任何 $(pk, \ sk) \leftarrow KeyGen(1^\lambda)$，任意 $m \in Z^*_N$，我们有： $Verify(pk, \ m,  \ Sign(sk, \ m)) = Verify(pk, \, m^d \bmod N) =  (m^d \bmod N)^e \bmod N = m^{ed} \bmod N \\ = m^{ed \bmod \phi(N)} \bmod N = m \bmod N$  
  
  ​				若公钥和私钥匹配，上述过程输出 *m*，因此算法输出1；否则，输出0。
  
- 安全性证明：

  - 定理：**上面的 *RSA* 签名策略不安全**，具体来说甚至不满足适应性选择消息攻击安全 *EUF*。

    **证明**：在 *EUF* 安全的条件中，攻击者 $A$ 拥有访问 $Sign(·)$ 的 *oracle* 权限。为证明 *RSA* 签名不满足 *CPA* 安全，攻击者 $A$ 需要在上述条件下，给定消息 $m$，伪造消息-签名对 $(m, \sigma)$，使得 $Verify(pk, m, \sigma) = 1$。

    首先，攻击者 $A$ 需要获取一对利用当前私钥 $(N, d)$ 签名的消息-签名对 $(m, \sigma)$，其中 $\sigma := m^d \bmod N$，并通过公钥验证该消息-签名对是合法的。
    
    然后，攻击者 $A$ 构造消息 $m' = 2m \bmod N$，并访问 $Sign(·)$ 获取该消息的签名 $\sigma' = (2m)^d \bmod N$，该消息-签名对通过公钥验证后也是合法的。
    
    由 $\sigma' / \sigma = 2^d \bmod N$ 知，$d = \log_2((\sigma' / \sigma) \bmod N)$，即可求得 *RSA* 签名的私钥 $(N, d)$，进而伪造合法的消息-签名对。
    
  - 注意，上述证明过程中，由于 $M = Z^*_N$ 是乘法群（且 $2$ 几乎一定与 $N$ 互素，因此 $2$ 位于该乘法群中）因此 $(m' / m) \bmod N$ 仍然为 $2$，即上述证明同样成立。

------

### 2.2 非 *0-1* 消息空间下的签名策略

- 例如 *RSA* 签名中的消息空间就为 $M = Z^*_N$

- 方案：

    - ***Hash-and_Sign Paradigm***
    - ***DSA/ECDSA***

    

    









