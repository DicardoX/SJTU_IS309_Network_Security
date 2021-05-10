# *DNS Spoofing Attack (DNS Poison)* 相关实现

[Ref: SelinaDeepKaur](https://github.com/SelinaDeepKaur)/**[DNS-Injector-Detector](https://github.com/SelinaDeepKaur/DNS-Injector-Detector)**

-----



## 1 *DNS Spoofing Only*

### 1.1 运行方法

*Command:*  `sudo python3 DNS_Spoofing.py -i en0 -h hostnames udp`

- `-i`：指定**攻击者实施攻击所监听的网络接口名称**
- `-h`：指定写有待 *poison* 域名和 *IP* 的映射文件。文件内容如"www.sjtu.edu.cn 119.3.32.96"，用于表示仅针对哪些域名进行poison，注意后面的 *ip* 地址与域名并无对应关系。
- `expression`：相当于是过滤器的选择，使用 `udp` 即可

-------



### 1.2 代码实现



------



### 1.3 结果分析

- 注意监听的网络接口**是攻击主机自己的网络接口**，从该接口获得含 *UDP* 报文的 *DNS* 请求包，解析构造，获得 *IP dst*、*IP src*、*DNS ID*、*DNS rdata* 等信息，并伪造响应包进行 *send*，在被攻击主机 (*Victim*) 上进行抓包，证明 *Victim* 确实收到了伪造的 *DNS* 响应包，即**完成了 *DNS Spoofing* 的攻击流程**。
- 网络接口监听到的 *DNS* 请求包中，*IP src (192.168.31.229)* 应该为**攻击主机的 *IP* 地址**，*IP dst (192.168.31.1)* 应该为**攻击主机设置的 *DNS* 服务器的 *IP* 地址**。为了方便抓包，我们在伪造的 *DNS* 响应报文中设置 *IP dst* 为 *hostnames* 文件中定义的 *redirect_to* 地址，并将 *DNS* 请求包中的 *rdata* 也设置成 *redirect_to*。
- 在攻击主机上运行 `sudo python3 DNS_Spoofing.py -i en0 -h hostnames udp` 进入监听状态，当攻击主机的 `en0` (*wifi*) 网络接口访问在 *hostnames* 文件中指定的域名时，相应的 *DNS* 请求包会被捕捉到：

<img src="./cut/截屏2021-05-11 上午2.04.48.png" alt="avatar" style="zoom:50%;" />

- 同时，在 *Victim* 主机上或攻击主机上使用 *Wireshark* 进行抓包，筛选条件为 `ip.addr==202.120.2.119`（这里为了便于抓包，我们选择将在伪造的 *DNS* 响应包中修改 *IP dst* 和 *DNS rdata*）。筛选结果如下：

<img src="./cut/截屏2021-05-11 上午2.05.19.png" alt="avatar" style="zoom:50%;" />

- 为了验证抓包结果的正确性，我们首先观察包的 *Info* 字段：

<img src="./cut/截屏2021-05-11 上午2.06.28.png" alt="avatar" style="zoom:50%;" />

​		可以看到，*Info* 提示该 *DNS* 报文属于响应包，且目的地 `www.bilibili.com` 的地址被成功篡改为 `202.120.2.119`，原因是我们设置了 *IP dst* 为该 *fake IP*

- 进一步通过 *DNS id* 的方式验证抓包结果的正确性，首先从攻击主机的输出信息中得知，该 *DNS* 的 *id* 为 *4139*。然后，在抓包工具 *Wireshark* 中查看该响应包的 *DNS id*：

<img src="./cut/截屏2021-05-11 上午2.05.54.png" alt="avatar" style="zoom:50%;" />

​		为 `Transaction ID: 0x102b`，注意到为十六进制，因此使用进制转换器验证正确性：

<img src="./cut/截屏2021-05-11 上午2.07.12.png" alt="avatar" style="zoom:50%;" />

- 注意到，伪造的 *IP dst* 还向攻击主机 (`192.168.31.229`) 发送了一条 *ICMP* 报文，告知该 *DNS* 请求包的 *dst* 无法到达，原因是攻击主机最远只能到达其本身设置的 *DNS* 服务器 (`192.168.31.1`)，不能跳出子网直接访问 `202.120.2.119`。
- 综上所述，本次 *DNS Poison Attack* 成功。

