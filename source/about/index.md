---
title: 关于我……
date: 2025-10-30 16:16:29
---

<div>

<img src="/images/logo.png" style="width: min(280px, min(30vh, 30vw)); height: min(280px, min(30vh, 30vw)); float: right; border-radius: 10px">

<style>
    #studyIn:hover {
    filter: brightness(1.4);
}
</style>

我是圆周率，目前就读于<span id="studyIn" style="text-decoration: underline wavy red; cursor: pointer; user-select: none;" title="Not Truth"></span>，喜欢倒腾电脑，正在学习打CTF~

个人介绍就算了吧，真的很懒！

也许下面会随机刷新友链？

</div>

<script>
    studyIn = ["北京邮电学院", "中国邮电大学", "北京等通知大学"]
    randomStudyIn = ()=>{document.getElementById("studyIn").innerText = studyIn[Math.floor(Math.random()*3)]}
    randomStudyIn()
    document.getElementById("studyIn").addEventListener("click", randomStudyIn)
</script>
