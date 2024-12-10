---
title: 在 CLion 开发 STM32
date: 2020-04-30
tags: [stm32] 
authors:
  - name: LYF
---



在 CLion 中开发 STM32 程序的教程在网上随处可见，然而所用操作系统以 MacOS 和 Linux 为主， Windows系统教程较少。且所用 CLion 版本各有不同，界面和配置流程也相差较大。~~目前我还没有检索到一个在2020年完全适用的 Windows 教程~~ 在我于[scuteee.com](scuteee.com)发表本文后，知名博主[稚晖君](https://space.bilibili.com/20259914)也于多平台发表了 [CLion 的开发环境配置](https://www.bilibili.com/read/cv6308000)，读者可以比较阅读。

本文约 3300 字，在一切顺利的情况下，实践本文内容大致需要 1 小时。

<!--more-->

# 在CLion中开发STM32
CLion 是一款现代化 C/C++ 集成开发环境，由 Jetbrain 公司开发，拥有优雅的界面、跨平台的特性和广受好评的智能插件。

STM32 的开发工具有 Keil MDK，STM32CubeIDE，VS Code的 Platform IO 等等。Keil 是功能强大的老牌开发软件，但是上古界面实在令人喜欢不起来。STM32CubeIDE 是 ST 力推的集成开发环境，集成了广受好评的代码初始化工具 STM32CubeMX ，界面也更加现代化，然而其代码补全功能居然还要按下 Alt+/ 才能使用（也可能是我没有找到相关的设置），智能程度也远远比不上 Jetbrain 公司开发的 CLion。

正好最近在尝试使用 CLion 替代 Visual Studio 开发 C/C++ 程序， CLion 新版本又添加了对 STM32CubeMX 的支持，于是果断选择 CLion 作为开发环境。然而，必须指出的是，目前业界，包括 ST 中国在内仍**普遍使用 Keil 作为开发工具**，学习时不能仅局限在一种开发环境。

## 背景知识

本文阅读者应具备下列知识背景

*   STM32CubeMX 软件的基本使用，如果没有使用经验，**请仔细阅读本部分内容，并自行学习相关内容**
*   STM32 基本使用方式与简单程序调试
*   如何 cmd 中执行简单命令

实践本文需要

*   安装 Windows 10 系统的计算机
*   带有 SWD 调试接口的 STM32 开发板（一般这个接口以一个独立的 4pin 排针引出）
*   ST-Link 或者其他适用于 STM32 的调试器

使用 CLion 开发 STM32 程序主要包括下面几个步骤：

1.  STM32CubeMX 初始化代码。STM32CubeMX 是意法半导体推出的代码初始化工具，可以在图形化界面中完成对芯片外设的基本配置并一键生成代码，不需要用户手动导入需要的外设文件、手动编写外设配置代码，大大节约了开发者的时间。此外，初始化代码步骤中 CLion 还将自动构建用于编译的 cmake 相关文件，而不需要用户自行编写。
2.  代码编写。
3.  使用 MinGW 和 arm-gcc 编译器编译程序。
4.  使用 OpenOCD 调试器进行代码下载与调试。OpenOCD 是一款开源调试器，旨在提供针对嵌入式设备的调试，在本文中，我们将使用 ST-Link v2 结合 OpenOCD 进行调试，OpenOCD 也同样支持 JLink 等调试器。

## 准备

#### 安装下列软件

提示1：**点击红色字体将跳转到相应链接**

提示2：在[ST官网](https://www.st.com/content/st_com/zh.html)下载速度可能较慢，[ST中国](https://www.stmcu.com.cn/)可提供替代

*   [CLion](https://www.jetbrains.com/clion/) 2019.3.15 或者更新的版本，过老的版本没有在软件中提供 STM32CubeMX 支持
*   [minGW](https://osdn.net/projects/mingw/releases/) 编译器，注意安装过程中要选择添加到环境变量，否则要手动添加
*   [arm-gcc-8-2019-Q4](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) 编译器，注意安装过程中要选择添加到环境变量，否则要手动添加
*   STM32CubeMX，可在 ST 官网下载
*   ST-Link驱动 根据自己的 ST-Link 版本在官网下载

#### 验证安装

在 cmd 中分别执行 `gcc-v` 和 `arm-none-eabi-gcc -v` 命令，若出现下面的输出，则说明编译工具安装已经成功。否则请检查环境变量

```shell
>gcc -v

Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=D:/Program\ Files/mingw64/bin/../libexec/gcc/x86_64-w64-mingw32/8.1.0/lto-wrapper.exe
Target: x86_64-w64-mingw32
```

```
>arm-none-eabi-gcc -v

Using built-in specs.
COLLECT_GCC=arm-none-eabi-gcc
COLLECT_LTO_WRAPPER=c:/program\ files\ (x86)/gnu\ tools\ arm\ embedded/8\ 2019-q3-update/bin/../lib/gcc/arm-none-eabi/8.3.1/lto-wrapper.exe
Target: arm-none-eabi
```

#### 下载调试器

下载 [openocd](http://www.freddiechopin.info/en/download/category/4-openocd) 调试器，此软件无需安装，将解压缩后的文件夹放到你想存放的目录即可。**记下存放的目录**，稍后我们会导入软件路径。

## 软件配置

#### 设置OpenOCD路径

打开 CLion ，进入 File - setting - Build, Excution, Deployment - Embedded Development（如红圈所示），CubeMX 的安装目录会自动识别，而 OpenOCD 的目录则需要手动填写，将你存放 OpenOCD 的目录输入到里面。完成以后点击 Test 验证是否成功配置

![233140.png](https://i.loli.net/2020/05/16/2q8FxynmIeKlYA5.png)

#### 在CubeMX中初始化代码

菜单栏中选择 File - New Project 创建新项目，选择 STM32CubeMX，如果你没有这个选项，请检查 CLion 版本是否过低。工程文件目录对应你希望创建的项目的位置，在这里，名为 F103ZET6 的文件夹是我用于存放这个单片机的项目的文件夹，在里面我新建一个工程，名为 temperature_mqtt_F103ZET 。为了规范归档，最好科学地为项目文件夹命名。如下图蓝色箭头所示。

![40.png](https://i.loli.net/2020/05/17/v57puCaFq9QBdcx.png)

按下 Create 键以后 CLion 会默认创建一个 STM32F030 的 STM32CubeMX 配置文件，我们首先需要修改芯片的型号，点击屏幕中央的 Open with STM32CubeMX 链接，CLion 会自动打开 STM32CubeMX 程序，CubeMX 程序界面如下图所示。

![3638.png](https://i.loli.net/2020/05/17/cltGb6RrFe9N2YS.png)

若需要修改芯片型号，点击上图左上角的 “STM32F030” 字样，将打开选型工具。选型工具界面如下所示，此处已经选择了本教程测试使用的 STM32F103ZE 芯片

![5.png](https://i.loli.net/2020/05/17/7Jde9YxZ1yGafzL.png)

选型完成后即可进行引脚配置、时钟配置等步骤，此部分请参阅 STM32CubeMX 的使用教程，本文不再赘述。随后进入到 Project Manager 页面，按如下选项配置。此时 **Project Name** 一栏应为空，填入本项目的文件夹名。**Project Location** 无需修改。**Toolchain/IDE **选择 STM32CubeIDE 或者 SW4STM32 均可用于 CLion，如果想用 Keil/IAR等其他 IDE，可在此选择对应的选项。

![YS__5~5OP4VNOF_16AMM8_F.png](https://i.loli.net/2020/05/17/xiewmYcqk6br35o.png)

完成这个步骤后，CubeMX 的任务已经完成。点击 CubeMX 界面右上角的 Generate Code 按钮生成代码， CLion 检测到代码已成功生成后，界面将显示配置已完成（如下图所示），提示代码初始化已成功完成。如果你的界面没有发生变化，那很可能是上一步中 CubeMX 中项目路径写错了，删除生成的文件重试一遍吧。

![A9OC_@_WM`KTS__2_CTV~UL.jpg](https://i.loli.net/2020/05/17/Dxog4Z5QLeSb2TI.jpg)

如果正确配置了 OpenOCD 路径，代码初始化完成后还会出现下面配置文件选择界面，此处我们先不选择，留待下面再做选择

![0R49__SMB4YIRUUE__R~GT3.png](https://i.loli.net/2020/05/17/IUloY9ESCXnQmia.png)



在初始化代码完成后，若发现之前外设功能配置得不对，也可以重新打开 项目名.ioc 文件重新配置。为了避免重新配置时用户代码被程序覆盖，应按照程序生成的代码中的注释指引在指定的位置编写代码。

```
  /* USER CODE BEGIN 1 */

  // 用户代码应在 BEGIN 和 END 中间编写
  HAL_UART_Transmit(&huart1,"Hello world!",12,HAL_MAX_DELAY);
  HAL_Delay(1000);

  /* USER CODE END 1 */
```

代码编写完成后，点击界面右上角的锤子即可编译代码生成 .elf 文件。如果不需要调试，可使用 STM32Cube Programmer 或者其他烧录工具完成将程序下载到单片机中

#### 修改/创建调试配置文件

调试单片机程序需要调试器，在 Keil 或者 IAR 等 IDE 中可以通过图形界面选择需要的调试器，但 CLion 本身并没有调试 STM32 的能力，而是要通过 OpenOCD。OpenOCD 则通过调试配置文件确定使用的调试器和目标芯片类型。打开 OpenOCD 的软件目录 *openocd-0.10.0\share\openocd\scripts* （不同版本可能有所差异），可以看到下面三个文件夹：**board, interface, target** 

**board** 文件夹存储了各家厂商官方开发板的配置文件，如果你使用的是 ST 官方出品的开发板，就可以直接使用其中的调试文件，例如 *NUCLEO*-*F103RB*（如下图） ，那么 **board** 文件夹中的 *st_nucleo_f103rb.cfg* 就是你应该选择的，其他官方开发板同理。

![Nucleo F1 board photo](https://www.st.com/bin/ecommerce/api/image.PF259875.en.feature-description-include-personalized-no-cpn-medium.jpg)

**interface** 文件夹存储了各种调试器的配置文件，包括 cmsis-dap、stlink-v2 等。**target** 文件夹则存储了各种芯片的配置文件，例如 *stm32f1x.cfg* 就对应着 STM32F1 系列。正点原子、野火等国内企业出品的开发板不属于官方开发板，自然在 **board** 文件夹中不会有他们的配置文件，因此我们需要根据自己使用的调试器和芯片，写自己的配置文件。下面是我自己使用的 F1 系列芯片的配置文件，使用淘宝卖十几块钱的盗版 ST-Link v2 调试器。

```
# st_my_F1_stlink-v2.cfg
# 文件名可以随便取，放到 board 文件夹中方便在 CLion 中选择

# 使用 stlink-v2 调试器
source [find interface/stlink-v2.cfg]

# 使用 hla_swd 调试接口
transport select hla_swd

# 目标芯片设定为 STM32F1 系列
source [find target/stm32f1x.cfg]

# 不使用复位接口
reset_config none
```

DAPLink 是 Arm 出品的开源软件项目，可对在Arm Cortex CPU上运行的应用程序软件进行编程和调试，没有盗版、掉固件等问题，还拥有虚拟串口、拖拽更新等功能，因此 DAPLink 同样是我经常使用的调试器，下面是使用 DAPLink 时的配置文件。

```
# st_my_F1_cmsis-dap.cfg

# CMSIS-DAP 和 DAPLink 其实不是同一个东西，但都使用同一个调试器配置
source [find interface/cmsis-dap.cfg]

# 使用 swd 调试接口
transport select swd

# 目标芯片设定为 STM32F1 系列
source [find target/stm32f1x.cfg]

# 不使用复位接口
reset_config none
```

如果使用其他调试器和芯片 **interface** 和 **target** 文件夹中找到对应的配置，按上述格式编写即可。如果有需要使用调试器的复位引脚，可以参考 OpenOCD 文档设置 *reset_config* 选项。

如果在一开始没有选择好调试配置文件，可以先点击红色箭头所指的位置，选择 **Edit Configurations..** ，再在蓝色箭头所指的位置选择配置文件即可。 

![0.png](https://i.loli.net/2020/07/15/BOgxNU7shPRWZTV.png)

#### 调试设置

调试功能，还需要进入到设置，在 **ToolChains** **中将 debugger 设置为 ARM-GCC 的 GDB 服务器**，如右边的红色箭头所示，否则调试无法运行。如果你平时还会使用 CLion 开发一般的 C/C++ 项目，可以创建两个工具链配置，一个作为普通 C/C++ 开发工具使用，另一个配置 arm-none-eabi-gcc 用于 STM32 的开发。

![233140.png](https://i.loli.net/2020/05/16/q5ZF6lsecUyhAiJ.png)

完成所有的配置以后，点击右上角的虫子按钮即可开始调试。与 STM32CubeIDE 开始调试后自动在 main 函数停止不同，CLion 中调试要手动添加断点才会停下来。下图展示了 Debug 状态下的程序界面，可以进行单步调试。Variables 栏中可以查看当前变量，操作均与 C/C++ 程序调试类似。

![QQ图片20200516233140.png](https://i.loli.net/2020/05/16/Gmt9NQ5Hlbh617Z.png)

#### 寄存器调试

有时候我们还希望能够直接查看 STM32 单片机各寄存器的值，方便在寄存器层面进行调试。OpenOCD 同样提供了这个功能，调试界面中 Peripherals 栏即为寄存器描述的区域（下图红色箭头所指）。但是此时点开，只会看到一条 "svd file is not loaded" 的提示。这是因为 OpenOCD 并不清楚单片机内部的寄存器配。需要到 ST 官网下载到对应芯片的系统视图描述（SVD）文件，导入后才能正常显示。对于 STM32F1系列的单片机，可在[此处](https://www.st.com/content/st_com/zh/products/microcontrollers-microprocessors/stm32-32-bit-arm-cortex-mcus/stm32-mainstream-mcus/stm32f1-series/stm32f103/stm32f103ze.html#)获取。其他系列单片机文件 SVD 文件也同样可从官网获得。导入完成后，寄存器显示效果如下

![20200516234849.png](https://i.loli.net/2020/05/16/ZiBGgXhAwTK8uL3.png)

至此，我们已经完成了整个软件配置过程。若对本文有任何的疑问和建议，欢迎通过评论区或者邮箱与我联系。