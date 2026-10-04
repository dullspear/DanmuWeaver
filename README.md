<p align="center">
  <img width="18%" align="center" src="https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202409231714145.png" alt="logo">
</p>
  <h1 align="center">
  弹幕编织者
</h1>

<p align="center">
  基于 phash/DTW 计算弹幕偏移时间
</p>
<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win%20|%20Linux%20-blue?color=#4ec820" alt="Platform Win32 | Linux | macOS"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
  </a>
</p>



### 介绍

你愿意忍受观看阉割版本的番剧/电影吗，你或许可以选择第三方网站，可是又舍不得放弃丰富的弹幕资源。

这个程序可以帮助你既能够观看完整视频，又可以使用移植来的弹幕资源。



### 输入

你只需要三个文件：（需自行下载）

1.完整的未阉割的视频（以下简称long）

2.被阉割/和谐过的视频（以下简称short)

3.和谐视频的弹幕（以下简称short_danmu)



### 输出

本程序将输出一个ass类型弹幕文件（以下简称long_danmu.ass)

重要的是，无论short如何剪切，本程序都能较为稳定的得出short与long的映射，从而根据该映射生成 long_danmu.ass。





![image-20240922223242804](https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202409222232993.png)





### 原理

1.下载原视频（以下称为L视频），和谐视频（以下称为S视频），以及和谐视频对应的弹幕（S弹幕）2.通过感知哈希函数对每一帧进行计算
3.进行dtw运算，得出最优路径
4.根据最优路径的映射关系，生成新弹幕
5.加载至完整视频


### 自行编译

使用 uv 管理依赖，在仓库根目录运行：

```bash
uv run python -m src.frontend.gui.gui
```

您也可以直接使用release中已经打包好的exe程序。


### 观看
推荐使用potplayer等可以加载弹幕的视频播放器。首先加载`字幕`（作为下方的中文字幕），然后加载`次字幕`作为上方弹幕。 

### 参考

[DTW（动态时间规整）算法原理与应用_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV12r4y1A7mT/?spm_id_from=333.788&vd_source=df034c933ea08326f3a58a38fa1c7fce)
 [鸣梦 - 博客园 (cnblogs.com)](https://www.cnblogs.com/HoEn/)







### 许可证

使用 GPLv3 许可证.

Copyright © 2023-2024 by dullspear

