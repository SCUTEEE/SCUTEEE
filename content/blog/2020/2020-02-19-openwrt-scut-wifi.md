---
title:  OpenWrt 系统路由器搭建宿舍 WiFi
date:   2020-02-19 18:42:00 +0800
tags: [教程, 生活, Linux]
comment: true
authors:
  - name: ToddZ
---

> 方便宿舍多台设备使用校园网。适用于所有能跑 OpenWrt 的路由器。

<!--more-->

# 2022/03/09 更新

网络上已经有预编译好的 `scutclient.ipk`，我们无需自行编译，只需要根据自己的处理器架构，到 `https://op.supes.top/packages/` 中对应的文件夹里搜 `scutclient`，然后安装即可（先安装 scutclient，再安装 luci-app-scutclient）。不知道处理器架构的，可以运行该命令来查看：`cat /etc/openwrt_release | grep DISTRIB_ARCH`。下载得到 .ipk 文件，然后上传到路由器，用 `opkg install [文件名]` 来安装。安装好后，可以用网页端，或按后面的“登录校园网”一节来操作。

-----

# 声明

本教程仅供技术交流，不希望触动学校的利益，不对架设宿舍 WiFi 的行为负责。

# 准备

* 一台装有 OpenWrt 的路由器（任何 OpenWrt 版本都行，我买的是 NetGear 的），或者软路由+普通路由器
* 校园网账号
* 网线
* 一台装有 Linux 的 x86_64 设备（电脑/虚拟机/服务器，我在教程中用的是9元的阿里云服务器，如果你都没有，可以通过E-mail：todd310378072@outlook.com 联系一下我）
* ssh软件（如果没有，文末有推荐软件）



# 一点预备知识

## SSH

ssh 是一种协议，我们可以通过ssh软件登录到路由器，然后通过输入命令来操作路由器。

## WAN

WAN，Wide Area Network的缩写，即代表广域网。通过这个连接到学校的网络。

## LAN

LAN，Local Area Network的缩写，即局域网。手机等通过这个连接到路由器。

## 交叉编译

交叉编译是在一个平台上生成另一个平台上的可执行代码（软件）。





# 交叉编译and部署

由于 OpenWrt 路由器并没有 cmake 和 make，所以需要先在 Linux服务器上编译好后，再部署到路由器上。

先通过 ssh 连接路由器，然后输入：

```bash
cat /etc/openwrt_release
```

然后会显示一些信息，这是我的：

```bash
DISTRIB_ID='OpenWrt'
DISTRIB_RELEASE='18.06.1' #重要！
DISTRIB_TARGET='ar71xx/nand' #重要！
DISTRIB_ARCH='mips_24kc'
DISTRIB_TAINTS='no-all'
DISTRIB_REVISION='R8.1.11 By Lean'
DISTRIB_DESCRIPTION='OpenWrt'
```



如果版本不是 `18.06.1`，或者不是`ar71xx`，那你需要自行找相应的 target 来编译；如果是，ssh 切换到 Linux服务器，输入：

```bash
wget https://downloads.openwrt.org/snapshots/targets/ar71xx/generic/openwrt-sdk-ar71xx-generic_gcc-7.4.0_musl.Linux-x86_64.tar.xz
```

> 注：由于 openwrt每年都会更新，所以上面那个文件不存在的话，去 [https://downloads.openwrt.org/](https://downloads.openwrt.org) 找最新的来替换。

下载好后，解压并进入相应目录：

```bash
tar -Jxvf openwrt-sdk-ar71xx-generic_gcc-7.4.0_musl.Linux-x86_64.tar.xz
cd openwrt-sdk-ar71xx-generic_gcc-7.4.0_musl.Linux-x86_64
```

然后新建目录：

```bash
mkdir package/scutclient
```

从 [https://github.com/scutclient/scutclient](https://github.com/scutclient/scutclient) 下载仓库里面的 /openwrt/Makefile 文件（貌似只能全部下载再解压？），然后放到上面新建的目录里面。

然后运行：

```bash
make defconfig
make package/scutclient/compile V=s
```

如果出现错误，可能缺少什么软件（比如我是缺少一个 gawk 和 ccache），或者上面的 sdk 有错（我前几次都编译失败，换了那个 sdk 才成功），这个请自行分析错误信息来解决。

编译好后，将编译好的 ipk 文件（在 bin 文件夹里）放到openwrt路由器里，然后通过 `opkg install [文件]` 来安装。



# 登录校园网

首先需要设置好 wan ，设为静态ip，然后将“校园网-个人信息”里的那些 ip、mac、网关填上去。 

将路由器插上网线，然后在 ssh 中输入下面命令连接校园网：

```bash
scutclient --username <username> --password <password>
```

上面那个大概率会出错，因为需要指定是哪个 WAN 口：

```bash
scutclient --username <username> --password <password> -i <wan>
```

如果你不知道是哪个，就用 `ifconfig` 查看，然后都试一次。

如果成功的话，就可以将这个命令挂到后台：（先 ctrl + c 停止正在运行的命令）

```bash
nohup scutclient --username <username> --password <password> -i <wan>
```

由于每天都会断网，所以早上起来时需要重新运行这个命令。你可以将该命令放到一个定时运行的文件中。（具体方法百度）



# 配置 wifi

这个就不用说了，wifi 名随便写，最好不要写自己宿舍号（也不要~~像我那样~~写其他宿舍号），担心学校有人查，如果能隐藏 wifi 就最好了。



# 谷歌学术

淘宝店帮忙刷的openwrt 大概率会安装 Shadowsocks，比如我的就安装了 ShadowsockR Plus +。如果你的没安装，自己上网找教程。我说一下大概的配置：

* 添加ss服务器（就填好ip、端口、密码就行），启用“TCP快速打开”和“自动切换”
* 客户端，主服务器就选添加的服务器，运行模式选 GFW，其余可以不变
* 保存并启动



# 推荐软件

如果你没有 ssh，我推荐两个：

* 手机端：ConnectBot
* 电脑端：MobaXterm
