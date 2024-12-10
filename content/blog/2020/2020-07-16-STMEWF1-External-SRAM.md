---
title: STM32F103 的外部 SRAM 测试记录
date: 2020-07-16
tags: [stm32] 
authors:
  - name: LYF
---

最近准备给 F103 的板子加一块屏幕，考虑到可能有比较大的内存需求，就稍微研究了一下使用 FSMC 接口的外部 SRAM 操作，并实现了 `SRAM_malloc()` 和 `SRAM_free()` 两个函数用于动态内存分配，并在 arm-gcc 编译环境下通过了简单的验证，在此撰文记录。本工程代码尚处于测试阶段，代码可能存在丑陋的写法/隐藏的 bug ，欢迎通过评论和邮件提出意见。

<!--more-->
# STM32F103 的外部 SRAM 测试记录

### 实验平台

硬件平台: 正点原子 STM32F103 小型系统板，板载 XM8A51216V 异步 SRAM

开发工具链: CubeMX 5.6.1 + CLion 2020.1.2 + arm-none-eabi-gcc 2019-Q4

硬件调试器: DAPLink

### STM32F103ZE FSMC 简介

基于 ***RM0008_ZHV1***    STM32F1 系列 ARM 内核 32 位高性能微控制器参考手册

STM32F1 系列的**大容量**产品拥有灵活的静态存储器控制器(FSMC)，可以于同步/异步存储器通信，包括 SRAM, ROM, NOR FLASH, PSRAM。FSMC 外设地址被映射到 0x6000 0000~0x9FFF FFFF，共 1GB 空间。这 1GB 空间被分为四块，分别分配给 NOR/PSRAM, NAND FLASH 和 PC 卡。NOR FLASH/PSRAM 对应的块又被分为四块，每块各 64MB ，如下图所示

![image-20200716170128777.png](https://i.loli.net/2020/07/16/gMzZ7pjLd59Ulo8.png)

对于本次实验使用的存储块 1 而言，划分出来的四个区均能被单独的片选选中。开发板外部 SRAM 的片选引脚已经被接到 FSMC_NE3 引脚，因此我们使用 NOR/PSRAM 块的第三区。总共使用 19 条地址线，16 条数据线。

### 在 CubeMX 中配置 FSMC

由于使用的是 SRAM 芯片而非很多开发板使用的 SDRAM，无需进行刷新操作，省去了相当多的配置工作，只需在 CubeMX 中选择好地址线、数据线宽度，根据芯片数据选择地址建立时间、数据建立时间和总线回复时间，使能写操作即可（此处还有要注意的地方，下面会说），其他时钟配置、Debug配置不再详述。

![image-20200716153625723.png](https://i.loli.net/2020/07/16/GwXUIbgc6SahK4m.png)

### 直接通过指针操作 SRAM

FSMC 外设配置完成以后，NOR/PSRAM 块的第三区就被映射到了 `0x6800 0000` 这一段内存上面，可以直接通过指针访问。这里我仿照正点原子例程的做法，定义了 SRAM 写函数和 SRAM 读函数。

```
#define Bank1_SRAM3_ADDR (uint32_t)0x68000000

void FSMC_SRAM_WriteBuffer(uint8_t *pBuffer,uint32_t WriteAddr,uint32_t n)
{
    for(;n!=0;n--)
    {
        *(volatile unsigned char *)(Bank1_SRAM3_ADDR+WriteAddr)=*pBuffer;
        WriteAddr++;
        pBuffer++;
    }
}

void FSMC_SRAM_ReadBuffer(uint8_t *pBuffer,uint32_t ReadAddr,uint32_t n)
{
    for(;n!=0;n--)
    {
        *pBuffer++=*(volatile unsigned char *)(Bank1_SRAM3_ADDR+ReadAddr);
        ReadAddr++;
    }
}
```

相当简洁明了的操作：用一个指针指向外部 SRAM ，再通过指针操作外部 SRAM 中储存的内容。但是，我们的外部芯片数据宽度是 16bit ，为何使用的是 `uint8_t` 数据类型？既然正点原子是这样写的，那先运行一下看看是什么效果吧。

```
uint8_t info_temp[100];
sprintf(info_temp,"Card ManufacturerID:%d\r\n",pCID.ManufacturerID);

FSMC_SRAM_WriteBuffer(info_temp,64,100);
uint8_t SRAM_Read[100];
FSMC_SRAM_ReadBuffer(SRAM_Read,64,100);
```

`pCID.ManufacturerID` 表示 SD 卡的厂商 ID ，在这里并不重要，只需要知道我们将一个字符串拷贝到 SRAM 当中就可以了。通过调试窗口可知，`info_temp` 正确存储了字符串，但 `SRAM_Read` 则很有问题。

```
info_temp    Card ManufacturerID:3
SRAM_Read    aaddMMnnffccuueeII::
```

显然是由于某些原因，相邻地址被写入了同样的内容。查阅参考手册 19.4.1 NOR和PSRAM地址映像，发现了下面的表述。

```
(1) HADDR是需要转换到外部存储器的内部AHB地址线。 
HADDR[25:0]包含外部存储器地址。HADDR是字节地址，而存储器访问不都是按字节访问，因此接到存储器的地址线依存储器的数据宽度有所不同，如下表：

数据宽度(1) 连到存储器的地址线                                    最大访问存储器空间(位) 
8位        HADDR[25:0]与FSMC_A[25:0]对应相连                    64M字节 x 8 = 512 M位 
16位       HADDR[25:1]与FSMC_A[24:0]对应相连，HADDR[0]未接       64M字节/2 x 16 = 512 M位

(1) 对于16位宽度的外部存储器，FSMC将在内部使用HADDR[25:1]产生外部存储器的地址FSMC_A[24:0]。不论外部存储器的宽度是多少(16位或8位)，FSMC_A[0]始终应该连到外部存储器的地址线A[0]。
```

使用 16 位宽度的存储器时，FSMC 的内部地址线最低位将不接，那是否意味着指针自增应自增 2 而非 1 呢？正点原子的教程中是这样解释的。

```
是因为我们这里用的数据宽 8 位，通过 UB 位和 LB 位来控制高低字节位，所以地址在这里是可只加 1 的
```

UB 和 LB 又是什么？翻了一下 FSMC 的 HAL 库文件并没有发现，参考手册也没有提及。通过查阅网络资料和开发板原理图，才发现这两个指的实际上是 FSMC 的字节信号引脚 NBL[1:0]，CubeMX 生成代码时并不会自动配置，FSMC 外设配置中也没有相关的内容，只能直接在引脚分配图上手动添加，如下图所示。事实上，即便手动添加了这两个引脚，从代码上也只能看到 GPIO 口的配置内容，尚不清楚这两个引脚究竟如何发挥作用。总而言之，通过字节信号， FSMC 外设可以控制高低字节的访问，实现地址连续的、单字节的 SRAM 读写。

![image-20200716163911818.png](https://i.loli.net/2020/07/16/J35CBs7VyX1tdlT.png)



### 动态内存分配

直接使用指针访问内存在内存用量不大时是可行的，但如果内存用量变大时，可能会出现越界等问题，因此有必要建立内存管理。正点原子有专门的工程实现了分块式内存管理，然而，arm-gcc 并不支持将变量定义到绝对地址的操作 `__altribute(at(Address))` ，干脆自己重新做一套新的。目前的版本只针对外部 SRAM 进行动态分配，内部 SRAM 靠编译器处理，使用 32KB 内部 SRAM 作为外部 SRAM 的内存表（确实有点太大了，不过可以通过提高单块分配大小来缩小内部 SRAM 的占用，未来也会考虑将内存表移到外部），实现了 `SRAM_malloc()` 和 `SRAM_free()` 两个函数，源码如下：

```
#define SRAM_BLOCK_SIZE 32          // 最小分配 32Byte 的外部 SRAM
#define SRAM_ADDRESS 0x68000000
#define SRAM_END_ADDRESS 0x68100000

uint16_t SRAM_BLOCK_NUM = (1024*1024)/SRAM_BLOCK_SIZE;
uint8_t SRAM_MAP[32768];

void SRAM_MAP_Init(){
    for(uint16_t i = 0;i<SRAM_BLOCK_NUM;i++){
        SRAM_MAP[i]=0;
    }
}

// 申请分配 size 字节的内存
void *SRAM_malloc(uint32_t size){

    if(size==0) return NULL;

    // 计算需要分配的内存块数
    uint16_t num = size/SRAM_BLOCK_SIZE;
    if(num%SRAM_BLOCK_SIZE) num++;

    uint16_t continuous_empyt_block_num = 0;
    for(uint16_t offset = SRAM_BLOCK_NUM-1;offset>=0;offset--){
        if(SRAM_MAP[offset]==0){
            continuous_empyt_block_num++;
        }
        else{
            continuous_empyt_block_num=0;
        }
        if(continuous_empyt_block_num==num){
            for(int i =0;i<num;i++){
                SRAM_MAP[offset+i]=num;
            }
            return (SRAM_ADDRESS+offset*SRAM_BLOCK_SIZE);
        }
    }
    return NULL;

}

void SRAM_free(void *ptr){
    if(ptr==NULL)return;
    // 超出外部 SRAM 的范围
    if(ptr > SRAM_END_ADDRESS)return;

    // 计算地址所属内存块
    uint16_t block = ((uint32_t)ptr-(uint32_t)SRAM_ADDRESS)/(uint32_t)SRAM_BLOCK_SIZE;

    // 获取该地址共分配了多少块内存
    uint8_t num =SRAM_MAP[block];

    for(int i = 0;i<num;i++){
        SRAM_MAP[block+i]=0;
    }

}
```

