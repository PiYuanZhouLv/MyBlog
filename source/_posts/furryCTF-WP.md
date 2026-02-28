---
title: furryCTF WP
date: 2026-02-28 18:53:13
tags:
---

furryCTF的WP

可惜了，差一点就能拿到吧唧了

![分数详情](QQ截图20260228191344.png)

[furryCTF 2025 Writeup by KFCTF_1s_so_ha2d.pdf](furryCTF%202025%20Writeup%20by%20KFCTF_1s_so_ha2d.pdf)

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