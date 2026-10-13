---
title: '[TSCTF-J2026]文字的秘密 - 出题人WP'
date: 2026-10-14 03:25:13
tags:
---

<!-- # 文字的秘密 出题人WriteUp <span style="font-size: 0.6em">by 圆周率</span> -->

<a href="文字的秘密 - 出题人WP.pdf">点击此处访问PDF版</a>

## 选手视角

### 1.png

这个是常见（？）人造文字的考察，如果你玩过今年三月的腾讯新游《洛克王国：世界》，那就应该不难认出这是其中的人造文字。接下来只要搜索“洛克王国 人造文字”就可以找到对照表了~

![alt text](image.png)

什么，你说你没玩过……那就只能参照2.png的解法了，不过好在这个人造文字是基于历史真实存在的文字（卢恩文字/Runes）稍加修改完成的，还是有点像英文字母的，连蒙带猜应该也能出（？）

![alt text](image-1.png)

按照对照表，我们可以还原如下文本：

![alt text](1.png)

```
1. Wooden coat wrapped around a graphite(n. 石墨) core, sharpened it writes clear words.
2. Transparent glass set in a frame, letting light and glances pass through.
3. Four legs support a seat, and a back lets you lean comfortably.
4. In rainy days it spreads a patch of dry sky over your head.
5. Coiled(v.-ed 卷，盘) fine strand(n. （线、绳的）一缕), able to string(v. 串) scattered beads(n.pl 珠子) into a bracelet(n. 手链).
6. Hint: last line of the three pictures are tips.
```

然后我们就可以得到前五个问题的答案：`pencil`、`window`、`chair`、`umbrella`、`thread`

### 2.png

这个很明显没有已知映射可以找到，所以我们就要自己根据英语的特点去猜出映射关系

首先是最特殊的情况：单字母成词，在英语中一般情况下能单字母成词的只有`a`和`I`，所以我们可以断定图像中单独出现的就是字母A

然后根据1.png的提示，可以大胆猜测最后一行的开头是`hint`（当然了，你也可以留个心眼，可能是`tips`也说不定，但接下来可以看到有`in`的组合而不可能是`ip`从而排除）

![alt text](2-1.png)

然后我们能猜到不少词：`[w]ith`、`han[g]in[g]`、`an[d]`、`[s]ta[r]t[s]`、`th[e]`

![alt text](2-2.png)

继续，发现：`wa[l][l]`、`with[o][u]t`、`e[v]er[y]`

![alt text](2-3.png)

![alt text](2-4.png)

最后可以还原如下文本：

![alt text](2.png)

```
1. Moves a slider along two rows of teeth, it makes garments(n.pl 衣服) open or close.
2. Small tubular(adj. 管状的) thing, blow into it and a shrill(adj. 尖锐的) note comes out.
3. Soft block with a gentle wipe, pencil marks vanish without a track.
4. A folded paper pouch(n. 小袋子), with a stamp it starts a journey.
5. Round-faced and mute, hanging on a wall, it announces the hour precisely.
6. Hint: every answer is in English lowercase.
```

可以得到中间五个问题的答案：`zipper`、`whistle`、`eraser`、`envelop`、`clock`

顺带提一嘴`hint2`，里面写明是出自莎士比亚的一句著名台词，应该很容易想到To be一句，对照一下有将近一半映射表出来，再进行推断应该就是随随便便了

### 3.png

仔细观察这个人造文字的特征，不难发现其大致可分为几部分，搭配种类很多，但每部分类型不算很多，结合最后一行冒号前仅有两个文字，可以大胆猜测这是基于汉语拼音的一种人造文字

但是这个来源实在是比较偏，如果没找到就只能启用hint3了

![alt text](image-2.png)

[https://www.omniglot.com/conscripts/zhonghuayuzi.htm](https://www.omniglot.com/conscripts/zhonghuayuzi.htm)

下面通过hint3分析规则

整体思路是分析相似之处，判别相异之处：

不难注意到“凄凄惨惨戚戚”的“凄凄”与“戚戚”对应文字完全一致，印证了我们的猜想，然后注意到“冷冷清清”的“清清”(qīngqīng)与“戚戚”(qīqī)文字类似，拼音仅差尾部-ng，可以猜测尾部的作用是标注鼻音，还有两种奇怪的尾，一个仅在“儿”上出现，另一个似乎做-i用；

然后注意到“乍暖还寒时候”的“还”(huán)“寒”(hán)、“到黄昏”的“黄”(huáng)“昏”(hūn)的半边是一致的，说明这半边是声母，剩下的图标就是韵(介)母部分

剩下就是尾的位置，由于拼音仅剩下声调没有表示，所以尾的位置就代表声调

下面贴出原版的对照表，我在这个表的基础上做了少量修改，不影响使用

![alt text](image-3.png)

接下来就是按照对照表翻译问题了

![alt text](3.png)

```
1. 圆骨绕轴转，托车身行千里。
2. 扁圆小片，穿扣眼，合衣襟。
3. 方盒握掌，拨号通远方。
4. 亮面无言，却能映出眼前万物。
5. 铁头安木柄，挥下钉入木。
6. 提示：啊咧？这个好像是一个表音文字呢！
```

得到最后5个答案：`wheel`、`button`、`phone`、`mirror`、`hammer`

### secret.ttf

通过最终的密码，我们可以来到最后一关

最后一关给了一个字体文件，这里可能需要一些脑鬼才可以和出题人对上脑电波，不过如果公布了提示，那就比较简单了，查看`portal.html`的源码，我们可以看到给字体设置了`font-feature-setting`，所以可以想到连字

![alt text](image-4.png)

使用FontForge或类似软件查看字体连字表，发现一个叫`flag`的feature，有两条连字规则：

![alt text](image-5.png)

1：将“咒语”`In the name of PiYuanZhouLv, please give me the flag!!!`替换为Glyph`where_is_the_flag`

![alt text](image-6.png)

2：将Glyph`where_is_the_flag`替换为flag

接下来就是把flag还原就结束辣~

## 出题人视角

本题承接宣讲提到的“人造文字”话题，深挖了关于人造文字的几种破解方式， ~~另外由于当前LLM视觉能力较弱，也作为反一把梭的尝试，考察选手自身水平。~~ 并非，还是被AI大人梭了

灵感来源是`2026XCTF-SCTF · Let's dance together!`，那一题考察了几个人造文字，刚好招新预热宣讲结束不久，还真就考察了来自原神的“稻妻文”

![alt text](saiti1.png)

另外还有一个来自动漫的人造文字（由浓度这么低的我看人物剪影想到是哪部真的好吗喂）

![alt text](saiti2.png)

最后一个人造文字实在没有找到，于是根据主题锚定了几个核心词，进而推出了整个对照表，觉得适合作为一道题，于是就有了这道题。

![alt text](image-7.png)

首先第一题考察常见人造文字，但也不能太常见，不然就送了，所以考察了今年的新游中的人造文字；

第二题考察未知人造文字，所以就是从Nerd Font中的图标中随机选了26个，组成映射表；

第三题本来计划考察汉语相关未知人造文字，但是意外让我看到了一个不错的模子，就考察检索能力了，不过考虑到要是没人找到就不好了，于是预留了`hint3`的声声慢，就可以当作未知人造文字做了；

最后的连字是我偶然想到的，为了这个，还研究了一段时间FontForge怎么用……

`hint1`也废了我一点时间，一开始使用PBKDF2HMAC的，但是还是怕爆破，为了尽可能抗爆破，询问AI后改用argon2，并且保证答案至少有5个字母，但是估计还是没法防止常见词字典爆破，所以最后是否放出`hint1`也是一个问题

最后的咒语本来是想混合使用中英文的，结果TrueType竟然不支持多语言间连字，只能回到纯英文的咒语

这道题最后定位为`7/10`，是在没有放出提示的情况下的难度，如果放出了hint，估计要到`5/10`左右，看看有没有选手愿意吃罢（x

### 附：中华语字规则 - 圆周率修订版

首先写出拼音，轻声无法表示，建议改回原音（我简单处理为一声）

根据[《汉语拼音方案》](http://www.moe.gov.cn/ewebeditor/uploadfile/2015/03/02/20150302165814246.pdf)（新华字典上也有）还原原始读音，如：`yīn -> īn` `wàn -> uàn` `yuán -> üán` `niú -> nióu`

![alt text](image-8.png)

套用[原始作者提出的对照表](https://www.omniglot.com/conscripts/zhonghuayuzi.htm)，韵/介母按顺序自上而下排列，可以连接时自然连接，*不使用*原作者提出的韵/介母简写规则（`uai -> ue`等），对于`-i`尾，仅在`zh` `ch` `sh` `r` `z` `c` `s`后时使用，其余按正常韵母符号表示

![alt text](image-9.png)

![alt text](yuzi-compare.png)

<script>
  // 修复图炸的情况
  (new Array(...document.getElementsByTagName('img'))).forEach(
      img=>{
          if(img.src.split('/')[3]!='images'&&!img.src.startsWith(location.href.split("#")[0])){
              console.log(`"${decodeURI(img.src.split('/').slice(-1))}" 貌似炸了`)
              img.src=img.src.split('/').slice(-1)
          }
  })
</script>