---
title: '[TSCTF-J2026]フラグの恋 - 出题人WP'
date: 2026-10-14 03:25:34
tags:
---

<!-- # フラグの恋 出题人WriteUp <span style="font-size: 0.6em">by 圆周率</span> -->

<a href="フラグの恋 - 出题人WP.pdf">点击此处访问PDF版</a>

## 选手视角

### 旮旯给木基本素养部分

首先题目并没有附件和环境，而是给了一串神秘文字，分析文字，发现仅由四个字组成，由此想到是兽音加密，搜索“兽音译者”即可找到解密程序

兽音译者需要一个四个字符的字符表，只要稍微进行过网上冲浪就马上能知道大概率是“鸡你太美”，由此可以解出附件的网盘地址

![alt text](image.png)

接下来就是下载附件，得到一个.enc文件，经过简单检索，就可以找到一大堆教你解密的视频（看得出来，为了让大家都玩得了旮旯给木，还是有不少 ~~被新手气坏了的人~~ 好心人的）

下载一个[PTE](https://paranoiaworks.mobi/pfte/)，然后就可以使用密码解压了

![alt text](image-1.png)

接下来是一个.lz4文件，LZ4是一种压缩算法，可以使用Python解压

```python
import lz4.frame
open('フラグの恋', 'wb').write(lz4.frame.decompress(open('フラグの恋.lz4', 'rb').read()))
```

接下来可以根据文件头判断，这是一个zip文件，修改扩展名后打开

![alt text](image-2.png)

可以看见右侧注释区直接给出了密码，得到下一层文件

拿到后binwalk一下，发现其中含有一个zip文件，改扩展名后发现需要密码

![alt text](image-3.png)

![alt text](image-4.png)

把扩展名改回来，考虑密码藏在视频里，视频不外乎就是图像和音频（当然，部分多媒体格式也支持嵌入文件，可以ffprobe一下），这里我们盯帧，发现22.44s附近有一个二维码

![alt text](image-5.png)

识别后得到“pwd is 114514”，说明压缩包密码是114514，得到下一层文件

至此，我们得到了本题的主角：旮旯给木

![alt text](image-6.png)

### Ren'Py解包部分

这个文件结构一眼使用Ren'Py编写，很好解包，下面开始解包

进到game文件夹内，发现一个archive.rpa，这个是renpy的自定义文件格式，可以使用unrpa项目解包

![alt text](image-7.png)

```sh
unrpa archive.rpa
```

![alt text](image-8.png)

这里出错了，很明显，这里的存档格式被魔改了，但我们只要能找到一个offset和一个key。就可以继续使用这个工具提取

我们进到renpy文件夹下找到loader.py文件，这个文件负责解码各版本的rpa文件，可以找到所需两个值的存储位置

![alt text](image-9.png)

```sh
unrpa archive.rpa --offset 565277 --key 1195461665 --force RPA-3.0
```

这里就解包好了，当然，都看到了源码，根据源码写一个解包脚本也是可以的

另外rpa文件的zlib几乎是形同虚设，binwalk都能出来不少文件，而且key所保护的加密内容竟然是文件名而不是内容，感觉实在是有点过于草台了（x

接下来就可以使用unrpyc恢复项目源码

```sh
python D:\path-to\unrpyc-master\unrpyc.py .
```

![alt text](image-10.png)

核心逻辑在strangebox.rpy中，首先导入了一个模块strangebox，然后要求输入目标值target，接下来提供SMC key解锁代码，最后验证输入是否正确

接下来就是寻找SMC key和target

### 解密SMC key

注意到有一个archive_me文件夹很可疑，里面有一个`piz.yek`，很容易想到是倒序的zip文件，如果处于某种原因没有解析出文件名，那么就只能通过瞪眼法，注意到最后的`40 30 B4 05`（ZIP文件头`50 4B 03 04`的倒序）

接下来反转这个文件的字节

```python
open('key.zip', 'wb').write(bytes.fromhex(open('piz.yek', 'rb').read().hex()[::-1]))
```

打开，是一个部分加密的zip文件，其中的文本文档很有可能含有密码，打开看看

![alt text](image-11.png)

这个文件下方显示其有283个字符，而图中的字很明显没有那么多，加上文字中强调“你看不见吗”，很容易想到这是零宽字符隐写，解压文本文档，观察其中的零宽字符种类

```python
print('\n'.join(sorted(map(repr, set(filter(lambda x: not x.isprintable(), open('圆周率的话.txt', encoding='utf-8').read()))))))
```

![alt text](image-12.png)

找一个[零宽字符隐写网站](https://tool.bfw.wiki/tool/1695021695027599.html)，勾选对应零宽字符进行解密

![alt text](image-13.png)

得到解压密码，进入下一步

![alt text](image-14.png)

注释中强调了rockyou，这是CTF中常见的一个弱密码表，其中包含超过一千四百万条密码记录。所以下一步就是利用rockyou爆破弱密码

首先使用zip2john提取哈希

```sh
zip2john key.rar.zip > hash1
```

删除哈希首尾多余的部分，对照哈希示例表找到模式，接下来就可以使用hashcat爆破（john其实也可以，但是可能不支持GPU加速，会慢很多）

```sh
hashcat -a 0 -m 13600 D:\path\to\hash1 D:\path\to\rockyou.txt
```

![alt text](image-15.png)

运行24s后得到密码`aya&yassin1`，进入下一层

![alt text](image-16.png)

很明显，提示我们按掩码爆破六位纯数字密码，我们如法炮制，使用rar2john获得密码后使用hashcat爆破

![alt text](image-17.png)

这次的哈希短一些，就可以直接通过命令行调用， ~~长的指令会使咖喱味的Terminal出现一点点bug~~

```sh
hashcat -a 3 -m 13000 $rar5$16$32a1ed568779dcbeeb9235022233e08c$15$420a947222c5eb5968888330d96fa7f2$8$51d35d2f50e5808e ?d?d?d?d?d?d
```

![alt text](image-18.png)

运行10s后得到了密码`833934`，进入下一层

![alt text](image-19.png)

这回几乎没有提示，但是图像就让人想起明文攻击，看一下加密和存储方式

![alt text](image-20.png)

使用的是传统ZipCrypto+Store，可以利用PNG文件头进行明文攻击，提取PNG文件头，然后使用bkcrack进行明文攻击，这里的代码把破解和提取写在一起了，就不用跑两次指令了

```sh
bkcrack -C "D:\path\to\key_final.zip" -c key.png -p pngheader.bin -D cracked.zip
```

![alt text](image-21.png)

解压得到key.png

![alt text](image-22.png)

这玩意一眼二维码，但是是什么变换呢？这里致敬（？）了一下DDLC中的`natsuki.chr`，采取的是极坐标变换，只要做一次Rect2Polar就好了

![alt text](image-23.png)

扫出来就是SMC key了

![alt text](image-24.png)

### 提取target

既然target也要输入，那么target在哪里呢？压缩包里还留下了一个存档文件，而renpy会自动存储所有的变量值，回去再看看target的代码：

![alt text](image-25.png)

由此可见，我们可以从存档文件里读取target的值

最简单的办法就是使用开发者模式加载存档，然后在控制台中输出target的值

为此，我们先将存档复制到renpy的存档文件夹：`%APPDATA%/Renpy/[project-name]-[project-id]/`，然后在game文件夹下创建一个rpy文件，写入

```rpy
define config.developer = True
```

接下来启动游戏按Shift+O就可以……

![alt text](image-26.png)

炸了，提示找不到字体，最简单的办法就是把文件夹里的字体复制一份改个名字就行

接下来启动游戏按Shift+O就可以打开控制台了

![alt text](image-27.png)

然后读取存档，启动控制台，输入target就有target的值了~

![alt text](image-28.png)

这里是可以自由执行Ren'Py/Python指令的，所以可以把target写到文件里，方便复制

另外各位的AI肯定是选择手撕save文件的，下面也分析一下

首先，可以注意到save文件的文件头是504B0304，所以改为zip并解压，里面几个文件明显没有用，唯一有用的是log，这是一个pickle文件

我让D老师写了一个在无对应类时进行polly fill的脚本，最后输出为json，附在最后

输出来的内容开头就送“store.target”……欸，怎么不一样？

![alt text](image-29.png)

这里就需要看一下renpy文件夹下的loadsave.py了，可以看到save/load逻辑中有我加上去的一段逻辑

![alt text](loadsave.png)

这里对存储的target进行了简单加/解密，但是加密后的格式与加密前一致，都是base64，所以一下子还真不一定看得出来

![alt text](image-30.png)

因为这个操作对于游戏是透明的，所以通过游戏提取就不会被阴到，突发奇想想到了之后就立刻加上了

~~Galgame有旮旯给木的做法，你应该手动解包，然后手动输入魔改的偏移，最后使用Ren'Py相关的知识解决问题，什么叫你丢给AI就出来了，旮旯给木不是这样的，我不接受！😤~~

### 分析strangebox

接下来就是最神秘的存在：strangebox

通过搜索在lib/python3.12文件夹下找到了`strangebox.pyd`

逆向分析一下，发现不是很好逆向的样子……

喂喂，这是Misc题，你想到哪去了，怎么会在逆向上卡你呢？所以有没有什么不用逆向的办法呢？

有的有的，兄弟有的

我们可以把它作为一个黑盒分析，一旦这个算法有些许设计上的缺陷，就算混淆得再复杂，照样能解出

接下来我们要导入这个模块，由于pyd与python版本相关，所以要启动lib/py3-windows-x86_64下的python，或者直接在控制台中测试

```python
import strangebox
strangebox.unlock('there_1s_@_5tran9e_6ox_aNd_heRe_i5_7he_keY_6ut_vvha7s_!n_it??!')
import base64
for i in range(16):
    print(f"{'1'*-~i:<16} {base64.b64decode(strangebox.E(b'1'*-~i)).hex()}")
```

![alt text](crack_exp.png)

我们发现，虽然加密结果整体上没什么规律，但是它有一个致命缺点：距离到一定程度后，后面的数据将不会影响前面加密的结果，也就是说，我们可以分组对其进行爆破，这样减少了非常大的枚举空间，最后的爆破成本是可以接受的（但是还是比较久，稍安勿躁）

下面给出爆破脚本

```python
from strangebox import *
unlock('there_1s_@_5tran9e_6ox_aNd_heRe_i5_7he_keY_6ut_vvha7s_!n_it??!')
import base64
target = base64.b64decode(b'SYEvg6pw9bmftakduXHUMLsK89olpkbzH3YHdGnbCi2svAMf7hviAVszOCmiPvxlLVt2fALAI3l3I2ZOffDo++YQiHYMr995')

CHARSET = '!012579@AJS_acdeghlmorstuvwy{|}'.encode()
import itertools
def guess(target, prefix=b''):
    for l in range(0 if (last := (len(target)-3 == len(prefix))) else 3, 3 if last else 4):
        for g in itertools.product(CHARSET, repeat=l):
            g = bytes(g)
            print((prefix+g).decode())
            if target.startswith(base64.b64decode(E(prefix+g))[:len(prefix)+2 if not last else None]):
                if last:
                    yield g
                else:
                    for gn in guess(target, prefix+g):
                        yield g+gn

import time
st = time.time()
for g in guess(target, b'TSCTF-'):
    print('[!] ', b'TSCTF-'+g, f'runtime: {time.time()-st:.2f}s')
    if not input("Continue?"):
        break
```

![alt text](image-31.png)

~~耗时两分半~~ 拿到flag

完结撒花~

## 出题人视角

首先这是一道misc大杂烩，因为我看着misc里面考的都比较灵活，基础没考什么，所以就往里面额外塞了一大堆misc基础知识。

首先是旮旯给木基础 & renpy解包/target提取，是承接宣讲内容主题的一部分，使用的都是我在实际调查时遇到的套路，而这些基本都是我们misc玩剩了的，考察搜索能力、面对未知知识的主动学习和灵活应变能力。

解密SMC key考察了含密码的压缩包的常见考法，但含密码的压缩包还远远不止这点知识点，比如伪加密、以文件名作为密码之类的考法都没有囊括在内。最后的图像极坐标变换也是不常考的点，更常见的变换应该是ZigZag来着，可以去了解一下ZigZag变换后的二维码特征。

为了给RenPy内置的python编译pyd文件，我可是费了不少功夫，通过询问D老师，最后解决了。简单来说就是配置UCRT编译环境，由dll文件生成符号文件，从不记得什么地方凑齐了includes，最后链接编译，有机会会在博客展开讲

由于要SMC，所以没办法直接Cython，最后是让D老师把代码用CPython API重写了一遍，为了尽可能防止直接逆向解决，最后开了O3+strip，不过感觉AI还能能分析出来，说不定有更高效的解密方式呢

顺带一题，由于本题计划考察黑盒逻辑分析，所以我写的算法根本没有考虑可逆性，会有一些映射到同一结果的，碰撞率在13%左右，不过比我大笔一挥几面A4纸的初版算法好多了（碰撞率好像是80%左右，一堆多解）。

### 附：D老师给的解包pickle的脚本

注意：请不要解包任何安全性未知的pickle文件！能RCE的！

```python
import pickle
import json
import sys
from datetime import datetime, date, time
from decimal import Decimal
from collections.abc import Mapping, Sequence

# ---------- 通用占位类 ----------
class Unknown:
    """
    当原始类缺失时，用此占位类替代。
    支持列表操作（append, extend, 整数索引）和字典风格操作（字符串键），
    同时保留所有属性（通过 __dict__）。
    """
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._module = getattr(cls, '_module', 'unknown')
        instance._name = getattr(cls, '_name', 'unknown')
        instance._list_items = []          # 存储列表元素
        return instance

    def __init__(self, *args, **kwargs):
        pass

    def __setstate__(self, state):
        # 如果状态是字典，更新到 __dict__
        if isinstance(state, dict):
            self.__dict__.update(state)
        else:
            # 其他状态保存备用
            self._state = state

    # ---------- 列表支持 ----------
    def append(self, item):
        self._list_items.append(item)

    def extend(self, iterable):
        self._list_items.extend(iterable)

    def __len__(self):
        return len(self._list_items)

    def __iter__(self):
        return iter(self._list_items)

    # ---------- 索引支持（兼容列表和字典） ----------
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._list_items[key]
        # 字符串键作为属性访问（优先从 __dict__ 获取）
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._list_items[key] = value
        else:
            self.__dict__[key] = value

    def __repr__(self):
        return f"<Unknown {self._module}.{self._name} (len={len(self._list_items)})>"


class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        try:
            return super().find_class(module, name)
        except (AttributeError, ImportError):
            # 动态创建 Unknown 子类并记录原类信息
            class UnknownSubclass(Unknown):
                _module = module
                _name = name
            return UnknownSubclass


# ---------- 递归转换器 ----------
def to_jsonable(obj):
    """将任意 Python 对象转换为 JSON 可序列化的结构"""
    # 基础类型
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, bytes):
        return repr(obj)
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj) if obj.is_finite() else str(obj)

    # 优先处理 Unknown 占位对象（包含列表元素 + 额外属性）
    if isinstance(obj, Unknown):
        # 列表元素（递归转换）
        list_items = [to_jsonable(item) for item in obj._list_items]
        # 额外属性（排除内部字段）
        attrs = {}
        for key, value in obj.__dict__.items():
            if key not in ('_module', '_name', '_list_items', '_state'):
                attrs[key] = to_jsonable(value)
        # 将 _state 也纳入（如果有）
        if hasattr(obj, '_state') and obj._state is not None:
            attrs['_state'] = to_jsonable(obj._state)
        return {
            '__unknown__': {
                'module': obj._module,
                'name': obj._name,
                'list': list_items,      # 列表数据（若是列表子类）
                'attrs': attrs           # 其他属性
            }
        }

    # 序列（列表、元组等）
    if isinstance(obj, Sequence) and not isinstance(obj, str):
        return [to_jsonable(item) for item in obj]

    # 映射（字典、有序字典等）
    if isinstance(obj, Mapping):
        return {str(k): to_jsonable(v) for k, v in obj.items()}

    # 集合
    if isinstance(obj, (set, frozenset)):
        return [to_jsonable(item) for item in obj]

    # 其他自定义对象：尝试提取 __dict__
    if hasattr(obj, '__dict__'):
        return to_jsonable(vars(obj))

    # 最终降级为 repr
    return repr(obj)


def load_pickle_to_json(filepath, indent=2):
    try:
        with open(filepath, 'rb') as f:
            unpickler = SafeUnpickler(f)
            obj = unpickler.load()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {filepath}")
    except pickle.UnpicklingError as e:
        raise ValueError(f"解析 Pickle 失败: {e}")

    jsonable = to_jsonable(obj)
    return json.dumps(jsonable, indent=indent, ensure_ascii=False)


if __name__ == '__main__':
    # 强制标准输出使用 UTF-8，避免重定向编码问题
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    else:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if len(sys.argv) < 2:
        print("用法: python unpickle.py <pickle文件路径>")
        sys.exit(1)

    pickle_path = sys.argv[1]
    try:
        result = load_pickle_to_json(pickle_path)
        print(result)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
```

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