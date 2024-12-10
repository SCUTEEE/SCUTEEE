---
title: SCUTEEE 写作指南
date: 2024-12-05 17:37:00 +0800
authors:
  - name: ToddZZF
math: true
mermaid: true
---

> 优化写作流程，让写出来的文章更加美观。

<!--more-->

本文分为四个部分：

1. Markdown 的语法
2. SCUTEEE 文章基本构成
3. 写作规范
4. 编辑器设置

本文看起来内容多，但其实并不复杂，希望大家能耐心阅读。

## 1. Markdown

### 1.1 基础语法

SCUTEEE 里的文章采用 [Markdown 格式](https://markdown.com.cn/)，更准确来说，是 [Github 风格的 Markdown](https://gfm.docschina.org/zh-hans/)，此外还支持一些额外的语法。Markdown 是一种标记语言，通过标记来区分不同的文字（比如标题、加粗、斜体、列表、表格等），它的基础语法非常简单，如下表[^markdown]所示，点击每个元素有更详细的介绍。

[^markdown]: <https://markdown.com.cn/>

| 元素                                                                                    | Markdown 语法                                            |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| [标题（Heading）](https://markdown.com.cn/basic-syntax/headings.html)                   | `# H1   ## H2   ### H3`                                  |
| [粗体（Bold）](https://markdown.com.cn/basic-syntax/bold.html)                          | `**bold text**`                                          |
| [斜体（Italic）](https://markdown.com.cn/basic-syntax/italic.html)                      | `*italicized text*`                                      |
| [引用块（Blockquote）](https://markdown.com.cn/basic-syntax/blockquotes.html)           | `> blockquote`                                           |
| [有序列表（Ordered List）](https://markdown.com.cn/basic-syntax/ordered-lists.html)     | `1. First item` <br>`2. Second item` <br>`3. Third item` |
| [无序列表（Unordered List）](https://markdown.com.cn/basic-syntax/unordered-lists.html) | `- First item` <br>`- Second item` <br>`- Third item`         |
| [代码（Code）](https://markdown.com.cn/basic-syntax/code.html)                          | `` `code` ``                                             |
| [分隔线（Horizontal Rule）](https://markdown.com.cn/basic-syntax/horizontal-rules.html) | `---`                                                    |
| [链接（Link）](https://markdown.com.cn/basic-syntax/links.html)                         | `[title](https://www.example.com)`                       |
| [图片（Image）](https://markdown.com.cn/basic-syntax/images.html)                       | `![alt text](image.jpg)`                                 |

### 1.2 扩展语法

以下是 Markdown 的扩展语法 [^markdown]，点击每个元素有更详细的介绍。

|元素|Markdown 语法|
|---|---|
|[表格（Table）](https://markdown.com.cn/extended-syntax/tables.html)|`\| Syntax      \| Description \|` <br> `\| ----------- \| ----------- \|` <br> `\| Header      \| Title       \|` <br> `\| Paragraph   \| Text        \|`|
|[代码块（Fenced Code Block）](https://markdown.com.cn/extended-syntax/fenced-code-blocks.html)|` ```json ` <br> `{` <br> `"firstName": "John",` <br>`"lastName": "Smith",`<br>`"age": 25` <br> `}` <br>` ``` `|
|[脚注（Footnote）](https://markdown.com.cn/extended-syntax/footnotes.html)|Here's a sentence with a footnote. `[^1]`  <br>`[^1]`: This is the footnote.|
|[标题编号（Heading ID）](https://markdown.com.cn/extended-syntax/heading-ids.html)|`### My Great Heading {#custom-id}`|
|[定义列表（Definition List）](https://markdown.com.cn/extended-syntax/definition-lists.html)|`term  `<br>`: definition`|
|[删除线（Strikethrough）](https://markdown.com.cn/extended-syntax/strikethrough.html)|`~~The world is flat.~~`|
|[任务列表（Task List）](https://markdown.com.cn/extended-syntax/task-lists.html)|`- [x] Write the press release`<br>`- [ ] Update the website`<br>`- [ ] Contact the media`|

### 1.3 SCUTEEE 特殊语法

SCUTEEE 有一些特殊的语法，这些语法在其他平台可能无法正常显示，并且在 VScode 或 Obsidian 中可能需要配置才能正常显示。

#### 1.3.1 改变图片宽度

有些图片太大，在电脑屏幕上会特别突兀，可以在图片的 URL 后面加 `#w-1/2`，使得宽度就变为一行文字的宽度的 1/2（注意，不是图片宽度的 1/2）。另外，需要注意的是这种方法只会在大屏幕下生效，小屏幕下还是会保持原宽度，以保证小屏幕下的可读性。

原图：

![示例图片](images/vintage-kunst-vogel-bunt.webp)

```markdown
![示例图片](images/vintage-kunst-vogel-bunt.webp#w-1/2)
```

![示例图片](images/vintage-kunst-vogel-bunt.webp#w-1/2)

> [!CAUTION]
> 待讨论：是否需要其他图片样式？

#### 1.3.2 多张图片平铺显示

如果想让多张图片平铺显示，可以将多张图片放一起，中间不加空行，然后链接后面加 `#tile`。如果图片太多，会自动换行。

```markdown
![图片1](images/1.webp#tile)
![图片2](images/2.webp#tile)
![图片3](images/3.webp#tile)
![图片4](images/4.webp#tile)
```

![图片1](images/1.webp#tile)
![图片2](images/2.webp#tile)
![图片3](images/3.webp#tile)
![图片4](images/4.webp#tile)

#### 1.3.3 提示块（Alert）

提示块（alert）是一种特殊的，带颜色的引用，在 [Hugo](https://gohugo.io/render-hooks/blockquotes/#alerts)、[Github](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts)、[Obsidian](https://help.obsidian.md/Editing+and+formatting/Callouts)、[Typora](https://support.typora.io/Markdown-Reference/#callouts--github-style-alerts) 中都支持，在 VS Code 中安装 Markdown Alert 插件后也能支持。它的格式是：

```markdown
> [!NOTE]
> 文字
> 文字
```

第一行的 `NOTE` 决定了其颜色，一共有五种颜色：

- `NOTE` 蓝色
- `TIP` 绿色
- `IMPORTANT` 紫色
- `WARNING` 黄色
- `CAUTION` 红色

它们的效果如下：

> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.

可以合理使用颜色来对不同内容进行区分，比如某个例题的题干和答案可以用绿色和蓝色区分。

#### 1.3.4 数学公式

SCUTEEE 使用 mathjax v3 来显示数学公式，它使用 LaTeX 语法，网上有很多教程，比如：[MathJax与LaTex的一点总结](https://zhuanlan.zhihu.com/p/568747716)、[基本数学公式语法(of MathJax)](https://blog.csdn.net/ethmery/article/details/50670297)。有两种方式插入数学公式：对于行内公式，用 `$` 包裹公式即可。比如 `$E = mc^2$`，显示为 $E = mc^2$；对于行间公式，则用 `$$` 包裹公式，比如：

```latex
$$
E = mc^2
$$
```

$$
E = mc^2
$$

> [!CAUTION]
> 注意，需要在头信息中加入 `math: true` 字段。具体可见下面的“头信息”一节。

#### 1.3.5 流程图

SCUTEEE 使用 [mermaid](https://mermaid.js.org/) 显示流程图，方法是将代码块的语言设置为 mermaid，然后在代码块内写。

    ```mermaid
    graph TD;
        A-->B;
        A-->C;
        B-->D;
        C-->D;
    ```

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

> [!CAUTION]
> 注意，需要在头信息中加入 `mermaid: true` 字段。具体可见下面的“头信息”一节。

## 2 SCUTEEE 文章基本构成

在了解完的 Markdown 语法后，我们就可以开始写文章了。

### 2.1 文章的文件组织

SCUTEEE 中有两类文章，一类是“单篇”文章，另一类是“系列”文章。

对于“单篇”文章，如果只是写一篇文章，文章中不需要其他外部文件（比如图片），那么可以直接新建一个 `.md` 文件即可。

```text
a_solo_article.md
```


如果需要引用外部文件，则新建一个文件夹，然后在里面新建一个 `images` 文件夹用于存放图片、新建 `assets` 文件夹用于存放其他文件、新建一个 `index.md` 文件用来写文章。

```text
a_new_article/
├─ images/
├─ assets/
└─ index.md
```

---

对于“系列”文章，则可以新建一个文件夹，里面新建一个 `_index.md`，作为系列的“入口”。然后，新建一个 `images` 文件夹用于存放图片，新建 `assets` 文件夹用于存放其他文件（没有其他文件也可以不建这个文件夹），多篇文章都放里面。这多篇文章共用图片。

```text
a_series_of_articles/
├─ images/
├─ assets/
├─ _index.md
├─ 1.md
├─ 2.md
└─ 3.md
```

如果图片很多，也可以针对每一个文章新建一个文件夹：

```text
a_series_of_articles/
├─ _index.md
├─ 1
   ├─ images/
   ├─ assets/
   └─ index.md
├─ 2
   ├─ images/
   ├─ assets/
   └─ index.md
└─ 3
   ├─ images/
   ├─ assets/
   └─ index.md
```

或者折中一下，每一章新建一个文件夹：

```text
a_series_of_articles/
├─ _index.md
├─ 1
   ├─ images/
   ├─ assets/
   ├─ 1.1.md
   └─ 1.2.md
├─ 2
   ├─ images/
   ├─ assets/
   ├─ 2.1.md
   └─ 2.2.md
└─ 3
   ├─ images/
   ├─ assets/
   ├─ 3.1.md
   └─ 3.2.md
```

可以根据需求，自行选择以上三种“系列”文章的组织方式。

### 2.2 文件/文件夹命名

如果是放在“博客”栏目的文章，应该按照 `2024-12-1-标题` 的格式命名，其中，日期应该是新建文件的日期。

如果是系列文章，那么应该在文件/文件夹名字前加入序号，比如：

```text
概率论
├─ 1-概率论的基本概念
   ├─ 1.1-概率论的基本概念.md
   └─ 1.2-全概率公式md
└─ 2-随机变量
   ├─ 2.1-一元离散随机变量.md
   └─ 2.2-一元连续随机变量.md
```

SCUTEEE 支持 3 级序号，即 `1`、`1.1` 和 `1.1.1` 都是可行的，但是 `1.1.1.1` 则只会考虑前 3 级。

> [!TIP]
> 为什么需要这样命名？
>
> 1. 这样命名可以在电脑上和网站中以同样的顺序显示
> 2. 多级命名，可以更好的组织文章，同时也更方便在中间插入文章（相比于只有一级序号）
> 3. 在文件名中设置序号，好于在文件头信息中、或其他文件中设置排序（初版 SCUTEEE 就是需要在另一个文件中设置顺序）

### 2.3 头信息

在文章开头，我们需要加入头信息（Front Matter）。头信息开头和结尾都是 `---`（三个减号），然后中间放文章的信息。最基础的信息包括标题、日期：

```yaml
---
title: 标题
date: 日期，格式是：2024-12-01 12:00:00 +0800
---
```

如果想要显示作者，可以加入：

```yaml
authors:
  - name: 作者1
    image: 头像（可选）
  - name: 作者2
    iamge: 头像
```

此外，如果需要显示数学公式或流程图，需要加入：

```yaml
math: 是否显示数学公式
mermaid: 是否显示流程图
```

最后推荐加上 tags，以便文章相互关联、分类：

```yaml
tags: [标签1, 标签2]
```

---

对于“系列”文章，需要在 `_index.md` 文件中额外写入：

```yaml
type: series
```

“系列”文章通常有相似的头信息，为了节省时间，可以在 `_index.md` 中写入 `cascade` 字段，`cascade` 内的字段会应用到“系列”中的每一个文章，但会被文章内部相同的字段覆盖。

```yaml
cascade:
  math: true
  authors:
    - name: 作者
      image: 头像
```

### 2.4 摘要

在“博客”中的文章应该在头信息后面，写摘要，然后单独写一行 `<!--more-->`，再写正文。比如：

```markdown
---
title: 标题
date: 2024-12-01 12:00:00 +0800
---

摘要，简要概括文章

<!--more-->

正文
```

## 3 写作规范

这节的规范分为三个程度：「推荐」、「应当」、「必须」

### 3.1 排版规范

Markdown 语法「应当」采用如下规则：

> [!TIP]
>
> - 段落开头不用缩进（空两格），因为段落之间的空行足以区分两个段落
> - 标题、段落、列表、代码、表格、LaTeX 等段元素之间「必须」有一个空行
> - 标题「必须」从 「##」开始，因为「#」是用来写文章标题的，而文章标题已经在头信息中写过了。
> - 加粗和斜体「应当」用 `*`，而不应该用 `_`

中英文混排「应当」采用如下规则：

> [!TIP]
>
> - 英文和数字使用半角字符
> - 中文文字之间不加空格，除非是强调，比如在粗体和一般字体之间加空格
> - 中文文字与英文、阿拉伯数字及 @ # $ % ^ & * . ( ) 等符号之间加空格
> - 中文标点之间不加空格
> - 中文标点与前后字符（无论全角或半角）之间不加空格
> - 如果括号内有中文，则使用中文括号
> - 如果括号中的内容全部都是英文，则使用半角英文括号
> - 当半角符号 / 表示「或者」之意时，与前后的字符之间均不加空格
> - 其它具体例子推荐 [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines)

中文符号「应当」使用如下写法：

> [!TIP]
>
> - 用直角引号（「」）代替双引号（“”），不同输入法的具体设置方法请 [参考这里](http://www.zhihu.com/question/19755746)，对于微软拼音，可以在「设置」-「词库和自学习」-「添加或编辑自定义短语」设置
> - 省略号使用「……」，而「。。。」仅用于表示停顿
> - 其它可以参考 [知乎规范](http://www.zhihu.com/question/20414919)

### 3.2 表达规范

表达方式，「应当」遵循 [《The Element of Style》](http://www.sciwriting.cn/download/elos.pdf)，中文翻译见 [《风格要素》](https://zhuanlan.zhihu.com/p/64998628)，以下是一些要点：

> [!TIP]
>
> - 使段落成为文章的单元：一个段落只表达一个主题
> - 通常在每一段落开始要点题，在段落结尾要扣题
> - 使用主动语态
> - 陈述句中使用肯定说法
> - 删除不必要的词
> - 避免连续使用松散的句子
> - 用相似的形式表达并列的观点
> - 将相关的词放在一起
> - 写概述时要保持统一的时态（这里指英文中的时态，中文不适用，所以可以不理会）
> - 将强调的词放在句末

为了让文风通畅，「推荐」遵循：

> [!TIP]
>
> - 写作时要置自己于幕后（Place yourself in the background）
> - 写作要顺其自然（Write in a way that comes naturally）
> - 不要写得华而不实（Do not overwrite）、
> - 不要言过其实（Do not overstate）
> - 不要故作谈笑风生（Do not affect a breezy manner）
> - 使用正规的拼写（Use orthodox spelling）
> - 要写得清楚明了（Be clear）
> - 不要强加自己的观点（Do not inject opinion）
> - 使用规范的语言（Prefer the standard to the offbeat）

### 3.3 LaTeX 规范

理工科文章涉及大量的公式，「应当」按照 [GB/T 7713.2—2022学术论文编写规则](https://wjk.usst.edu.cn/2023/0210/c13371a285730/page.htm) 进行规范。要点如下：

1. 正确使用正斜体，「必须」符合 [GB/T 3102.11](https://journal.cricaas.com.cn/attached/file/20210517/20210517161953_566.pdf) 的规定

   「必须」使用斜体的情况：

   - 变量（如 $x,y$）
   - 变动的副标（如 $\sum_i x_i$ 中的 $i$）
   - 函数（如 $f,g$）

   「必须」使用正体的情况：

   - 有定义的已知函数（如 $\sin, \ln, \exp$ 以及）
   - 数学常数（如 ${\rm e}=2.7\cdots$，$\pi=3.14\cdots$）
   - 已定义的算子（如 $\dif f/ \dif x$ 中的 $\dif$）
   - 单位（如 $10 {\rm kg}$）

   其他「推荐」情况：

   - 如果单个字母表示某个词的缩写，则宜用斜体；如果是多个字母表示某个词的缩写，则宜用正体。比如用 $v$ 表示 velocity，而 $v_{\min}$ 中用 $\min$ 表示 minimum

2. 在行文中，「推荐」避免使用多于 1 行的表达式，比如 $\exp(x)$ 优于 $e^x$
3. 在公式中，「推荐」避免使用多于 1 个层次的上下标，比如 $P_{1,\min}$ 优于 $P_{1_{\min}}$
4. 在公式中，「推荐」避免使用多于 2 行的表达形式，比如：
  
   $$
   \frac{\exp(x)}{\sin(x/2)}
   $$

   优于

   $$
   \frac{e^x}{\sin \frac{x}{2}}
   $$

5. 多行公式，「应当」用 `\begin{align}` 和 `\end{align}` 包围（或者 `aligned` 或 `align*`），每行用 `&` 对齐。
6. 对于过长的公式，「推荐」在符号前面换行，上一行末尾不重复这一符号。比如：

   $$
   \begin{align*}
   f(x，  y)= & f(0， 0)+\frac{1}{1 !}\left(x \frac{\partial}{\partial x}+y \frac{\partial}{\partial y}\right) f(0， 0) \\
   & +\frac{1}{2 !}\left(x \frac{\partial}{\partial x}+y \frac{\partial}{\partial y}\right)^{2} f(0， 0)+\cdots \\
   & +\frac{1}{n !}\left(x \frac{\partial}{\partial x}+y \frac{\partial}{\partial y}\right)^{n} f(0， 0)+\cdots
   \end{align*}
   $$

推荐阅读：

- [ChinaTeX 数学排版常见问题集](https://static.latexstudio.net/wp-content/uploads/2018/02/ChinaTeXMathFAQ_V1.1.pdf)

## 4 编辑器设置

SCUTEEE 推荐两款编辑器

- [Obsidian 官网](https://obsidian.md/)：最好用的「所见即所得」Markdown 编辑器，推荐 Markdown 初学者/希望专注写作的同学使用；
- [Visual Studio Code 官网](https://code.visualstudio.com/)：强大的代码编辑器，推荐想要一边编程、一边记笔记的同学使用。

去官网找对应的安装包，安装完成后，需要进行如下设置，才能写出符合 SCUTEEE 规范的文章。

### 4.1 Obsidian

安装好 Obsidian 后，新建一个仓库，并进行如下设置：

**编辑器设置**：

- 严格换行：开启
- 显示行号：开启

![编辑器设置](images/ob_编辑器设置.webp#w-2/3)

**文件与链接设置**：

- 内部链接：基于当前笔记的相对路径
- 使用 Wiki 链接：关闭
- 检测所有类型文件：开启
- 附件默认存放路径：当前文件所在文件夹下的指定的子文件夹
- 子文件夹名称：images

![文件与链接设置](images/ob_文件与链接设置.webp#w-2/3)

### 4.2 VS Code

VS Code 推荐使用默认的 Markdown 预览，并安装如下插件来正确显示：

- 提示块：[Markdown Alert](https://marketplace.visualstudio.com/items?itemName=kejun.markdown-alert)
- Mermaid：[Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)

### 4.3 格式化

推荐采用 [markdownlint](https://github.com/DavidAnson/markdownlint/tree/v0.36.1/doc) 格式化，但里面的规则不一定要全部遵守。VS Code 的商店中已经有这个插件，而 Obsidian 的这个插件还在测试中（[Obsidian Markdownlint Plugin](https://github.com/ebullient/obsidian-markdownlint)），可以用 Linter 代替。

## 5 补充

### 5.1 `.gitignore`

当上传文章到 Github 时，有一些东西无需上传的，比如编辑器的设置。我们需要在根文件夹下新建一个 `.gitignore` 文件，告诉 git 哪些需要 ignore（忽略），里面的内容为：

```text
# Visual Studio Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
!.vscode/*.code-snippets

# Local History for Visual Studio Code
.history/

# Built Visual Studio Code Extensions
*.vsix

# macOS
.DS_Store

# Obsidian
.obsidian/*
```
