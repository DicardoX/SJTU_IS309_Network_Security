# Mac Wireshark入门

[Wireshark Document](https://www.wireshark.org/docs/wsug_html_chunked/ChCapInterfaceSection.html)

[Mac中wireshark如何抓取HTTPS流量](https://www.cnblogs.com/realjimmy/p/13418520.html)

-----

- 当您**在不启动捕获或打开捕获文件的情况下打开Wireshark**时，它将显示“欢迎屏幕”，其中列出了**任何最近打开的捕获文件和可用的捕获接口**。每个接口的网络活动将显示在接口名称旁边的火花线中。**可以选择多个接口，同时从中捕获。**

<img src="./cut/截屏2021-04-25 下午4.34.46.png" alt="avatar" style="zoom:30%;" />

​		注意：带有“齿轮”标识的接口允许或要求在捕获前配置，点击即可配置

​		Wireshark不仅限于网络接口——在大多数系统上，您还可以捕获USB、蓝牙和其他类型的数据包。

- 当您选择“捕获→选项...”（或使用主工具栏中的相应项）时，Wireshark会弹出“捕获选项”对话框。如果您不确定要在此对话框中选择哪些选项，那么在许多情况下，将默认设置保持原封状态应该可以很好地工作。

  <img src="./cut/截屏2021-04-25 下午4.41.53.png" alt="avatar" style="zoom:40%;" />

  - 输入Input：

    - 参数：
      - Interface：接口名称
      - Traffic：显示网络活动随时间推移的火花线
      - Link-layer Header：**此接口捕获的数据包类型**
      - Promiscuous：混杂模式
      - SnapLen (B)：快照长度，或**每个数据包捕获的字节数**
      - Buffer (MB)：保存捕获到的数据包的缓冲区大小，一般默认即可
      - Monitor Mode：让您捕获完整的原始 802.11 标头。支持取决于接口类型、硬件、驱动程序和操作系统。请注意，启用此功能可能会将您与无线网络断开连接。
      - Capture Filter：抓取过滤器，可双击进行编辑，可以被设置为多个
    - 将鼠标悬停在某个接口上或点击下拉可以显示与它关联的IPv4或IPv6地址

  - 输出Output：

    <img src="./cut/截屏2021-04-25 下午4.59.23.png" alt="avatar" style="zoom:40%;" />

  - 选项Option：

    <img src="./cut/截屏2021-04-25 下午5.01.26.png" alt="avatar" style="zoom:40%;" />

    - Display Options：
      - 实时更新数据包列表：在捕获期间实时更新数据包列表窗格。如果您不启用此功能，Wireshark在停止捕获之前不会显示任何数据包。当您检查此操作时，Wireshark会在一个单独的进程中捕获，并将捕获反馈到显示进程。
      - 实时抓拍时自动滚动：随着新数据包的出现，滚动数据包列表窗格，因此您总是查看最新的数据包。如果您没有指定此Wireshark，则将新数据包添加到数据包列表中，但不滚动数据包列表窗格。如果禁用“实时更新数据包列表”，此选项将显示灰色。
      - 在抓取过程中显示抓取信息
    - Name Resolution：
      - 解析Mac地址：将MAC地址转换为名称
      - 解析网络名称：将网络地址转化为名称
      - 解析运输名称：翻译运输名称（端口号）

- 参考[ref 2]((https://www.cnblogs.com/realjimmy/p/13418520.html))将wireshirk与google chorme绑定，之后双击wifi开始访问，过滤框输入特定内容（如ip.addr==202.120.35.204）进行过滤，从而进行流量分析

