---
title:  利用 Termux 在安卓上搭建 JupyterLab
date: 2020-02-20
tag: [教程, Linux, Jupyter]
authors:
    - name: LYF
---
<!--more-->
## Termux与JupyterLab简介
Jupyter lab是Jupyter Notebook的进化版，是一个基于Web页面的集成开发环境。可以在本机使用，也可以在远程服务器部署后使用。但Jupyter Lab有一个缺点就是需要加载的资源很多，对于带宽费用极高的云服务器来说并不适合。Termux是一个Android下一个高级的终端模拟器,可以在Android设备上拥有类似于使用Linux系统的体验。因此我萌生了在老手机上部署Jupyterlab后，使用局域网连接使用的想法。一方面局域网不需要担心带宽问题，另一方面手机也拥有相当的便携性，可以打造一个移动的JupyterLab。

## Termux的安装与基本配置
Termux程序可以在Google Play或酷安下载，在本部分中，我着重参考了[国光大佬介绍的Termux配置方法](https://www.sqlsec.com/2018/05/termux.html#toc-heading-1)。这个帖子还介绍了很多Termux的使用方法，有兴趣可以自行尝试

1. 打开Termux程序
![img](../image/Termux/1.jpg)

2. 安装必备的一些工具,如果不使用代理，则进行这一步之前最好修改清华源
   
        pkg install wget curl git unzip unrar

3. 安装screenfetch与查看系统
        
        pkg install screenfetch
        screenfetch
    

![img](../image/Termux/1%20(3).jpg)

4. 进行界面优化和存储映射，这一步手机会提示授予权限，输入完两个数字以后，输入exit重启Termux

        sh -c "$(curl -fsSL https://github.com/Cabbagec/termux-ohmyzsh/raw/master/install.sh)"  
        Enter a number, leave blank to not to change: 14
        Enter a number, leave blank to not to change: 6
    

界面优化后的效果图
![img](../image/Termux/1%20(5).jpg)

5. 安装模拟root环境的工具，这里使用的是proot，如果你的手机已经root了的话，使用tsu

        pkg install proot

## 安装与配置Jupyter Lab
1. 安装Python
        
        apt-get update
        pkg install python

2. 升级pip
   
        pip install --upgrade pip
    
3. 安装jupyterlab

        pip install jupyterlab

4. 生成配置文件

        jupyter lab --generate-config

5. 修改juyter lab开启的ip
        
        cd .jupyter
        vim jupyter_notebook_config.py

由于我手机在局域网中的ip是192.168.1.3，因此如下图一样修改。修改完成以后切记将这行的注释#去掉。为了保证每次重连WiFi时ip不会改变，最好在路由器中将ip和手机的mac进行绑定或者使用静态ip（不推荐，因为可能导致无法上网）

![img](../image/Termux/1%20(18).jpg)

6. 设置密码

        jupyter notebook password

7. 在浏览器中输入192.168.1.3:8888，即进入到Jupyter Lab界面

## Python包的配置
只有一个Python运行环境是远远不能满足需求的，还需要安装大量的软件包。这一部分可以说是Termux配置Python中最麻烦的地方，经常出现各种错误。在这一部分我重点参考了[安卓termux折腾手记：安装python库+tasker调用](https://www.jianshu.com/p/c239a7eaadba)。在这一步当中，系统版本等因素都可能会影响安装，出现错误时可以先仔细阅读错误信息，看下是不是因为缺少某些必须组件导致。其次可以尝试安装低版本。

1. pip安装numpy总是失败，因此我也不折腾了，直接使用下面的方法

        curl -L https://its-pointless.github.io/setup-pointless-repo.sh | sh
        pkg install numpy
        pkg install scipy
    
2. pip安装pandas，这一步需要较长时间
   
        pip install pandas
    
3. 安装爬虫库

        pip install requests BeautifulSoup4
        apt-get install libxml2 libxslt
        pip install lxml
        apt install clang libffi openssl
        pip install scrapy

4. 安装Matplotlib，这一步同样需要比较长的时间
   
        pip install matplotlib

安装完成。

## 启动Jupyter lab
完成安装后，启动Jupyter lab

    jupyter lab

打开浏览器，输入192.168.1.3:8888

![img](../image/Termux/2.png)

Jupyter lab已经成功运行
