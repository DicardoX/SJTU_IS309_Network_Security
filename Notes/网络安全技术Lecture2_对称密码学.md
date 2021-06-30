# 网络安全技术 Lecture 2 对称密码学

信息安全的两大特性：

- **机密性 *Secrecy/Confidentiality***：**防止攻击者破解通过不安全信道传输的消息的内容**
    - 方法：**加密算法**
- **完整性 *Authentication/Integrity***：接收方需要能够识别它**收到的消息的确来自声称发送它的一方**，且在**传输过程中没有被篡改**
    - 方法：
        - 对称密码学：**消息认证码 *Message Authentication Code, MAC***
        - 公钥密码学：**数字签名 *Digital Signature***

----------



## 1. 私钥加密 *Private Key Encryption*，机密性

### 1.1 概念

#### 1.1.1 语法 *Syntax*

​	私钥加密策略由**消息空间 $M$** 和**三个算法 $KeyGen$、$Enc$、$Dec$** 定义

- $KeyGen(\lambda) \rightarrow k$：
    - 概率性算法，根据安全参数 $\lambda$ （描述了该加密方案安全等级）某种分布输出密钥 $k$
- $Enc(k, m) \rightarrow c$：
    - 输入：密钥 $k$，消息 $m \in M$
    - 输出：密文 $c$
- $Dec(k, c) \rightarrow m$：
    - 输入：密钥 $k$，密文 $c$
    - 输出：明文 $m$
- 注意：“消息”和“明文”的在使用上的区别：**一般把加密算法的输入称为“消息”，解密算法的输出称为“明文”**

-------

#### 1.1.2 安全性证明

- 私钥加密策略 $(KeyGen, Enc, Dec)$ 必须满足如下安全要求：
    - **对任意 $KeyGen$ 生成的密钥 $k$ 和任意消息 $m \in M$， 必须满足 $Dec(k, Enc(k, m))=m$** 

------------------

#### 1.1.3 安全模型 *Security Model*

- **安全模型 = 威胁模型 + 安全保障**
- ***CCA2* 安全模型**：
    - **考虑**如下私钥加密 $\Pi = (KeyGen, Enc, Dec)$ 的实验，假定一个攻击者 $A$，以及安全参数 $\lambda$
    - **准备阶段**：运行 $KeyGen(\lambda)$ 获得密钥 $k$，并将安全参数 $\lambda$ 提供给攻击者 $A$
    - **学习阶段一**：**给予攻击者 $A$ 对 $Enc_k(·)$ 和 $Dec_k(·)$ 的 *oracle* 访问权限**，即当攻击者 $A$ 向 $Enc_k(·)$ 或 $Dec_k(·)$ 提交消息 $m$ 或 密文 $c$ 时，相应加密或解密后的密文 $c$ 或 明文 $m$ 被返回
    - **挑战阶段**：攻击者 $A$ 输出一对长度相同的明文 $m_0^* \neq m_1^* \in M$ ，被攻击者选择一个特殊的比特 $b \in \{0, 1\}$ ，以此为依据选择使用哪一个明文，并计算 $c^* \leftarrow Enc(pk, m_b^*)$ ，将**挑战密文**$c^*$提供给攻击者 $A$ 
    - **学习阶段二**：与学习阶段一相同，但攻击者 $A$ 不被允许向 $Dec_{sk}(·)$ 询问挑战密文 $c^*$ 
    - **输出阶段**：攻击者 $A$ 基于收到的挑战密文 $c^*$ 输出一个比特 $b' \in \{0, 1\}$ ，来猜测 $b$ 
    - 若 $b' = b$ ，则攻击者 $A$ 成功。将**攻击者 $A$ 的优势** 定义为$Adv_{\Pi, A}^{CCA2} = |Pr[b'=b] - 1/2|$ ，则我们定义一个**私钥公加密策略 $\Pi = (KeyGen, Enc, Dec)$ 是CCA2安全**的条件是：**对于所有 *PPT* 攻击者 $A$ ，都存在一个可忽略的函数 $negl$ 使得 $Adv_{\Pi, A}^{CCA2} \leq negl(\lambda)$ **
        - 该部分属于安全保障，之前的均属于威胁模型

------



### 1.2 私钥加密策略

- 两类：流密码 *Stream Ciphers*、块密码 *Block Ciphers*

#### 1.2.1 流密码 *Stream Ciphers*

<img src="./cut/截屏2021-06-13 下午5.38.59.png" alt="avatar" style="zoom:40%;" />

- 密钥 $k$ 输入到**密钥流生成器 *Keystream Generator*** 中，不断生成**密钥流 *Key Stream***，并与消息 $m$ **逐字符/逐位加密**，生成密文 $c$

- 安全性：给定一段长的密钥流，**不能推导出密钥**，且**不能推导出密钥流的后续段**

- ***RC4* 算法**：

    - ***Step 1.* 初始化**

        <img src="./cut/截屏2021-06-13 下午6.15.00.png" alt="avatar" style="zoom:40%;" />

    - ***Step 2.* 密钥流生成**

        ​	<img src="./cut/截屏2021-06-13 下午6.16.10.png" alt="avatar" style="zoom:50%;" />

    - 使用 $KeyStreamByteSelected$ 来和消息中的每个 *byte* 做**异或运算 (xor)**

---------

#### 1.2.2 块密码 *Block Ciphers*

<img src="./cut/截屏2021-06-13 下午6.22.15.png" alt="avatar" style="zoom:40%;" />

- 输入：**消息块 *a block of plaintext***，**密钥 *secret key***

- 输出：**密文块 *a block of ciphertext***

- **密钥可以在不同的消息块重复使用**

- 方案：*DES*、*3DES*、*AES*、*Twofish*、*Serpent*

- **迭代式块密码 *Iterated Block Cipher***：

    - 通过 ***round function*** 的迭代来从消息中获取密文，*round function* 即为基本块的复杂线性组合

- ***DES***：*16* 轮的 *Feistel round funtion*，块大小为 *64 bits*，密钥大小为 *56 bits*

    - ***DES* 的安全性**：完全取决于 *f* 的内部结构
        - 可以认为是**安全**的，目前针对 *DES* 最有效的攻击仍是**穷举攻击**

- ***Triple DES (3DES)***：两个 *56 bits* 的密钥

    <img src="./cut/截屏2021-06-13 下午6.40.09.png" alt="avatar" style="zoom:35%;" />

- ***DESX***：三个密钥，相比 *DES* 更难通过穷举攻击攻破

    <img src="./cut/截屏2021-06-13 下午6.42.56.png" alt="avatar" style="zoom:35%;" />

- ***AES (Advanced Encryption Standard)***：

    <img src="./cut/截屏2021-06-13 下午6.45.47.png" alt="avatar" style="zoom:30%;" />

- 块密码**如何处理多个块**？讨论三种操作模式

    - **电子密码本 *Electronic Codebook (ECB) mode***：基本工作模式

        <img src="./cut/截屏2021-06-13 下午6.54.35.png" alt="avatar " style="zoom:40%;" />

        - 待处理信息被划分为大小合适的块，进行**独立加密/解密处理**，每个块使用**相同的密钥和 *DES* 结构**
        - 优点：操作简单，易于实现，可以并行处理，能够防止误差传播
        - 缺点：由于所有块的加密方式一致，明文中重复的内容会在密文中有所体现，**难以抵抗统计分析攻击** 和 **重放攻击 **

    - **密码块链 *Cipher Block Chaining (CBC) mode***：

        <img src="./cut/截屏2021-06-13 下午6.58.28.png" alt="avatar" style="zoom:40%;" />

        - 所有块被串联在一起，一个**公开的随机向量 *IV*** 被用来初始化 *CBC*
        - 加密：$C_0 = E(K, P_0 \oplus IV)$，$C_1 = E(K, P_1 \oplus C_0)$，...
        - 解密：$P_0 = IV \oplus D(K, C_0)$，$P_1 = C_0 \oplus D(K, C_0)$，...
        - 优点：**解密时错误的有限传播**，且具有更高的安全性，**解密时支持并行计算**
        - 缺点：错误会影响到后一个分组，加密时**无法对中间的某个消息块进行单独加密**，不支持并行计算，**更适用于随机读取而非写入**
        - 对 *CBC* 模式的攻击：**加密过程中，攻击者对初始化向量 *IV* 中的任意 *bit* 进行反转，则消息块中相应的 *bit* 也会被反转**。 

    - **计数器模式 *Counter (CTR) mode***：**参考流密码来实现块密码**

        <img src="./cut/截屏2021-06-13 下午7.06.35.png" alt="avatar" style="zoom:40%;" />

        - 通过逐次累加的计数器进行加密来生成密钥流的流密码，**最终的密文分组是通过将计数器加密得到的比特序列，与明文分组进行异或得到的**
        - 加密：$C_0 = P_0 \oplus E(K, IV)$，$C_1 = P_1 \oplus E(K, IV+1)$，...
        - 解密：$P_0 = C_0 \oplus E(K, IV)$，$P_1=C_1 \oplus E(K, IV+1)$，...
        - 优点：**加密和解密均支持并行计算**，不存在错误的传播，可以进行中间分组的单独加密，**同时适用于随机读取和写入**
        - 缺点：攻击者反转密文分组中的某些比特时，明文分组中的相应比特也会被反转



#### 1.2.3 流密码和块密码的比较

- 使用流密码总体要比块密码更快，硬件实现更简单
- 流密码逐字符进行加密/解密，而块密码逐块进行加密/解密
- 流密码中的密钥仅能使用一次，而分组密码的密钥可以重复使用
- 流密码中冗余较少，块密码中增加了冗余
- 流密码用于 *Web* 的 *SSL* 安全连接，块密码用于数据库和文件加密

--------



## 2. 消息认证码 *Message Authentication Code, MAC*，完整性

- 一种**确认完整性并进行认证**的技术

### 2.1 概念

#### 2.1.1 语法 *Syntax*

​	消息认证码由三个 *PPT* 算法 $KeyGen$、$Mac$、$Verify$ 定义

- $KeyGen(\lambda) \rightarrow k$：
    - 概率性算法，根据安全参数 $\lambda$ （描述了该加密方案安全等级）某种分布输出密钥 $k$
- $Mac(k, m) \rightarrow t$：**标签生成算法 *tag-generation algorithm***
    - 输入：密钥 $k$、消息 $m \in \{0,1\}^*$
    - 输出：标签 $t$
- $Verify(k, (m, t)) \rightarrow 1/0$：**验证算法 *verification algorithm***
    - 输入：密钥 $k$、消息 $m$、标签 $t$
    - 输出：$b \in \{0, 1\}$，$b=1$ 表示合法，否则不合法

---------

#### 2.1.2 安全性证明

- 消息认证码必须满足如下安全要求：
    - 对任意 $\lambda$，任意 $k \leftarrow KeyGen(\lambda)$，任意消息 $m \in \{0, 1\}^*$，都要满足 $Verify(k, m, Mac(k, m)) = 1$

----------

#### 2.1.3 安全模型 *Security Model*

- **安全模型 = 威胁模型 + 安全保障**

- **自适应选择消息攻击 (*EUF*) 安全模型**：
    
    - **考虑**如下消息认证码 $\Pi = (KeyGen, Mac, Verify)$ 的实验，假定一个攻击者 $A$，以及安全参数 $\lambda$
    
    - **准备阶段**：运行 $KeyGen(\lambda)$ 获得密钥 $k$，并将安全参数 $\lambda$ 提供给攻击者 $A$
    
    - **学习阶段**：**给予攻击者 $A$ 对 $Mac_k(·)$ 的 *oracle* 访问权限**，即当攻击者 $A$ 向 $Mac_k(·)$ 提交消息 $m$ 时，相应的标签 $t$ 被返回
    
    - **输出阶段**：攻击者 $A$ 输出一对伪造的 (消息, 标签) 对，$m^* \in \{0, 1\}$，$t^*$
    
    - 令 $Q$ 表示攻击者 $A$ 在学习阶段向 $Mac_{k}(·)$ 提交的消息集合，若：
    
        - $Verify(k, m^*, t^*)=1$
        - $m^* \notin Q$ 
    
        则攻击者 $A$ 成功。
    
    - 将攻击者的优势定义为 $Adv_{\Pi, A}^{EUF} = |A \ succeeds|$，则我们定义一个**签名策略 $\Pi = (KeyGen, Mac, Verify)$  在适应性选择消息攻击下本质上不可伪造**的条件是：**对于所有PPT攻击者 $A$ ，都存在一个可忽略的函数 $negl$ 使得 $Adv_{\Pi, A}^{EUF} \leq negl(\lambda)$ **.
        - 该部分属于安全保障，之前的均属于威胁模型













