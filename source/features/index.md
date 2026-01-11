---
title: 特性修改
date: 2026-1-4 17:20:11
toc: true
---

本站有很多圆周率自己加的史，如果您不想要这些特性，可以在这里修改

**注意：本页的选项均使用localStorage存储，请使用支持localStorage的浏览器**

<p id="support-storage" class="unknow">正在检测你的浏览器是否支持localStorage……🔎</p>

<style>
    .unknow{
        border: 1px hsla(54, 88%, 24%, 1.00) solid;
        color: hsla(54, 88%, 24%, 1.00);
        background-color: hsla(54, 90%, 85%, 1.00);
        border-radius: 5px;
        padding: 5px;
        width: fit-content;
    }
    .support{
        border: 1px #077207 solid;
        color: #077207;
        background-color: #b4fbb4;
        border-radius: 5px;
        padding: 5px;
        width: fit-content;
    }
    .unsupport{
        border: 1px #720707 solid;
        color: #720707;
        background-color: #fbb4b4;
        border-radius: 5px;
        padding: 5px;
        width: fit-content;
    }
</style>

<script>
    function test(){
        try{
            localStorage.setItem('test', 'ok');
            var result = localStorage.getItem('test') == 'ok';
            localStorage.removeItem('test');
            return result;
        }catch(error){
            console.error(error);
            return false;
        }
    }
    let result = test();
    document.getElementById('support-storage').classList.remove('unknow')
    if(result){
        document.getElementById('support-storage').innerText = '你的浏览器支持localStorage！🎉🎉🎉'
        document.getElementById('support-storage').classList.add('support')
    }else{
        document.getElementById('support-storage').innerText = '你的浏览器好像不支持localStorage！🤔'
        document.getElementById('support-storage').classList.add('unsupport')
    }
</script>

## 明/暗主题

<fieldset>
<legend>主题</legend>
<label style="display: flex"><input name="theme-radio" type="radio" value="auto">跟随系统<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 1em;"><path d="M12 21.9967C6.47715 21.9967 2 17.5196 2 11.9967C2 6.47386 6.47715 1.9967 12 1.9967C17.5228 1.9967 22 6.47386 22 11.9967C22 17.5196 17.5228 21.9967 12 21.9967ZM12 19.9967C16.4183 19.9967 20 16.415 20 11.9967C20 7.57843 16.4183 3.9967 12 3.9967C7.58172 3.9967 4 7.57843 4 11.9967C4 16.415 7.58172 19.9967 12 19.9967ZM7.00035 15.316C9.07995 15.1646 11.117 14.2939 12.7071 12.7038C14.2972 11.1137 15.1679 9.07666 15.3193 6.99706C15.6454 7.21408 15.955 7.46642 16.2426 7.75406C18.5858 10.0972 18.5858 13.8962 16.2426 16.2393C13.8995 18.5825 10.1005 18.5825 7.75736 16.2393C7.46971 15.9517 7.21738 15.6421 7.00035 15.316Z"></path></svg><span title="使用媒体查询自动选择" style="text-decoration: underline; text-decoration-style: dotted;">?</span></label>
<label style="display: flex"><input name="theme-radio" type="radio" value="light">亮<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 1em;"><path d="M12 18C8.68629 18 6 15.3137 6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12C18 15.3137 15.3137 18 12 18ZM12 16C14.2091 16 16 14.2091 16 12C16 9.79086 14.2091 8 12 8C9.79086 8 8 9.79086 8 12C8 14.2091 9.79086 16 12 16ZM11 1H13V4H11V1ZM11 20H13V23H11V20ZM3.51472 4.92893L4.92893 3.51472L7.05025 5.63604L5.63604 7.05025L3.51472 4.92893ZM16.9497 18.364L18.364 16.9497L20.4853 19.0711L19.0711 20.4853L16.9497 18.364ZM19.0711 3.51472L20.4853 4.92893L18.364 7.05025L16.9497 5.63604L19.0711 3.51472ZM5.63604 16.9497L7.05025 18.364L4.92893 20.4853L3.51472 19.0711L5.63604 16.9497ZM23 11V13H20V11H23ZM4 11V13H1V11H4Z"></path></svg></label>
<label style="display: flex"><input name="theme-radio" type="radio" value="night">暗<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 1em;"><path d="M11.3807 2.01886C9.91573 3.38768 9 5.3369 9 7.49999C9 11.6421 12.3579 15 16.5 15C18.6631 15 20.6123 14.0843 21.9811 12.6193C21.6613 17.8537 17.3149 22 12 22C6.47715 22 2 17.5228 2 12C2 6.68514 6.14629 2.33869 11.3807 2.01886Z"></path></svg></label>
</fieldset>

<script>
    var themeSetting = localStorage.getItem('color-scheme') || 'auto';
    (document.querySelector(`input[name=theme-radio][value=${themeSetting}]`)||document.querySelector('input[name=theme-radio][value=auto]')).checked = true;
    function switchThemeTo(colorScheme){
        localStorage.setItem("color-scheme", colorScheme);
        scheme = colorScheme==='auto'?(matchMedia('(prefers-color-scheme: dark)').matches?"night":"light"):colorScheme;
        if(scheme==='light'){
            document.getElementById("sun").style.display = "none";
            document.getElementById("moon").style.display = "";
            let classlist = document.querySelector("html").classList;
            classlist.remove('night');
            classlist.add('light');
        }else{
            document.getElementById("sun").style.display = "";
            document.getElementById("moon").style.display = "none";
            let classlist = document.querySelector("html").classList;
            classlist.add('night');
            classlist.remove('light');
        }
    }
    document.querySelectorAll('input[name=theme-radio]').forEach((input)=>{
        input.addEventListener("change", ((input)=>(()=>{
            switchThemeTo(input.value)
        }))(input))
    })
    document.getElementById("sun").addEventListener("click", ()=>{
        document.querySelector('input[name=theme-radio][value=light]').checked = true;
    })
    document.getElementById("moon").addEventListener("click", ()=>{
        document.querySelector('input[name=theme-radio][value=night]').checked = true;
    })
</script>

## Logo

<fieldset>
<legend>额外显示Logo</legend>
<label style="display: flex"><input name="logo-radio" type="radio" value="show">显示额外的 Logo！😜</label>
<label style="display: flex"><input name="logo-radio" type="radio" value="none">你搞这么花干什么啊😡</label>
</fieldset>

<script>
    var logoSetting = localStorage.getItem('extra-logo') || 'show';
    switchLogoTo(logoSetting);
    (document.querySelector(`input[name=logo-radio][value=${logoSetting}]`)||document.querySelector('input[name=logo-radio][value=show]')).checked = true;
    document.getElementById("extra-logo").style.display = 'flex';
    function switchLogoTo(logo){
        localStorage.setItem("extra-logo", logo);
        if(logo==='none'){
            // document.getElementById("extra-logo").style.display = 'none';
            document.getElementById("extra-logo").style.opacity = '0';
        }else{
            // document.getElementById("extra-logo").style.display = 'flex';
            document.getElementById("extra-logo").style.opacity = '1';
        }
    }
    document.querySelectorAll('input[name=logo-radio]').forEach((input)=>{
        input.addEventListener("change", ((input)=>(()=>{
            switchLogoTo(input.value)
        }))(input))
    })
</script>

## 返回按钮

<fieldset>
<legend>返回按钮逻辑</legend>
<label style="display: flex"><input name="backbtn-radio" type="radio" value="session">在<code>sessionStorage</code>中记录返回地址</label>
<label style="display: flex"><input name="backbtn-radio" type="radio" value="referer">使用<code>Referer</code>作为返回地址</label>
<label style="display: flex"><input name="backbtn-radio" type="radio" value="history">执行<code>history.back()</code></label>
<label style="display: flex"><input name="backbtn-radio" type="radio" value="none">我不要这些乱七八糟的功能</label>
<div id="backbtn-explain" style="margin: 10px; border: 1px solid; padding: 5px"></div>
</fieldset>

<script>
    var backFunc = localStorage.getItem("backbtn-func") || "session";
    const backExplain = {
        session: '<span>使用<code>sessionStorage</code>存储访问过的界面以模拟返回按钮</span><br/><span style="color: red">缺点：会在浏览器自带的History里面拉屎，每点一次都会被当成“前进”</span>',
        referer: '<span>使用<code>document.referer</code>作为返回目标</span><br/><span style="color: red">缺点：只能返回一层，若使用了“上一篇”/“下一篇”等功能就会在两个页面来回跳</span>',
        history: '<span>使用<code>History API</code>，与浏览器回退按钮功能一致</span><br/><span style="color: red">缺点：锚点会被当成返回点，使用过目录功能后会在同一个页面上跳来跳去</span>',
        none: '<span style="color: red">解决问题的终极方法就是解决提出问题的人/事！</span>'
    }
    function backChoose(opt){
        (document.querySelector(`input[name=backbtn-radio][value=${opt}]`)||document.querySelector('input[name=backbtn-radio][value=session]')).checked = true;
        document.getElementById("backbtn-explain").innerHTML = backExplain[opt] || backExplain['session'];
    }
    backChoose(backFunc);
    function switchBackTo(opt){
        localStorage.setItem("backbtn-func", opt);
        document.getElementById("backbtn-explain").innerHTML = backExplain[opt] || backExplain['session'];
    }
    document.querySelectorAll('input[name=backbtn-radio]').forEach((input)=>{
        input.addEventListener("change", ((input)=>(()=>{
            switchBackTo(input.value)
        }))(input))
    })
</script>