# 网络安全技术 Lecture 8. 认证和密钥交换

## 1 认证 `Authentication`

- *Alice* 向 *Bob* 证明她的身份
- 可能也同时需要 *Bob* 证明自己的身份（**互相认证 *Mutual Authentication***）
- 在**具有物理安全连接的独立计算机**上进行身份验证相对简单，**在网络上的认证则相对复杂**
  - 攻击者能够被动地观察信息 (*Passively Observe Messages*)
  - 攻击者能够重放信息 (*Replay Messages*)
      - **重放攻击 *Replay Attack***：入侵者从网络上截取主机 *A* 发送给主机 *B* 的报文，并把由 *A* 加密的报文发送给 *B*，使主机 *B* 误以为入侵者就是主机 *A*，然后主机 *B* 向伪装成 *A* 的入侵者发送应当发送给 *A* 的报文。重放攻击有**延时性**，因此可以通过**现时**的方式来抵御。
  - 经常需要一个**加密信道**来安全地进行网络上的认证

### 1.1 单向身份认证 *One-way Authentication*

- 开放网络上可能会有窃听者，在 *Alice* 登陆邮件服务器的时候，可能会展开**重放攻击**：

  <img src="./cut/截屏2021-04-19 上午11.44.26.png" alt="avatar" style="zoom:30%;" />

  - 窃取 *Alice* 的登陆信息，并利用 *Alice* 的身份登陆邮件服务器，重放 *Alice* 的登陆信息

  - 对于以下情况，攻击者仍能简单地窃取**公钥加密后的用户名和密码** $E_{PK}(Username, \ Password)$ 或**哈希映射后的密码** $h(Password)$ 来展开重放攻击：

  <img src="./cut/截屏2021-04-19 上午11.45.44.png" alt="avatar" style="zoom:40%;" />

------



### 1.2 挑战-响应单向身份认证 *Challenge-Response One-Way Authentication*

- 目的是**抵御重放攻击**

- 假设 *Bob* 想要认证 *Alice*

  - **挑战报文**从**验证者 (*Verifier*) *Bob (Email Server)*** 发送到 **证明者 (*Prover*) *Alice***

  - 只有 *Alice* 才能够提供正确的**响应报文**

    <img src="./cut/截屏2021-04-19 下午3.12.06.png" alt="avatar" style="zoom:40%;" />

    - **挑战报文 *N*** 是一个随机数，**仅使用一次**，不需要是一个随机生成器生成的数，随便取就可以
    - **攻击者只能截取从 *Alice* 到 *Server* 发送的内容，但无法截取 *Server* 发给 *Alice* 的 *N***。*Bob* 通过 *Alice* 回复的响应报文中的 *N* 是否与自己发出的一致来判断是否为重放攻击。（“现时”）
    - **响应报文 *F(passwd, N)*** 中，*F* 是一个**公开的**单向函数，*passwd* 是 *Alice* 的密码，*F(passwd, N)* 在已知 *passwd* 的条件下可以解出 *N*
      - *F* 可以是**哈希函数**或者**分组密码** 
    - **只有 *Alice* 和 *Email Server* 知道 *passwd* 的值**，因此只有 *Alice* 可以提供正确的响应报文
  
  - 若 *Alice* 是一个机器，则 *passwd* 实际上可以被改成 **对称密钥 *K***
  
    <img src="./cut/截屏2021-04-19 下午3.19.13.png" alt="avatar" style="zoom:35%;" />
  
    - **通常，我们在描述协议时忽略从 *Prover* 到 *Verfier* 的 第一条信息流**，即 *"I'm Alice"*
  
  - 其他的基于对称密钥的挑战-响应技术：
  
  <img src="./cut/截屏2021-04-19 下午3.25.00.png" alt="avatar" style="zoom:40%;" />

---------



### 1.3 相互认证 *Mutual Authentication*

- *Alice* 和 *Bob* 互相认证，假设二人共享一个对称密钥 $K_{AB}$

<img src="./cut/截屏2021-04-19 下午3.29.14.png" alt="avatar" style="zoom:40%;" />

- *Alice* 先向 *Bob* 发送自己的 $ID_{Alice}$ 和 报文 $R_1$（<font color=blue>“喂，*Bob* 在吗，我是 *Alice*，请用$K_{AB}$ 加密你的 $ID_{Bob} $ 和 $R_1$ 证明自己的身份！”</font>）
- *Bob* 再向 *Alice* 发送使用对称密钥 $K_{AB}$ 加密过的 $ID_{Bob}$ 和 $R_1$（<font color=blue>“好的，我确实是 *Bob*，那你真的是 *Alice* 吗？请用 $K_{AB}$ 加密你的 $ID_{Alice}$，报文 $R_1$ 和我挑选的报文 $R_2$ 来证明自己的身份！”</font>）
- *Alice* 最后向 *Bob* 发送使用对称密钥 $K_{AB}$ 加密过的 $ID_{Alice}$，$R_1$ 和 $R_2$ （<font color=blue>“OK，我确实是 *Alice*，很高兴和你通信！”</font>）
- 相互认证完成。

----------



### 1.4 **公钥符号和假设 *Public Key Notations and Assumption***

- **使用 *Alice* 的公钥加密 *M*：$\{M\}_{Alice}$**
- **使用 *Alice* 的私钥签名 *M*：$[M]_{Alice}$**
- **所有的公钥都被假设为已被验证过（例如数字签名），且被广泛公布**

-------



### 1.5 基于公钥的单向身份认证 *Public Key Based One-Way Authentication*

- 现在是 *Bob* 要验证 *Alice* 的身份

- **基于公钥加密的方案**：

  <img src="./cut/截屏2021-04-19 下午3.45.19.png" alt="avatar" style="zoom:35%;" />

  - *Bob* 向 *Alice* 发送使用 *Alice* 的公钥加密的报文 *R*
  - *Alice* 使用自己的私钥解密，并将 *R* 发送给 *Bob*
  - *Bob* 直接比较 *R* 查看是否为 *Alice*

- **基于数字签名的方案**：

  <img src="./cut/截屏2021-04-19 下午3.47.36.png" alt="avatar" style="zoom:35%;" />

  - *Bob* 向 *Alice* 发送报文 *R*
  - *Alice* 使用自己的私钥进行签名，然后将 $[R]_{Alice}$ 发送给 *Bob*
  - *Bob* 使用 *Alice* 的公钥进行验证，比较 *R* 查看是否为 *Alice*

------



## 2 密钥交换 *Key Exchange*

### 2.1 *Basic Idea*

- **密钥交换协议 *(Key Exchange Protocol)***是**两方之间的通信协议**，目的是**在协议每次成功运行之后**建立**会话密钥 *Session Key***
- **会话密钥**的作用：**生成其他用作特定会话的密钥**，即**一个会话密钥对应一个会话，并生成该会话中可能使用的其他密钥**
  - 例如，可以**使用派生密钥保证机密性 *Confidentiality***；其他派生的密钥可以**用于消息身份验证/完整性 *Integrity***
- **中心化密钥管理 (*Centralized Key Management*)**：每个用户只和管理机构共享一个长期密钥，**长期密钥仅用来在用户间安全传输会话密钥`session keys`**，**数据由会话密钥进行加密/解密**
- 为什么不直接在所有会话里使用长期共享的对称密钥？
  - 降低所有会话被攻破的风险
  - 使用会话密钥的目标是，**即使某一个会话的所有密钥全部被攻破，只要长期密钥是安全的，其他会话的密钥将保持安全**
  - 控制长期密钥的数目，方便密钥的管理
- 有时候，我们需要**完全正向保密 *PFS, Perfect Forward Secrecy***，将在之后讨论

------



### 2.2 *Diffie-Hellman* 密钥交换：

- 被动攻击者情况下安全，活动攻击者（如中间人攻击）情况下不安全

<img src="./cut/截屏2021-04-19 下午4.32.10.png" alt="avatar" style="zoom:40%;" />

- 密钥交换：

  - *Alice* 和 *Bob* 分别持有一个大整数 *a* 和 *b*，且共享一个群的相关信息（包括 *(G, g, q, p)*，这些信息攻击者也会知道）
  - 在认证过对方确实是 *Alice* / *Bob* 之后：
    - *Alice* 向 *Bob* 发送 $g^a \bmod p $
    - *Bob* 计算得到对称密钥 $(g^a)^b = g^{ab} \bmod p$
    - *Bob* 向 *Alice* 发送 $g^b \bmod p$
    - *Alice* 计算得到对称密钥 $(g^b)^a = g^{ba} = g^{ab} \bmod p$

- 二人能够将 $K = g^{ab} \bmod p$ 作为对称密钥（**会话密钥**）

  - **原因是当攻击者窃取到 $g^a \bmod p$ 和 $g^b \bmod p$ 后，在 $CDH$ 假设成立的条件下，无法计算得到对称密钥 $K = g^{ab} \bmod p $**

  - *Diffie-Hellman* 密钥交换**在 *Diffie-Hellman* 假设成立的前提下是安全的**

  - 但是，该密钥交换策略是**不安全**的，**若网络中的攻击者是否处于活动状态**，即**中间人攻击 (*Main-in-the-middle Attack*)**。 “活动”是指攻击者可以拦截，修改，删除或将消息插入网络

    <img src="./cut/截屏2021-04-19 下午5.15.16.png" alt="avatar" style="zoom:40%;" />

    - *Trudy* 与 *Alice* 共享对称密钥 $g^{at} \bmod p$，与 *Bob* 共享对称密钥 $g^{bt} \bmod p$，则 *Alice* 和 *Bob* 甚至不知道 *Trudy* 的存在

-------



### 2.3 攻击者能力 *Adversarial Capabilities*

- 在设计密钥交换协议时，我们必须首先确定潜在对手的能力
- 如果密钥交换协议**仅在存在被动对手（即窃听者）的情况下**使用，则 ***Diffie-Hellman* 密钥交换协议被认为是安全的**
- 但是，如果**存在活动的对手（例如中间人攻击）**，则 ***Diffie-Hellman* 密钥交换协议不被认为是安全的**
- 在下面，让我们考虑一个活跃的对手。 对手可以拦截，修改和重播在任何两个通信方之间交换的消息。

-----------



### 2.4 基于公钥的密钥交换 *Public Key Based Key Exchange*

- *K* 为会话密钥，**为通话双方在密钥交换过程中互相确认的**

- 方案一：仅使用公钥加密

  <img src="./cut/截屏2021-04-19 下午9.32.46.png" alt="avatar" style="zoom:35%;" />

  - 该方案并不安全，因为攻击者可以冒充 *Bob*，仅加密，未身份认证
    - 冒充 *Bob* 拿到 $ID_{Alice}$ 和 *R*，然后选择一个会话密钥，和 *R* 一起用 *Alice* 的公钥加密后，和窃取到的 *Bob* 的 *ID* 一起发送给 *Alice*，即可冒充成功

- 方案二：仅使用私钥签名

  <img src="./cut/截屏2021-04-19 下午9.39.47.png" alt="avatar" style="zoom:35%;" />

  - 该方案更不安全，就连被动攻击者都可以发现会话密钥的值，只进行了身份认证（签名），未加密保护密钥
    - 原因是直接窃听得到 *R* 和 $[R, K]_{Bob}$ 的值，再用 *Bob* 的公钥验证即可得到 *K* 

- 方案三：**基于公钥的密钥交换**，同时使用公钥加密和私钥签名

  <img src="./cut/截屏2021-04-19 下午9.50.56.png" alt="avatar" style="zoom:35%;" />

  - 该方案安全，**先私钥签名后再公钥加密**，可以有效保证双方的安全性，但做不到**前向安全**，因为没有使用 *DF* 协议
      - **前向安全 *Forward Secrety***：即完全前向安全，指**长期使用的主密钥泄漏不会导致过去使用的会话密钥被泄露**。
      - 方案三中，若 *Bob* 或 *Alice* 的私钥被攻破，则只要攻击者保存了过去截取的交互信息，即可以破获过去使用的会话密钥 *K* 

-------



## 3 完全前正向安全 *PFS, Perfect Forward Secrety*

- 为了解决如下问题：

  - *Alice* 使用长期密钥 $K_{AB}$ 加密信息并发送给 *Bob*
  - *Trudy* 记录密文 *c*，随后攻击 *Alice* 或者 *Bob* 的电脑以获得 $K_{AB}$（通过获取 *a* 或 *b* 的方式）
  - 然后 *Trudy* 就能完全解密信息了

- 因此，***PFS* 的关注点在于，让攻击者无法解密之前记录的密文**，即使之后 *Trudy* 会获得 $K_{AB}$ 或者其他的秘密

- 我们可以使用 ***Diffie-Hellman* 来实现 *PFS***：

  - 但虽然 *DH* 对被动攻击者来说是安全的，对于积极攻击者却不安全（例如中间人攻击）

- 改进：

  <img src="./cut/截屏2021-04-19 下午9.58.55.png" alt="avatar" style="zoom:35%;" />

  - 会话密钥：$K_{AB} = g^{ab} \bmod p$
  - ***Alice* 忘记 *a*，*Bob* 忘记 *b***
    - 即使 *Alice* 和 *Bob* 也无法恢复出会话密钥 $K_{AB}$
  - 即使攻击者获得了二人的秘密，也无法恢复出会话密钥 $K_{AB}$
    - 原因是，在 *Diffie-Hellman* 密钥交换中，**被窃取的不会是 $K_{AB}$**，而是 $g^a \bmod p$ 或 $g^b \bmod p$，攻击者会攻破 *Bob* 或 *Alice* 通过获得 *b* 或 *a* 来计算出会话密钥



















