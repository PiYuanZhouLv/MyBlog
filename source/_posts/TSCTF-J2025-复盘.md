---
title: TSCTF-J2025 复盘
date: 2025-11-04 12:33:21
tags:
---

今天下午不想写作业，就来复盘一下TSCTF-J2025吧~

> 不知道为什么图片路径可能会炸掉，在最后面写了一个简易的修复代码，不能保证一定有用
> 
> 如果图炸了的话请手动拼接URL，为
>
> <span id="urlNow"></span>image-编号.png

<script>
  document.getElementById("urlNow").innerText = location.href.split('#')[0]
  document.getElementById("urlNow").innerText += location.href.split('#')[0].slice(-1)==='/'?'':'/'
</script>

## Misc

### Meow

Word文档的本质是一个ZIP压缩包，所以可以在里面藏东西，把扩展名改为.zip后解压，可以在`[Content_Types].xml`文件里看到一行注释

![alt text](image.png)

提示了base64的字母表，所以不需要一眼丁真

做题时因为没有看见异常文件就忽略了这个方向

### PyJail

感觉自己的第一种解法应该可以做到拿os啊，为什么会触发import钩子呢？

然后按照WP的方法试了一下，结果发现：是全角字符的问题

![alt text](image-1.png)

同样是使用`__import__`，但是使用Unicode绕过的版本会触发import，而正常半角字符的不会！

经过实验，发现，是python处理unicode的时候需要先导入unicodedata这个库来支持将形近字转化，这就是最开始用Unicode绕过行不通的原因

![alt text](image-2.png)

再来就是后面用os的底层实现来完成指令执行了，可以用`execlp`/`execvp`来执行，不过还要处理一下`fork`和`pipe`

下面是从WP里面复制的

```python
import os
import sys

def run_command(cmd):
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        os.dup2(w, 1)
        os.dup2(w, 2)
        os.close(w)
        os.execvp("/bin/sh", ["/bin/sh", "-c", cmd])
        os._exit(1)
    else:
        os.close(w)
        with os.fdopen(r) as f:
            output = f.read()
        os.waitpid(pid, 0)
        return output

print(run_command("ls -l"))



import os

def run_command(cmd):
    pid, fd = os.forkpty()
    if pid == 0:
        os.execvp("sh", ["sh", "-c", cmd])
    else:
        output = b''
        while True:
            try:
                data = os.read(fd, 1024)
                if not data:
                    break
                output += data
            except OSError:
                break
        os.waitpid(pid, 0)
        return output.decode()

print(run_command("ls -l"))
```

## AI

### JustReverse

对着WP的代码，看了半天，简直一模一样，回去对比了一下输出，发现第一个卷积就错了，仔细一看，不禁破口大骂： __我是\*\*__ ，艹，一开始想试一下这个算法对不对，还没有写`line`这个变量就打算先试试，结果左下角的值算的是写死的0，后来加上了`line`变量之后忘改了，因为写的太长还没有发现！\#\@\%\!\#\@\#\@

![alt text](image-4.png)

把那个0改成`line[-1]`，然后就解出答案了……

![alt text](image-5.png)

![alt text](image-6.png)

<img src="image-3.png">
<div style="text-align:center; font-size: 0.8em;">《我　裂　开　来》</div>

给出更正后的代码

```python
import numpy as np

n = 58

import torch
import torch.nn as nn
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.linear = nn.Linear(n, n*n)
        self.conv1=nn.Conv2d(1, 1, (2, 2), stride=2)
        self.conv2=nn.Conv2d(1, 1, (1, 1), stride=1)
        self.conv3=nn.Conv2d(1, 1, (2, 2), stride=1, padding=1)
        self.relu=nn.ReLU()

    def forward(self, x):
        x = x.view(1, 1, 2, 2*n)
        x = self.conv1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = x.view(n)
        x = self.linear(x)
        x = x.view(1, 1, n, n)
        x = self.conv3(x)
        return x

mynet=Net()
mynet.load_state_dict(torch.load('model.pth'))

out = list(map(lambda line: list(map(float, line.split(' '))), open('ciphertext.txt').readlines()))

out = np.array(out)

out -= mynet.conv3.bias.detach().numpy()

# print(out)

def reverse_conv(kernel, after, before_size):
    last_line = [0] + [0] * before_size + [0]
    before = []
    for i in range(before_size):
        line = [0]
        for j in range(before_size):
            line.append((after[i][j] - kernel[0][0] * last_line[j] - kernel[0][1] * last_line[j+1] - kernel[1][0] * line[-1])/kernel[1][1])
        last_line = line + [0]
        before.append(line[1:])
    return before

outl = reverse_conv(mynet.conv3.weight.detach().numpy().reshape((2, 2)).tolist(), out.tolist(), n)

# print(outl)

lb = mynet.linear.bias.detach().numpy()
lw = mynet.linear.weight.detach().numpy()

# print(lb.shape)
# print(lw.shape)

out2 = np.linalg.inv(lw.T @ lw) @ (lw.T @ (np.array(outl).reshape((-1)) - lb))

# print(out2)

out1 = (out2 - mynet.conv2.bias.detach().numpy()) / mynet.conv2.weight.detach().numpy()

# print(out1)

w1 = mynet.conv1.weight.detach().numpy()
b1 = mynet.conv1.bias.detach().numpy()

ori = (out1 - b1).reshape((-1))

# print(ori)
ajust = [round(i) for i in ori.tolist()]
# print(ajust)
b = sum([[i&1, (i&2)//2] for i in ajust], []) + sum([[(i&4)//4, (i&8)//8] for i in ajust], [])
# print(b)
for i in range(0, len(b), 8):
    print(chr(int(''.join(map(str, b[i:i+8])), base=2)), end='', flush=True)
```

注：不过还是学到了东西的，WP里面用的是`pinv`方法直接求广义逆，但我们高代还没有学到广义逆，我也不知道有这么一个函数，就手动搓了一个 $(W^TW)^{-1}(W^TY)$
$$
(W^TW)^{-1}(W^TY)\\\\
=(W^TW)^{-1}(W^T(WX))\\\\
=(W^TW)^{-1}(W^TW)X\\\\
=X
$$

## Web

### Druid

看到WP之后我是不能理解当时在干什么的……

admin/admin登录之后在数据源里面就有用户名

![alt text](image-7.png)

## Reverse

### Catbits

那么这道题剩下的那个Toko在哪里呢？答案是：`舞台`也是可以存放代码的！

这是在面试的时候学长讲的，WP里面也有，所以只要在角色的右边选舞台就可以看到了

![alt text](image-8.png)

<hr>

差不多就写到这吧，马上要上英语课了

后面有机会的话可能还会写写Reverse里面solves>=2的题，以及Pwn的一些题目

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