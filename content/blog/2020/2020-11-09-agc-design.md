---
title: AGC 高频谐振放大器
date: 2020-11-09
tags: [教程, 硬件, 高频, 多图预警]
authors:
  - name: ToddZ
math: true
---

<!--more-->

# 吐槽

&emsp;&emsp;原本历届都是做收音机的，到了我们这届德生不提供元件了，就换了题目，那行吧，这咱也不能强求赞助商。

&emsp;&emsp;原本说好了做锁相环的，其他班也确实做了锁相环，但到我们班就换成了AGC谐振放大，那行吧，咱班要求高点。

&emsp;&emsp;但尼玛你出题要和器件条件相吻合啊！做分立的关键部分中周（也就是电感）全都是坏的，麻烦你买元件能不能检查一下啊！尼玛这我焊好了才发现是坏的，这咋改电路啊！！！



# 设计任务与约束条件

设计并制作一个带自动增益控制（AGC）的高频谐振放大器，放大部分要求采用集成与分立元件两种方案实现。具体指标：

1. 谐振频率 $f=10.7$ Mhz，允许偏差 $100$ kHz
2. 增益不小于 $40$ dB
3. 输入阻抗 $R_\text{in}=50 \Omega$
4. 在满足增益条件下，尽可能减小矩形系数 $K_{r0.1}$
5. AGC 输出 $100$ mV，增益范围不小于 $30$ dB

AGC 增益范围计算方法：

$$
20 \log \left(\frac{U_{omin}}{U_{imin}}\right)-20 \log \left(\frac{U_{omax}}{U_{imax}}\right) \text{(dB)}
$$

器件条件：OPA847、AD860、AD603、三极管9018、10.7M中周（7mm×7mm）

实现条件：分立元件方案在万用焊接板上布局实现。

<!--![高频洞洞板](/assets/images/高频洞洞板.jpg)-->

<center><img src="https://i.loli.net/2020/11/09/SLN4rkcwlKRHUQf.jpg" title="高频洞洞板" width="600"></center>

# 理论基础

首先先不要紧张，这就是个谐振放大器，而且老师规定要用集成和分立两种方法，而集成就几种芯片，分立就一种三极管，所以也不用做那么多选择。至于 AGC 是什么，这个待会再看。

## 高频小信号放大器

&emsp;&emsp;去看高频第三章的内容：

* [单调谐回路谐振放大器](https://scuteee.com/courses/sophomore/commuelectronic/单调谐回路谐振放大器)
* [双调谐回路谐振放大器](https://scuteee.com/courses/sophomore/commuelectronic/双调谐回路谐振放大器)

&emsp;&emsp;好像形式大多是固定的，而且既然给了中周，那应该是用电感耦合。我找了一些电路图，到时候应该改改参数即可。

* [2011年全国电子设计大赛D题LC谐振放大器设计报告](https://max.book118.com/html/2017/0426/102456377.shtm) 里面明确提到了“中周选频”
* 课后习题：3.10，有趣的是其中的谐振频率恰好是 10.7Mhz，不过输入阻抗为 2.64kΩ，。

## AGC

&emsp;&emsp;自动增益控制(Automatic  Gain  Controll)是一种自动控制方法。它通过检测输出信号幅度，自动控制信号链路的增益，以使整个放大电路在输入信号幅度发生变化时，维持输出信号幅度不变。

&emsp;&emsp;自动增益控制中，输入信号幅度值和输出信号幅度值关系曲线如图：

<img src="https://ez.analog.com/cfs-file/__key/communityserver-discussions-components-files/750/pastedimage1556531097430v1.jpeg" style="zoom:50%;" />

1. 欠幅区：当输入信号过小时，压控增益放大器即便达到最大增益 $G_\text{min}$，其输出信号也达不到 AGC 设定的稳幅电压，此时随着输入信号幅度的增加，输出信号幅度也随之明显增加；
2. 稳幅区：当输入信号增大到一定值后，随着输入信号的增加，输出信号几乎维持不变，这个区域被称为稳幅区；
3. 超幅区：压控增益放大器的实际增益开始接近甚至达到 $G_\text{min}$，此时随着输入信号的进一步增大，压控增益放大器已经无力通过降低增益来降低输出信号，只能任由输出信号也随之上升。

&emsp;&emsp;根据题目的要求，增益范围 $20 \lg G_\text{max} - 20 \lg G_\text{min}$ 不小于 $30$ dB，并且 $(U_\text{omax}-U_\text{omin})/2=100mV$

AGC一般采用如下结构：

<img src="https://i.loli.net/2020/11/10/t3Ccuabo7DLfUyz.png" style="zoom:50%;" />

&emsp;&emsp;输出信号与设定直流电压 $V_\text{REF}$做比较，当输出幅度大于 $V_\text{REF}$ 时，$V_G$ 将持续变大以减小增益，进而减小输出幅度；当输出幅度小于 $V_\text{REF}$ 时，$V_G$ 将持续变小以增大增益，进而增大输出幅度，最终一定会维持输出幅度与设定幅度基本相等。压控增益放大器的增益受控于 $V_G$，且一定是负反馈关系：$V_G$ 越大，压控增益放大器的实际增益越小。

&emsp;&emsp;某些运放有 AGC 输出（比如 AD8310 的 3 脚 OFLT 就是 AGC 输出），通过一颗电容交流耦合后送到运放做电压跟随即可。而实验室提供的 AD603 也有 AGC 功能，下面来看看 AD603 是如何做到 AGC 的。

<img src="http://www.analog.com/-/media/images/products/zh/specialty-amplifiers/differential-amplifiers/ad6/ad603-fbl01.gif?h=500&thn=1&hash=5CF836B1A24F7676F2423C53CE24616D754B434D" style="zoom: 50%;" />

&emsp;&emsp;AD603 的结构图如上。先说说引脚：

* VPOS、VNEG 为正负电源输入端，推荐使用 ±5V，最大取 ±7.5V；
* GPOS、GNEG 为正负增益控制端（正端口正电压越大，增益约大；负端口则反之）；
* VINP 为信号输入端，COMM为地，FDBK 为反馈连接端口。

&emsp;&emsp;从图上来看，信号先是经过一个受控的衰减器，然后再经过一个放大器。衰减器受 GPOS 和 GNEG 控制；放大器的增益则可以通过在 VOUT 与 FDBK 之间连接不同电阻来调整，电阻值越大，则增益越大。

&emsp;&emsp;AD603 的实用电路如下：后面的三极管都是用于检波（得到输出的正弦信号的幅值）

![](http://www.elecfans.com/uploads/allimg/171201/2749557-1G201191K4401.jpg)

![](https://cache.amobbs.com/bbs_upload782111/files_44/ourdev_666145XZWFZQ.png)

* [自动增益控制（AGC）电路的设计](https://zhuanlan.zhihu.com/p/161754910)
* [agc自动增益控制简介](https://wenku.baidu.com/view/b7089cfbd05abe23482fb4daa58da0116c171ffa.html?rec_flag=default&word=agc%E8%87%AA%E5%8A%A8%E5%A2%9E%E7%9B%8A%E6%8E%A7%E5%88%B6%E7%AE%80%E4%BB%8B&fr=pc_oldview_relate-1001_1-3-wk_rec_doc2-1001_1-57270722192e45361066f505-b7089cfbd05abe23482fb4daa58da0116c171ffa)
* [自动增益控制电路的设计与实现](https://wenku.baidu.com/view/bbf0e94a33d4b14e84246815.html?rec_flag=default&word=agc%E8%87%AA%E5%8A%A8%E5%A2%9E%E7%9B%8A%E6%8E%A7%E5%88%B6%E7%AE%80%E4%BB%8B&fr=pc_oldview_relate-1001_1-6-wk_rec_doc2-1001_1-16661ed9ad51f01dc281f105-bbf0e94a33d4b14e84246815)

### 滤波器

&emsp;&emsp;这个没什么好说的，就无源滤波，电阻和电感串并联就行。由于无源滤波对信号有一定衰减，所以实际的放大电路的放大倍数要比要求的高一些。下面这个网站可以很方便的计算出电感与电容值。

* [(无源)高频滤波器](https://www.23bei.com/tool-771.html)

&emsp;&emsp;但如果使用谐振放大器的话，就无需滤波。

### 阻抗匹配

&emsp;&emsp;射频中有讲如何实现阻抗匹配，但我们班没学射频，所以我也不确定题目要求的阻抗要如何实现。如果使用集成器件的话还好，直接在输入端接个电阻到地就行；如果是分立元件（三极管）的话，也是接个电阻，另外还要加个电感避免影响静态工作点。

* [匹配网络](https://wenku.baidu.com/view/0a7969a669eae009591bec52.html)



## 器件

### 9018

&emsp;&emsp;TO-92 塑封封装 NPN 半导体三极管，参数见 [datasheet](http://www.fsbrec.com/pdf/9018.pdf)，但找不到 Pspice 模型，在 Multism 中只好用 2N2369/3DG84B代替。

### 中周

&emsp;&emsp;中频变压器（俗称中周），是超外差式晶体管收音机中特有的一种具有固定谐振回路的变压器，但谐振回路可在一定范围内微调，以使接入电路后能达到稳定的谐振频率。当旋转磁帽时，使磁帽上下移动，改变磁芯和磁帽的相对位置，从而能够在10%的范围内改变中周线圈的电感量。

&emsp;&emsp;中周大概长下图这样，主要是一对耦合电感，然后既然其参数中有谐振频率，那么应该还有电感。至于微调的话应该是调两个电感的耦合系数吧？

<!--<center><img src="https://i.loli.net/2020/11/09/5sW9VXvxtyFg1w7.jpg" title="中周" width="300"></center>-->

<center><img src="https://i.loli.net/2020/11/09/jy6NGfxpsdzCeWt.jpg" title="中周内部" width="400"></center>

<center><img src="https://i.loli.net/2020/11/09/Jw2VdauAoclqC4U.jpg" title="中周等效电路" width="400"></center>

&emsp;&emsp;中周的资料非常少，只有收音机论坛里面的人才会讨论，淘宝上也基本没人卖，据老师说我们用到的中周也是厂家在旮旯角翻出来的……然而，在测试时我发现中周全是坏的，拆开外壳后发现次级回路的两个脚根本没有接电感，也就是说，这个中周只能当一个可调电感来使用。然后经过我进一步的测试发现，初级回路的电感值在 MH 级别，也就是说，要达到规定的谐振频率，电容是在 0.01nF 级别，但我们最小的电感也就是 0.5nF……

&emsp;&emsp;于是乎，由于缺少实验元件，分立的就不用做了（好耶ヽ(✿ﾟ▽ﾟ)ノ），而我作为第一个发现电感有问题的人，还能加分（好耶ヽ(✿ﾟ▽ﾟ)ノ）



### OPA847

[Datasheet OPA847](https://media.digikey.com/PDF/Data%20Sheets/Texas%20Instruments%20PDFs/OPA847.pdf)

### AD860

[Datasheet AD8605/AD8606/AD8608](https://www.analog.com/media/en/technical-documentation/data-sheets/AD8605_8606_8608.pdf)

### AD603

[Datasheet AD603](http://www.chip37.com/article/97.html)

# 参考

* [三极管在Multisim替换](https://wenku.baidu.com/view/9233508fa58da0116c174977.html)
* [图解经典电路之六管调幅收音机](https://zhuanlan.zhihu.com/p/32082174)
* [收音机原理及电路图](https://blog.csdn.net/ccsss22/article/details/108206316)