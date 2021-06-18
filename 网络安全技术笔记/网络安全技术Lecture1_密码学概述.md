# 网络安全技术 Lecture 1 密码学概述

## 1. 密码学与网络安全

### 1.1 密码学的分类

-  ***Crptology***：创建/破解密码的艺术和科学

    - **密码设计学 *Cryptography***：设计密码方案，在不安全的信道上进行安全传输

        <img src="./cut/截屏2021-06-12 下午10.03.01.png" alt="avatar" style="zoom:40%;" />

    - **密码分析学 *Cryptanalysis***：分析、破解密码方案，起锻炼密码设计学的作用

        - 获取用于加密密文的密钥
        - 不使用密钥从密文中恢复明文

    - 早期密码学的概念：密码 (*cipher*) 或密码系统 (*crptosystem*) 用于加密明文/解密密文

- ***Crpto***：包含上述几个概念，更加广义

    - 签名（不可否认性）、认证 (*authentication*)、识别 (*identification*)、零知识证明 (*zero-knowledge*)、承诺 (*commitment*) 等等

---------

### 1.2 古典密码学（属于对称加密策略），艺术、启发式

- **凯撒密码（移位密码）(*Casear's Cipher*)**：

    - 简单向后移位，共 $26$ 种移位方案
    - **消息空间 *Message Space***：$M = \{m \ | \ m$ *is any string consists of 26 English letters with the length of* $n \}$
    - **密钥空间 *Key Space***：$K = \{k \ | \ k \in [0, 25]\}$
    - **密文空间 *Ciphertext Space***：$C = \{c \ | \ c$ *is any string consists of 26 English letters with the length of* $n \}$
    - **密钥生成算法 *Key Generation Algorithm***：$KeyGen(\lambda) = \{k \ | \ k \in \mathbb{N}$ *and* $k$ *is randomly chosen in the range of* $[0, 25]$ *according to some probabilistic distribution* $\}$

    - **加密算法 *Encryption Algorithm***： $Enc(k,m) = \{c \ | \ c[i] = (m[i] + k) \bmod 26, i \in [1, n]\}$
    - **解密算法 *Decryption Algorithm***：$Dec(k, c) = \{m \ | \ m[i] = (c[i] - k) \bmod 26, i \in [1, n] \}$

- **简单置换密码 *Simple Substitution Cipher***：

    - 哈希映射，共 $26!$ 种映射方案
    - **消息空间 *Message Space***：$M = \{m \ | \ m$ *is any string consists of 26 English letters with the length of* $n \}$
    - **密钥空间 *Key Space***：$K = \{k \ | \ k=permulation(1, 26)\}$
    - **密文空间 *Ciphertext Space***：$C = \{c \ | \ c$ *is any string consists of 26 English letters with the length of* $n \}$
    - **密钥生成算法 *Key Generation Algorithm***：$KeyGen(\lambda) = \{k \ | \ k[i] \in \mathbb{N}$ *and* $k$ *is random permutation of* $1, 2, ..., 26$ *according to some probabilistic distribution* $\}$
    - **加密算法 *Encryption Algorithm***：$Enc(k, m) =\{c \ | \ c[i] = k[m[i]], i \in [1, n]\}$
    - **解密算法 *Decryption Algorithm***：$Dec(k, c) = \{m \ | \ m[i] = k^{-1}[c[i]], i \in [1, n]\}$

-------



## 2. 现代密码学，科学，方法论

### 2.1 现代密码学概念

- 以**更系统的方式进行开发和分析**，最终目标是**提供给定构造安全的严格证明**。
- **语法 *Syntax***：
    - 规程，从现实场景中提炼出的要求，相当于是**安全证明过程中的基本元素**
    - **描述了密码原语应该具有哪些功能**
    - 例如在加密方案中，密钥生成算法、加密算法、解密算法等的定义
- **安全模型 *Security Models***：
    - **安全性 *Security***
    - 针对不同等级的攻击者，攻击者有何种攻击能力，**在特定攻击能力下能够保证的安全性**
    - 不同的安全模型会产生不同的安全性要求，需要设计不同安全性的方案
- **可证明安全 *Provable Security***：
    - **正确性 *Correctness***
    - 用来证明**密码方案的安全性**
    - 例如对于对称加密，**必须满足如下正确性要求**：**对任意由密钥生成算法生成的密钥 $k$ 和任意明文 $m$ ，有：$Dec(k, Enc(k, m)) = m$**

注意：**语法和正确性定义并描述了密码方案的功能 *functionalities***

-----------

### 2.2 密码方案设计原则

- **科克霍夫原则 *Kerckhoffs' Principle***
    - **加密算法必须公开，仅密钥保密**
        - 一般假设攻击者了解正在使用的加密方案
    - 原因有三点：
        - **密码算法本身不可能一直保密**
        - **更换密钥比更换密码算法更方便，且更易保存**
        - **经过公开分析的密码算法，才能被认为是“安全的”算法**

- **大密钥空间原则 *Sufficient Key-space Principle***
    - **任何安全加密方案的密钥空间必须足够大，以使穷举攻击 (*Brute Force/Exhaust Search*) 不可实现，即攻击代价大于攻击对象的价值**
    - 为安全提供了必要条件，但不是充分条件

------

### 2.3 现代密码学原则

- 原则一：**规范定义 *Formal Definitions***
    - 清晰描述**范围内的威胁类型**，以及**需要何种安全保障**，为构建方案的**评估、分析和、比较和使用**提供方法
    - 注意：**安全模型 = 威胁模型 + 安全保障**
    - **安全保障 *Security Guarantee***：描述了该方案旨在防止攻击者做什么（目的）

    <img src="./cut/截屏2021-06-13 下午5.05.53.png" alt="avatar" style="zoom:30%;" />

    - **威胁模型 *Thread Models***：描述了**对抗强度**，与 “安全模型” 相辅相成（明确威胁模型，进而确定安全模型）（对抗对象）

        - **唯密文攻击 *Ciphertext Only Attack, COA***：
          
            - 最基础，攻击者仅通过观察密文来判断信息
            - 攻击者的目标是推断出使用相同密钥加密得到的密文所对应的明文信息
            - **该威胁模型对应的安全保障要求最低**
            - 模型流程：
                - 学习阶段（挑战前）：给予攻击者同一密钥 $k$ 生成的一些密文 $c_i$
            
            <img src="./cut/截屏2021-06-13 下午3.38.34.png" alt="avatar" style="zoom:30%;" />
            
        - **已知明文攻击 *Known Plaintext Attack, KPA***：
            - 攻击者掌握了由某些密钥生成的多对明文-密文
            
            - 攻击者的目标是推断出使用相同密钥加密得到的**其他**密文所对应的明文信息
            
            - 模型流程：
            
                - 学习阶段（挑战前）：给予攻击者同一密钥 $k$ 生成的一些密文-明文对 $(c_i, m_i)$
            
                <img src="./cut/截屏2021-06-13 下午3.41.34.png" alt="avatar" style="zoom:30%;" />
            
        - **选择明文攻击 *Chosen Plaintext Attack, CPA***：
            - 攻击者自主选择一些明文，并掌握了这些明文对应的密文

            - 攻击者的目标是推断出使用相同密钥加密得到的**其他**密文所对应的明文信息

            - 性质：

                - **没有确定性公钥加密方案满足 *CPA* 安全**

            - 模型流程：

                - 学习阶段（挑战前 + 后）：攻击者选择明文 $m$，被攻击者返回同一密钥 $k$ 加密后的密文 $c$

                <img src="./cut/截屏2021-06-13 下午3.43.18.png" alt="avatar" style="zoom:30%;" />

        - **选择密文攻击 *Chosen Ciphertext Attack, CCA***：

            - 攻击者自主选择一些密文，并掌握了这些密文对应的明文

            - 攻击者的目标是推断出使用相同密钥加密得到的**其他**密文所对应的明文信息

            - 模型流程：

                - *CCA*：学习阶段（挑战前 + 后）：攻击者选择密文 $c_i$，被攻击者返回同一密钥 $k$ 解密后的明文 $m_i=Dec(k,c_i)$
                - *CCA2*：*CCA* + *CPA*（下图为 *CCA2*）

                <img src="./cut/截屏2021-06-13 下午3.46.39.png" alt="avatar" style="zoom:30%;" />

        - 注意：

            - 四种威胁模型各自有适用的环境，没有优劣之分
            - **攻击者能力由强到弱**的排序：*CCA*、*CPA*、*KPA*、*COA*
            - **相应安全的方案强度**：*CCA*、*CPA*、*KPA*、*COA*
            - *Question.* **如果一个加密方案满足攻击者能力较强的威胁模型下的安全，那能不能直接推导出它也满足较弱威胁模型下的安全呢？** 
                - **可以直接推导出**。

- 原则二：**精确假设 *Precise Assumptions***

    - 大多数现代密码构造都不能被无条件地证明其安全性，这些证明需要依赖于计算复杂性理论中目前远不能被解答的问题。**安全性证明通常依赖于假设，这些假设是未经证实但被推测为正确的陈述**
    - 这些假设必须**显式 *explicit***且在**数学上精确 *mathematically precise***
    - **假设的验证 *Validation of assumptions***：一个假设只有被精确陈述，才能对其进行研究和可能的推翻。假设在不被推翻的情况下检查和测试的次数越多，我们就越有信心该假设是正确的
    - **方案的比较 *Comparison of schemes***：考虑基于两种不同假设的两个方案，并假设其他一切为真。**基于较弱假设的方案更好**；若两种假设不具备可比性，则**研究得更好 *better-studied* 的假设对应的方案更可取**
    - 举例：大整数分解假设、离散对数假设、*Diffie-Hellman* 假设

- 原则三：**安全性证明 *Proofs of Security***

    - **规范定义**和**精确假设**使我们能够实现目标，即**严格证明构造的方案满足特定假设下的给定定义**。
    - **安全性证明** 相较于上述二者则更加能够保证没有攻击者能够成功：
        - (**归约 Reduction**)：“**若假设 *X* 成立，则没有攻击者能够在博弈中以不可忽略的优势 (*non-negligible advantage*) 取得成功**”
    - 方案的可证明安全性并不一定意味着该方案在现实世界中的安全性
        - 为了在现实世界中攻击可证明安全的方案，需要关注：定义（理想化定义和部署方案的实际环境有何不同），基本假设（是否成立）
    - 可证明安全并没有结束攻击者和被攻击者的斗争，只是为提高被攻击者的安全提供了框架



