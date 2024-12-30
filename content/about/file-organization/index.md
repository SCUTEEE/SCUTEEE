---
title: SCUTEEE 文件组织
date: 2024-12-17 19:57:00 +0800
authors:
  - name: ToddZZF
type: docs
---

<!--more-->

「文件组织」是一件很复杂的事情，这不仅仅包括文件的目录结构，还包括这些文件的存储方式、版本控制、展示与下载方式等等。这是非常值得讨论的，尤其是对 SCUTEEE 以及类似的资源共享站。首先我们来看看一些常见的方案。

## 常见方案

我们主要关注以下几点：

- 资源（比如某课程的 PPT）
  - 存储
  - 展示
- 信息（比如一些课程评价）
  - 存储
  - 展示

### 案例一

[OpenWHU](https://github.com/openwhu)，武汉大学课程资料整理-WHU课代表计划，采用如下组织方式：

- 资源
  - 存储：[Github](https://github.com/openwhu/OpenWHU)
  - 展示：Alist
- 信息
  - 存储：[Github](https://github.com/openwhu/openwhu.github.io)
  - 展示：MkDocs

OpenWHU 的课程资源全都存储在 <https://github.com/openwhu/OpenWHU>，但是看 Alist 网盘中，上传存在另一个目录中。根据这个 [issue](https://github.com/openwhu/OpenWHU/issues/92)，他们以前是将仓库克隆到服务器上，然后在服务器上搭建 Alist。然后另外开一个 Alist 文件夹以供上传（当然，他们也接受 github pull requests、邮件等方式），但是最终还是会上传到 Github 上。

他们 Github 上的存储的文件大小为8.13GB，只有少部分 Zip 文件启用了 LFS。Github 对一般的仓库并没有严格限制，只对 LFS 文件有 1GB 的限制。因此他们应该还是白嫖 Github，唯一需要付费的只有服务器。

它们的信息只包含项目介绍，以及一些选课攻略，与资源的关系不大。

### 案例二

[浙江大学课程攻略共享计划](https://github.com/QSCTech/zju-icicles)，很多学校都受该项目的启发（浙大这个项目是 16 年创立的）。该项目组织方式如下：

- 资源 & 信息
  - 存储：[Github](https://github.com/QSCTech/zju-icicles)
  - 展示：[MkDocs](https://qsctech.github.io/zju-icicles/)

该项目没有专门的「信息」站，全部都是资源，Github 上的仓库大小为 5.02GB，每个文件夹放一门课程（有些学校会按 Branch 区分学院）。展示则是用 Python 获取文件树，融合对应课程下的 README.md 再输出 Markdown 文件，从而使 MkDocs 承载「信息」的功能。

这类项目所有东西都放在一个 Github 仓库中，所以「几乎不可能」把整个仓库 clone 下来。这类仓库推荐的上传方式都是利用网页端直接上传，具体是（以浙大的操作过程为例）：

1. 首先Fork本项目
2. 上传文件到已有文件夹：打开对应文件夹，点击绿色Download按钮旁的upload，上传你的文件。
3. 上传文件到新文件夹：打开任意文件夹，点击绿色Download按钮旁的upload，把浏览器地址栏中文件夹名称改为你想要新建的文件夹名称，然后回车，上传你的文件。

下载也是需要到仓库内下载，但是 Github 只支持单独下载某个文件，下载整个文件夹需要借助第三方工具，比如（中科大）：

> 链接下载文件夹的功能是由我们定制的 [gitzip](https://xovee.github.io/gitzip/) 实现，并非 GitHub 官方提供，如若因 GitHub API 访问限制的缘故而无法成功下载文件夹的话，请使用替代方案：（1）KinoLien 开发的 [gitzip](https://kinolien.github.io/gitzip/)；（2）Minhas Kamal 开发的 [DownGit](https://minhaskamal.github.io/DownGit/#/home)；（3）zhoudaxiaa 开发的 [DownGit](http://downgit.zhoudaxiaa.com/#/home)。

### 案例三

[HOA.MOE](https://github.com/HITSZ-OpenAuto)，哈工大（深圳）自动化课程攻略共享计划。

- 资源：
  - 存储：[Github](https://github.com/HITSZ-OpenAuto)
  - 展示：[Hugo](https://hoa.moe/)
- 信息
  - 存储：[Github](https://github.com/HITSZ-OpenAuto)
  - 展示：[Hugo](https://hoa.moe/)

HOA 选择将课程分开为独立的仓库，每个课程下有 README.md 存储课程信息，然后通过主站汇总。细节上，每次课程 README 更新后，会触发主站的 github workflow，自动运行程序提取课程 README，生成主站下的 markdown 文件（程序自动 Commit），然后再触发 Cloudflare 部署网站。

为了加速下载资源，HOA 还搭建了镜像站。

分开存放使得单独下载某门课程的所有文件成为可能，并且贡献者共享资料也更加方便。

### 案例四

[MITMath](https://github.com/mitmath), educational materials for MIT math courses.

- 资源：
  - 存储：[Github](https://github.com/mitmath)
  - 展示：Github README，及 Github page

MITMath 把每一门课程作为一个仓库，相关信息均在 README 中。少数仓库有 Github Page，但也只是 README 的内容。这个就只是老师放 PPT 等课程材料，不涉及「课程攻略」之类的内容。

## 方案分析

在浏览上述方案时，一个疑惑始终萦绕我心头：Why Github？你可能会说：

- 首先，Github 是免费的
  - 节省存储和下载费用
- 其次，Github 是最大的开源项目托管平台
  - 更多人会关注并参与到我们的开源项目中
- 接着，Github 有良好的社区支持
  - 通过 Issues 和 Discussions 获得用户反馈
- 最后，Gitub 提供了自动化工具
  - GitHub Actions 自动化脚本、运维工具

我认为唯一的原因只是「Github 是免费&靠谱，并且所有人都能上传/下载」，因为上述的大部分方案根本没用到 Github 的管理功能——Git。对于 PPT、WORD、PDF，几乎不会修改（我想没有人会修改往年试卷吧？），也就不必版本控制了，我们只需要上传/下载功能。虽然 Github 不适合干这种事情，但是我们只是把 Github 当作一个基础，在此基础上我们可以搭建镜像站/卫星站（借助 Alist 或 Cloudreve），优化下载速度。

课程信息很可能是需要频繁变动的（至少每年都会变），这类文件和代码的管理方式类似，需要用到 git 的功能，因此很适合在 Github 上管理。

既然「资源」和「信息」的管理方式不同，那么是否应该把他们放一起呢？分开放更适合 Github 管理，但放一起更符合逻辑（都是同一门课的东西），或者应该折衷一下，放同一个仓库的不同分支，还是放不同仓库但是用 submodule 结合？我认为这取决于「资源」是否影响「信息」的管理，就比如我想 `git clone` 信息，但不能让「资源」影响了我的下载速度。以我对 `git` 有限的了解，我认为「资源」和「信息」放同一个仓库的不同分支是更好的选择，因为：

- 放同一个仓库，显然更方便查找和管理
- 可以只下载 「信息」：只需要克隆指定分支 `git clone --branch <branch-name> --single-branch <repository-url>`
- 更方便集成子模块：主仓库添加子模块时可以指定分支 `git submodule add -b <branch-name> <repository-url> <path-to-submodule>`，并且主仓库下载时（`git clone --recurse-submodules <A-repository-url>`）或更新时（`git submodule update --init --recursive`），只会下载指定的分支，不会下载其他模块。

所以我认为，最优方案是：将课程分开为一个个仓库，main 分支放「信息」，新建一个 resources 分支放「资源」。两个分支不交互（也没必要交互）。

---

为了将课程信息集合起来，通过网站展示，我们有两种方法：

1. 方法一：利用 git 的 `submodule`，适合大量的信息（比如我的笔记）
   - 缺点一：子仓库更新，主仓库需要手动 `git submodule update --remote`（这步可以在 Cloudflare 调用 Hugo 前做，可以不 Commit 到 Github。）
   - 缺点二：不支持 edit in Github
2. 方法二：利用 Hugo 的 `Content Adapter + transform.Unmarshal`，适合少量的信息，比如只有一页 README
   - 构建时更新，优点是实时性更强，缺点是每次构建都拉取，很慢
3. 方法三：利用 Hugo 的 Module
   - 缺点：同方法一；另外还要额外下载 golang，感觉比方法一更复杂……；另外还不支持 [edit in Github](https://discourse.gohugo.io/t/get-module-source-from-page/23208)

为了在课程仓库更新后，及时更新网站，需要在课程仓库设置 Workflow，用于触发 Cloudflare 重新编译部署网站。

另外，上面方法在需要预览时会很麻烦。比如子仓库有一个新的 branch，我们希望预览这个 branch，那么需要在主仓库也新建一个 branch，然后修改主仓库的 submodule 的 branch/或修改 `Content Adapter`，然后才能预览。（或许可以弄一个 workflow 来实现？）

以上只是一点点小分析，还有很多坑要踩了才知道。

## SCUTEEE 的方案

### 主站

主站存储在 <https://github.com/SCUTEEE/SCUTEEE>，其本质上是一个 [Hugo](https://gohugo.io/) 静态网站，其有着最基本的 Hugo 文件结构：

- `content`：文章内容
- `themes`：主题
- `config`：网站设置

简单来说 Hugo 会读取网站设置，然后以设置的主题为模板，将文章内容渲染成网页。渲染过程是在 Cloudflare Pages 中执行的，并且部署到 Cloudflare 的服务器上。

> [!note] Cloudflare Pages
>
> Cloudflare Pages 是 Cloudflare 提供的一种托管静态网站和前端应用的服务。我们看重其如下特点：
>
> 1. 全局边缘网络加速：Cloudflare 的全球内容分发网络（CDN）能够将你的静态内容分发到世界各地的多个节点，从而提升网站的访问速度和可靠性。
> 2. 预览部署：Cloudflare Pages 提供了预览部署功能，开发者可以在每次提交代码时生成预览链接，以便团队成员或客户在代码正式发布之前查看网站效果。
> 3. Git集成：Cloudflare Pages 可以与 GitHub 和 GitLab 完全集成，简化了代码提交和部署的流程。开发者可以将网站托管与源代码管理紧密结合。
>
> 但需要注意，Cloudflare Pages 是有限制的：
>
> 1. 每个项目最多 10 个自定义域名
> 2. 每个站点最多 20,000 个文件
> 3. 单个文件最大 25 M
>
> 因此，Cloudflare Pages 并不适合分发大文件。另外，小文件（比如图片）也最好别放太多（我们可能需要一个 Python 程序，在 Hugo 编译前，将本地文件上传到图床并替换 Markdown 内的链接）。

`hugo.yml` 和 `themes` 需要较强的编程能力以及对 Hugo 的深入了解（不了解的同学推荐借助 GPT），所以在此不赘述。需要注意的是，`themes` 中的主题用过 submodule 引入到主站中，而不是用 `go mod`，以方便开发者修改。

`content` 中的内容分为：

- `index.md` 主页
- `courses` 课程
- `majors` 专业
- `blog` 博客
- `about` 关于

其中，除了 `courese` 引用外部仓库，其余都存储在主站内。`courses` 的引用有以下方式：

- 通过 `hugo module` 引用外部仓库
- 通过 `courses/_content.gotmpl` 生成
  - 具体原理是 `_content.gotmpl` 会读取 `data/courses.yml`，然后利用 github api 获取对应的 README 文件，再生成网页

`majors` 中，每一个专业对应一个文章，里面手动列出所有的课程。此外还可以写一些关于本专业的建议。

`blog` 就是正常的博客，每个年份的博文对应底下的一个文件夹，并且博文开头必须是年月日，如 `2025-01-01-标题.md`，注意要月和日不足两位的要补 0. 如果博客这个模块未来有很多文章，那么可能会变为单独的仓库。

`about` 中有对 SCUTEEE 的介绍，以及一些投稿相关的指南。

从上面可以看出，SCUTEEE 的主站其实非常简单。

### 课程

每个课程都是 Github 上的一个仓库。关于仓库命名，由于 Github 仓库只支持英语，因此我们需要将中文课程名翻译成英语。最好是对中文进行直译，但如果直译太长了，可以适当缩减。在 Description 中写课程中文。

每个课程仓库有两个分支：

- `main` 分支：课程信息、课程笔记等 markdown 内容
- `resources` 分支：课程资料，比如 word、ppt、pdf

这两个分支创建好后，就不应该相互关联。SCUTEEE 为所有课程创建了模板：[course-template](https://github.com/SCUTEEE/course-template)，所有课程仓库都从该模板创建，创建时请确保勾选 `Include all branches`.

`resources` 分支下，已经建立了四个文件夹：

- `assignments` 作业
- `exams` 考试
- `lab` 实验
- `slides` PPT

把文件存到对应的文件夹内就行，可以通过 github 网页端直接上传文件/文件夹。注意事项写在了各文件夹下的 `README.md` 中。

`main` 分支专门用来放需要在网站展示的 `markdown` 文件。其中，根目录下有 `README.md` 和 `_index.md`，因为我们希望在 Github 仓库内也能看到课程的基本信息，所以把基本信息全写在 `README.md` 内，而 `_index.md` 只提供基本的 Front Matter（课程名、series、github链接）。关于 `main` 分支中的 markdown 笔记这方面我暂时还没确定，暂定的方案是新建各章节目录放进去，等以后贡献的人多了，再仔细想怎么做。
