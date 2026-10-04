# 费曼的彩虹 · 英文伴读：章节页编写规范

读者：中文母语的程序员，手里是**英文原版纸质书**（Feynman's Rainbow, Leonard Mlodinow）。词汇量大约是大学英语四六级，
没有在英语国家生活过。他的原话：

- "不少生词和固定短语不认识，比如 down the hall，每个字我都认识，但是我不知道什么意思。我也不知道我的理解是否正确。"
- "有一些背景知识，似乎作者是默认读者知道的。"
- "这本书基本没有图片，要是导读里能有图片就好了。……尽量多放图，现在的人很缺乏读长文的能力，没有图根本读不下去。"

所以每一页做四件事：**补背景、多放图、解词和短语、帮他确认读懂了**。本站是伴读，不是译本：读者要去读原书。

**样板：`chapters/00.html`。动笔前完整读一遍，结构、组件、语气都以它为准。**

## 你只写这些文件

- `chapters/NN.html`（NN 是两位章号，01–24）
- `assets/img/NN-*.jpg`（只通过 `tools/fetch_img.py` 生成）

**不要改** `assets/style.css`、`assets/fr.js`、`assets/chapters.js`、`index.html`、`AUTHORING.md`、`tools/` 或别的章节页
（多个作者并行；发现共享文件有 bug 写在报告里）。页面里不写 `<style>`，不写 `<script>`，颜色和组件都用共享样式里现成的。
导航里你的章节暂时显示"待写"是正常的，主编最后统一更新。

## 写作依据

- 原书英文：`source/text/NN.txt`。每行一段，行首 `[段号]`；`{F}` 表示这一段在纸质书里是斜体，是费曼的原话。
  **先完整读完你负责的章节再动笔。** 需要前后文时可以读相邻章节。
- `source/` 里的一切（包括 `source/epub/` 里的图）都是原书材料，**不能复制到 `assets/`，不能出现在页面里**。
  原书每章开头有一个小的费曼图装饰，那是书的版式，不要用；想放费曼图就自己画。
- 页面、图片名、报告里**不要出现 epub 的文件名**。

## 版权红线（违反任何一条都要返工）

1. **不逐段翻译或转述原书。** "这一章在做什么"不超过 150 个汉字，说的是这一章的作用和读法，不是按顺序复述情节。
2. **直接引用原文：每页最多 2 处，每处不超过 25 个英文单词**，用
   `<blockquote class="quote">英文原文<cite>— 说明。本站译：中文</cite></blockquote>`。
3. 词条里的定位片段（`.loc`）是 4–7 个连续的原文单词，这是允许的；除引用块外，页面上不能有 12 个词以上的原文连续片段。
4. 理解检查的答案用你自己的话，两三句，说结论，不复述段落。
5. 自检：`python3 tools/overlap.py chapters/NN.html` 必须打印 `✓` 和"全部通过"。

## 页面骨架

```html
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>第 N 章 · 费曼的彩虹 英文伴读</title>
<link rel="stylesheet" href="../assets/style.css">
<script src="../assets/chapters.js"></script>
<script src="../assets/fr.js"></script>
</head>
<body data-chapter="N">
<main>
  …下面各节…
</main>
</body>
</html>
```

章头（标题、词数、难度标签）、顶栏、章末导航、备案号页脚、词条的"记下"按钮和筛选栏，都由 `fr.js` 注入，你不用写。

各节顺序固定：

### 1. `<h2>这一章在做什么</h2>`
`<div class="gist"><p>…</p></div>`，不超过 150 个汉字。说清：这一章在全书里起什么作用、谁出场、读的时候抓什么。
紧跟一张图（照片或示意图），让读者一打开页面就看到图。

### 2. `<h2>背景：作者默认你知道的事</h2>`
2–5 个 `<h3>` 小块，每块是一件美国读者知道、中国读者多半不知道的事：人物、地点、机构、历史事件、美国生活里的东西
（学制、品牌、电视节目、俚语背后的典故）。**每块文字不超过 120 个汉字，并尽量配一张图。**
出现多个人物时用人物卡：
```html
<div class="who">
  <div><b>中文名</b><span class="en">English Name</span>一句话：他是谁、在这一章里干什么。</div>
</div>
```
注意：作者在序言里说过，除了费曼、盖尔曼（Murray Gell-Mann）、Helen Tuck、John Schwarz、Mark Hillery、Nick Papanicolaou
和历史人物，**其他人的名字和性格都改过**。改过名的人不是真实人物，不要去找照片，也不要当真人介绍。

### 3. `<h2>这一章的物理，先用中文过一遍</h2>`（只有物理多的章节才有）
先用 3–6 句大白话讲这一章的物理在说什么（面向没学过大学物理的程序员，可以用编程类比），配至少一张自己画的示意图，然后是名词对照表：
```html
<div class="table-wrap"><table class="terms">
  <tr><th>英文</th><th>中文</th><th>一句话</th></tr>
  <tr><td>quantum chromodynamics</td><td>量子色动力学</td><td>描述强力（把夸克粘在一起的力）的理论，简称 QCD。</td></tr>
</table></div>
```
物理说法必须是你有把握的标准说法；只讲到读懂这一章所需的深度。

### 4. `<h2>词与短语</h2>`
开头一句 `<p class="lede">词条按在书里出现的顺序排。斜体小字是它所在的那句话里的几个词，方便你在纸质书上找到。</p>`，然后是词条：
```html
<div class="entry trap"><div class="en">land an office</div><div class="loc" data-p="3">… to have landed an office just …</div><div class="zh">弄到一间办公室</div><div class="note">land 作动词：把好东西搞到手。常见 <i>land a job</i>。</div></div>
```
- `.en`：词或短语的原形（一页之内不能重复，它是"记下"功能的键）。
- `.loc`：原句里**连续的 4–7 个词，一字不差地照抄**，包含这个词条，前后加 `…`。`data-p` 是 `source/text/NN.txt` 里的段号。
- `.zh`：在**这一句里**的中文意思，短。
- `.note`（可省）：一句话说用法、容易错在哪、典故。不写废话。
- `class="entry trap"`：**每个字都认识、合起来意思变了**的短语，或者熟词生义（如 fellowship 不是友谊，late 是已故）。
  这是读者最需要的一类，要靠你读原文一句一句找，词频表找不出来。口语、俚语、短语动词、习语、美国生活用语都算。
  每章的 trap 应占三分之一以上；对话多的章节会更多。
- 数量：短章（不到 1200 词）30–45 条，一般章节 45–70 条，第 4、9 章可以到 90 条。按出现顺序排。
  读者认识四六级词汇，不要收 important、discover 这种词；`down the hall` 序言里讲过，不用再收。
- 费曼的原话（`{F}` 段落）是口语实录，句子不完整、有口头禅，读者容易晕。遇到这种段落，在 `.note` 里点明"这是口语，书面形式是……"。
- 中文里要加引号时用「」，不要用英文直引号。

### 5. `<h2>值得停下来的句子</h2>`
1–2 个引用块（见红线第 2 条），每个后面一小段：句子结构怎么拆、为什么值得停。挑长难句或者全书的要害句。

### 6. `<h2>检查一下理解</h2>`
开头 `<p class="lede">先在心里答，再点开。答错的那题，回书里把对应段落再读一遍。</p>`，然后 4–6 题：
```html
<details class="check"><summary>1. 问题？</summary><p>答案，两三句。</p></details>
```
问的是**容易读错的地方**：谁对谁说的、是讽刺还是当真、某个指代指什么、作者的态度、一句口语的真实意思。不问"这一章讲了哪几件事"。

## 图：越多越好，但每张都要有用

**每章至少 4 张图，其中至少 1 张照片、至少 1 张自己画的 SVG；物理多的章节至少 2 张 SVG。** 页面上半部分（第 1–3 节）不要出现连续两屏没有图的情况。

### 照片（维基共享资源）
国内打不开维基，图必须下载到本地。用现成的工具：
```sh
source/.venv/bin/python tools/fetch_img.py search "Caltech Athenaeum"          # 找图，✓ 表示授权可用
source/.venv/bin/python tools/fetch_img.py get 07 athenaeum "File:Caltech Athenaeum.jpg"   # 存为 assets/img/07-athenaeum.jpg
```
- 工具只接受公有领域 / CC0 / CC BY / CC BY-SA，会自动登记到 `assets/img/CREDITS.md`，并打印出处文字。
- **下载后必须用 Read 工具看一眼图**，确认画面内容就是你要的（搜索结果常常名不副实），再写 alt 和图注。画面不对就删掉文件，并把 CREDITS.md 里对应那行删掉。
- 图注里只写你从图片说明里能确认的事；年份、人物身份不确定就不写。
- 适合找照片的：真实的人（费曼、盖尔曼、施瓦茨、爱因斯坦、牛顿、麦克斯韦等）、地点（加州理工、帕萨迪纳、伯克利、以色列的基布兹）、
  实物（彩虹、盖革计数器、气泡室径迹、粒子加速器、费曼的面包车）、历史照片。费曼本人的照片能用的不多，序言已经用了 `00-feynman.jpg`，
  别的章节可以直接引用 `../assets/img/00-*.jpg`，但尽量找新的。
```html
<figure class="fig"><img src="../assets/img/07-athenaeum.jpg" alt="画面里有什么" loading="lazy">
<figcaption>图注：这是什么，和这一章有什么关系。<span class="src">作者，授权，维基共享资源</span></figcaption></figure>
```
两张竖图并排用 `<div class="pair crop">` 包两个 figure；窄图用 `<figure class="fig narrow">`。

### 自己画的示意图（内联 SVG）
适合画的：物理概念（四种力、夸克组成质子、费曼图、所有路径求和、彩虹的光路、弦和点）、人物关系、时间线、地图示意、
一个比喻的图解、口语短语的字面意思和实际意思对比。画得简单清楚，像白板上的草图。
```html
<figure class="fig"><svg class="diagram" viewBox="0 0 640 260" role="img" aria-label="一句话描述图的内容">…</svg>
<figcaption>本站示意图。说明。</figcaption></figure>
```
- **必须用 `class="diagram"`，颜色只用共享样式里的类**（SVG 属性里写 `var()` 不生效，写死颜色在深色模式下会看不见）：
  文字 `<text>` 默认即可，加粗 `t-b`，次要 `t-m`，色块上的白字 `t-on`；
  线 `ln`（灰）、`ln-a`（强调色粗线）、`ln-d`（虚线）、`s1`–`s6`（彩色线）；
  填充 `box`（浅底带边框）、`f-fg`、`f-a`、`f-soft`、`f1`–`f6`（彩色）。
  不要写 `fill="#…"`、`stroke="#…"`、`style="…"`。箭头用 `<marker>`，里面的 path 也用这些类。
- viewBox 宽度用 640，文字不小于 12px，在 400px 宽的手机上也要能看清：一张图里的文字不要超过二十来个标签。
- 中文标注。不要照着原书或别处的图描。

## 事实要准

背景和物理里写的每一件事（年份、人名、机构、谁得了什么奖、哪件事在哪年）都要是你有把握的。
拿不准的宁可不写，或者在报告里列出来让主编核对。**不要编数字，不要编引语。** 书里说的事和史实有出入时，以书为准描述书里的情节，史实另说。

## 语言

中文，句子短，直接说事。不用"值得注意的是""让我们""总而言之"这类套话，不用破折号堆砌，不写小结段。
不要夸这本书或夸读者。术语第一次出现给英文原文。

## 交稿前自检（都要通过）

```sh
python3 tools/overlap.py chapters/NN.html                                    # 必须"全部通过"
node tools/check.mjs chapters/NN.html --shots source/shots                   # 必须"全部通过"（四种组合：浅/深 × 400/1100）
```
`check.mjs` 会报 JS 错误、加载失败的图、横向溢出、低对比度文字。截图在 `source/shots/chapters_NN.html-*.png`，整页很长；
用下面的命令把 400px 浅色和深色截图切成几段，**至少各看一遍有图的那几段**，确认 SVG 在两种主题、手机宽度下都看得清、文字没重叠：
```sh
source/.venv/bin/python -c "
from PIL import Image; import sys
for th in ('light','dark'):
    im=Image.open(f'source/shots/chapters_NN.html-{th}-400.png'); H=im.size[1]
    for i,y in enumerate(range(0,min(H,7200),1800)): im.crop((0,y,400,min(H,y+1800))).save(f'source/shots/NN-{th}-{i}.png')
"
```
另外自己数一遍：引用块 ≤2；`.en` 没有重复；每个 `.loc` 都能在 `source/text/NN.txt` 对应段落里原样找到。

## 报告（你的最后一条消息）

每章按这个格式：
```
第 N 章
标题：（你起的中文标题，不超过 10 个字，不剧透结尾）
一句话：（不超过 24 个字，给目录用）
phys：0/1/2（0 几乎没有物理，1 有一些物理名词，2 物理名词密集）
talk：0/1/2（0 书面语为主，1 有一些口语，2 口语俚语多）
图：照片 X 张（文件名），SVG Y 张
词条：共 X 条，其中 trap Y 条
拿不准的事实：（没有就写"无"）
共享文件的问题：（没有就写"无"）
自检：overlap ✓/✗，check ✓/✗
```

另外：`python3 tools/lint.py chapters/NN.html` 必须打 ✓（查 .en 重复、.loc 能否在原文对应段落找到、词条顺序、图的数量、写死的颜色、内联 style）。
