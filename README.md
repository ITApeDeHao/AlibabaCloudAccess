# 物联网基于python云平台的接入

[TOC]



# 1．设计目的

学习使用云平台记录收集设备数据反馈给用户端，实现物联网与云平台的连接，了解物联网与云平台的关系以及实现流程。

# 2．功能要求和关键问题

## 2.1 系统功能描述

1、设计一个图形用户界面，来实现文本数据或二进制数据（比如图像文件或者音频文件等）的双向传输。

2、将接受的数据展示在图形界面或打开。

3、登陆注册系统

## 2.2复杂工程问题分析

将本地与云平台相连，传输数据和接收数据。通过来自阿里的python第三方库linkkit进行连接。用base64库对接收数据进行编码转码以便传输，这里接收后要将字符串转变为字节流写出。

首次连接设备与云平台时无法正常接入，通过继承重构官方文档给的三方库函数，得以解决实现正常上传。根据官方帮助文档创建消费组订阅但是我将双向传输连接在一个设备的一个订阅中，连接造成冲突，云与设备一直重复上线下线操作，后来想到类似于QQ的登录顶号意识到需要走两条线路进行传输。

思考用户如何将接收到的数据展示在图形界面时，起初我的想法是直接将数据解码展示，但是展现的只是数据的文本信息，并不能将图片展示，所以创建了一个目录用于存放接收到的临时数据，每次连接阿里云都将重置该目录下的文件。且每次传输都会覆盖上次传输的数据。

# 3．系统整体框架设计

总体设计分为五大模块：PC端接收和发送、设备端发送与接收、登陆注册。

两端分别连接登陆窗口与收发系统，将云消息暂时存储在本地计算机以显示在图形界面或打开观看，并且在每下次连接时清空暂存信息。

 

# 4．模块的设计和实现

## 4.1 阿里云基础和设计

### 4.1.1 阿里云概述

阿里云物联网平台是一个集成了设备管理、数据安全通信和消息订阅等能力的一体化平台。向下支持连接海量设备，采集设备数据上云；向上提供云端API，服务端可通过调用云端API将指令下发至设备端，实现远程控制。

### 4.1.2 阿里云应用设计

在阿里云平台创建一个初始化产品，并赋予其四大功能如图1所示，后续开发皆需

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image002.jpg)

图 创建产品与定义功能

围绕展开。在此基础上，分别创建两个设备即对应PC端与设备端，以便后续可以进行相互传输如图2所示.

 

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image004.jpg)

图2 创建两个设备

在规则引擎中选择服务端订阅—>消费组列表—>创建两个消费组（依然是为了能够实现双向传输）—>订阅列表—>创建订阅（如图3-图5所示）

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image006.jpg)

图3 创建订阅

 ![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image008.jpg) 

图4 消费组信息

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image010.jpg)

图5 订阅产品信息

至此，阿里云平台设置暂时告一段落

## 4.2 PC端与设备端

两个端口实现数据相互传输，大致内容相同，只需连接不同的阿里云平台设备即可，所以此后内容主要以设备端开发详细讲解

### 4.2.1 PC端

即用户端，用户可以接收到设备发送的数据，并记录下来。

 

### 4.2.2 设备端

设备端即用户不可见端，向用户传取数据以便用户可以获知所需要的信息数据。   

## 4.3 图形界面开发

### 4.3.1 登陆窗口界面

用户凭据用户注册信息，可以在数据库中找到对应的用户信息以便识别信息，并且为用户提供连通注册界面的按钮，以便存入用户身份方便下次使用。如图6所示

 

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image012.jpg)

图6 登录界面窗口

### 4.3.2 注册窗口界面

用户通过此界面可以向数据库发送创建信息，以获取拥有向PC端发送信息的权力，主要作用为连接数据库，从数据库中查找是否用户名冲突和写入用户身份信息的作用，如图7所示

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image014.jpg)

图7 注册界面

### 4.3.3 数据传输窗口界面

此界面即为我们本次开发的主要窗口界面，主要提供了连通阿里云物联网平台和向PC端发送信息选择功能与数据接收并展示在图形界面的功能如图8所示

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image016.jpg)

图8 传输数据窗口

PC发送数据，设备端收入并显示是如图9和10（打开音频播放软件）所示

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image018.jpg)

图9 接收传输的数据

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image020.jpg)

图10 接收音频

 

## 4.4 阿里云数据上传和保存

### 4.4.1 从设备端上传到云平台

分别通过界面中选择不同类型的数据上传到阿里云平台后，可在云平台中看到数据和PC端本地查看到暂时数据，如图11所示（视频因数据量过大，网速原因上传时间较长，容易造成卡顿，所以此处将接口关闭，如果想到改善方法取消注释即可连通此处接口）

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image022.jpg)

图11 阿里云平台接收信息

 

### 4.4.2 PC本地获取云平台信息

PC设备通过下载云平台数据判断文件类型，写入到本地磁盘后，并且在每下词连接阿里云时进行数据清空。如图12所示

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image024.jpg)

图12 本地暂存信息

# 5. 调试和运行结果

### 5.1碰到的问题和解决方案

起初，可以正常连接阿里云平台，但无法将数据如我们预期一般正常传输上去，通过改进判断方式，将字节流数据转为字符串。后续出现获取信息时字符串转字节流数据错误，对字节流进行了base64编码。

但与此同时出现新的问题，base64.b64decode解码只能对4的倍数的字节流进行编码，在外网中找到一个解决方案使用base64.urlsate_b64encode编码会自动进行填充“=”使字节流的长度为4的倍数。

 

### 5.2运行结果

PC和设备端分别打开登陆窗口界面完成登陆。

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image026.jpg)

图1左图为PC窗口，右图为设备窗口

（后续图片皆是如此）

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image028.jpg)

图2 注册窗口界面

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image030.jpg)

图3连接阿里云平台

![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image032.jpg)

图4选择向PC发送的数据![img](file:////Users/dehaomeng/Library/Group%20Containers/UBF8T346G9.Office/TemporaryItems/msohtmlclip/clip_image034.jpg)

图5 PC端获取到的数据展示在图形界面中

 

# 6．心得体会

基于python的云平台的接入我是第一次接触，完全从零开始，在此之前并不了解云平台的概念，本次课设又恰巧收考试周影响，做的内容差强人意，但是基本实现了相互传输的功能。寒假在将其修改补进再深入了解一下这个概念。

本次课设的要点在于如何接入云平台，并且理解云平台的概念。运用云平台的传输方式和存储方式大大降低了硬盘的内容空间损耗，并且实现了物联网设备与用户的互通，将实时数据通过网络发送到PC用户端，可以更快的，更便捷的让用户不在时刻为某件事而担忧。物联网云平台强化设备与产品的概念。用户通过订阅和设备发布的形式进行数据交互。将数据上传后的开发便容易的多。

我一开始觉得这个课设并不会多难，但是当真正上手后发现对云平台的陌生使得本应该很快完成的我一误再误，从阅读官方文档到整合官方代码这一点事就耗费掉了我大约两天的时间（期间有考试和复习）。所以目前只实现了三种数据的传输，后续我会完善优化视频数据传输，增加一些输入与反馈功能。

大量的阅读他人的优秀代码对于改进自己的“垃圾堆”有的极其有效的帮助，并且一定要在书写代码时，时时刻刻保持良好习惯，我在此次开发过程中深受其害，只是一个小小的变量名使得我的传输数据和接收数据彻底混乱以致我不得不回退代码以及写完之后不得不进行重构函数。

不得不提一句图形界面的开发尽量避免使用tkinter吧，实在太难开发了……，踩到的坑是一个接一个。不过在此次开发中又新学到许多三方库的搭建和组合使用。

希望能看到这篇文章的同学吸取不良习惯的教训，提前培养好习惯。