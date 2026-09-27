# 个人学术主页 · 蓝色中英双语版

直接用浏览器打开本目录的 `index.html`。导航会打开独立的 HTML 页面，支持浏览器前进、后退及直接打开子页面。无需安装依赖或构建。

中文入口是 `zh/index.html`。页面右上角的「中文 / English」会打开当前页面的另一语言版本；同一语言内的所有导航和文章链接保持该语言。语言切换不依赖 JavaScript 或浏览器存储，直接打开本地文件也可使用。

## 文件

- `index.html`：个人介绍、三个研究关键词、最新四篇研究专栏图文卡片（桌面两列两行、手机单列，只显示代表图、年份、标题和阅读入口）、三篇代表论文。
- `research.html`：保留的研究方向资料页，已从顶部导航和首页移除入口。
- `publications.html`：顶部左侧为两篇待发表稿件，右侧为 Google Scholar 引用表与年度柱状图；下方七篇已发表论文中，六篇附有相应研究专栏入口。
- `cv.html`：在线展示教育、复旦博士后任职、科研经历及荣誉，不提供简历下载。
- `contact.html`：复旦邮箱、单位、ResearchGate、ORCID、Google Scholar 和 Web of Science。
- `assets/yangbo-ye.jpg`：用户提供的两寸证件照，保留原图比例；桌面显示宽度为 180px。
- `CONTENT_REVIEW.md`：资料来源、已填内容和待更新事项，仅供维护时参考。
- `highlights.html`：Research Highlights 全部文章列表，完整简介在左、代表图在右，小屏幕上下排列。
- `assets/highlights/`：第一、二、五篇代表图的指定面板裁图；其余文章复用正文图片。
- `highlight-template.html`：研究介绍文章模板，明确标注预览，并设置 noindex。
- `zh/`：页面与文章的中文版本，与英文页面一一对应。
- meiyu-2020.html：2020 年梅雨与华南高温的条件归因研究介绍。
- `southwest-rainfall-2020.html`：2020 年西南持续暴雨的故事线与概率归因研究介绍。
- `compound-2020.html`：2023 年 WCE 论文介绍，结合故事线与概率方法归因 2020 年暴雨—高温空间复合事件。
- `north-china-heat-2023.html`：华北端午高温的快速归因，原论文于2023年在线发表、编入2024年ERL卷期。
- `cold-2023.html`：2025年npj论文介绍，解释2023年12月东部寒潮的环流成因、人为影响与未来变化。
- `school-heat-2024.html`：2026年WCE论文介绍，研究2024年秋季开学高温的归因与儿童暴露变化。
- `assets/school-heat-2024/`：选取原文Fig. 1a–b、3e、4、6c–d，网页依次编号为图1至图4。
- `assets/cold-2023/`：原论文Fig. 1、2、4、5，网页依次编号为图1至图4。
- `assets/north-china-heat-2023/`：从原论文直接提取的五张完整配图。
- `assets/compound-2020/`：从原论文直接提取的四张完整配图。
- `assets/southwest-rainfall-2020/`：原论文两张完整配图。
- assets/meiyu-2020/：从作者本地论文直接提取的四张完整原图。
- `styles.css`：统一蓝色配色、布局、手机适配、深色模式。
- `theme.js`：深色模式及年份；关闭 JavaScript 仍可阅读和导航。
- `original/index.html`：原稿备份，未修改。

## 后续更新资料

1. 本次已填入姓名、照片、教育经历、现职与邮箱。变更信息时同步中英文版本。
2. 照片可用同名文件替换，并同步 HTML 图片尺寸；保持有姓名 alt 文本。
3. 新论文提供题目、作者、期刊、年份和 DOI，更新论文页与首页代表论文；有真实 PDF、代码、数据地址时才添加论文资源链接。
4. 更新任职起始年月和最近一年的经历，仅在线展示，不添加简历下载入口。
5. Scholar、ORCID 和 Web of Science 已按用户提供的账号加入联系页；若补充 GitHub 地址，再加入。

页面沿用初稿的研究主题，并补充简历中有依据的研究经历；研究表述仍需在正式发布前由本人核对。博士后身份与合作导师采用用户本次确认信息，未推测任职起始日期。导航在各 HTML 中显式保留，修改名称或路径时同步所有页面即可。

## 添加 Research Highlights 文章

1. 复制根目录的 `highlight-template.html` 和 `zh/highlight-template.html`，分别保存成同名的新文件，例如 `heatwave-study.html`。当前模板仅展示结构，不含虚构研究结果。
2. 在两种语言中填写文章标题、简介，以及背景、方法、结果、讨论四部分。简介使用 article-overview 独立着色区域；图片使用 figure/article-figure 放在相关段落间，figcaption 仅放图题。文末放论文引用，其后用 article-story 着色区域展示“背后的故事”。标题和描述元数据也需修改；素材来源记录在 CONTENT_REVIEW.md。
3. 新文章两个文件的语言切换链接与 `rel="alternate"` 链接，都改为新文件名。中文页保留共享资源的 `../` 路径。
4. 内容正式核实后删除文章中的预览提示，以及 `meta name="robots" content="noindex"`；有真实发布日期时再加入日期。
5. 在中英文 `highlights.html` 中添加该文的标题、完整简介、代表图和链接；首页的 highlight-grid 只保留最新四篇，不显示简介；专栏的 highlight-list 保留全部文章与完整简介。卡片使用 data-tone="1" 至 "5" 的五种蓝色循环，同一文章在各页保持同色。完整简介与文章的 article-overview 各段保持一致，后续修改文章简介时同步专栏列表卡片，首页卡片无需添加简介。
6. 新文章加入 `check_site.py` 的 `ARTICLES` 元组；正文页面会自动使用 Highlights 导航高亮。

这是静态文章专栏，没有在线编辑后台。修改 HTML 后即可预览，无需构建。

## 直接在页面编辑文章

本地打开中英文研究文章后，文章上方会出现“编辑模式”。点击后可直接修改标题、各节正文和图题，字数与阅读时间会自动更新；图片、论文链接和导航不在编辑范围内。中英文独立修改，不自动翻译。

- “保存 HTML”：支持文件保存窗口的浏览器中可用。选择当前文章原文件即可覆盖；中文原文件位于 `zh/`，英文位于网站根目录。
- “下载副本”：浏览器不支持文件保存窗口时也可用。保留文章原文件名（例如 `meiyu-2020.html` 或 `southwest-rainfall-2020.html`），放回对应目录并替换原文件。只下载副本不会自动更新原网页。
- “取消”：恢复进入编辑模式前的内容；有修改时会先询问是否放弃。未保存便刷新或离开时，浏览器会尝试提示。

保存输出保留相对资源路径与编辑入口，并同步文章自身的浏览器标题、描述、阅读提示和更新日期（按保存时的本地日期）；首页/文章列表上的介绍不会自动改动。编辑入口只在本地文件模式显示，部署后不显示。没有自动草稿备份，请及时保存。

后续文章可引入 `article-editor.js`（中文页使用 `../article-editor.js`）启用相同功能；脚本使用现有文章结构，不需要安装依赖。

直接以本地文件打开时，浏览器可能限制主题偏好的跨页保存；每页的切换仍可用。通过正常网站地址访问时可跨页保存。

## 检查

运行 `python check_site.py` 检查页面、导航和本地链接；运行 `node check_theme.cjs` 检查主题切换和存储不可用情况。
运行 `node check_article_editor.cjs` 检查中英文阅读统计、文件写入及取消/失败处理。

网站已于 2026-09-27 发布至 GitHub Pages：

- 英文：https://yeyangb.github.io/
- 中文：https://yeyangb.github.io/zh/
- 仓库：https://github.com/yeyangb/yeyangb.github.io

原 GitHub Pages 地址已启用 HTTPS，Scholar 更新已在 GitHub Actions 上成功运行。

yangboye.com 已于 2026-09-27 绑定，阿里云解析和 GitHub DNS 检查均已通过，中英文 HTTP 页面已验证可访问。自定义域名的 HTTPS 仍待 GitHub 签发证书，完成后需在仓库 Settings → Pages 开启 Enforce HTTPS。

## GitHub Pages 与引用统计自动更新

`.github/workflows/pages.yml` 已在当前仓库启用。以下步骤供迁移仓库或重新配置时参考：

1. 将网站文件、`scripts/`、检查脚本及 `.github/workflows/pages.yml` 放入仓库的 `main` 分支。若默认分支不是 `main`，修改工作流的 `push.branches`。
2. 在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**。
3. 在 **Actions → Publish website and refresh Scholar → Run workflow** 手动运行一次。工作流需要写入仓库以保存引用快照；若分支保护禁止机器人直接提交，需要在该仓库规则中允许此更新方式。
4. 后续推送到 `main` 会发布网站；每周一北京时间约 10:17 自动获取 Scholar 数据并发布，GitHub 的调度可能延迟。也可随时手动运行。

统计来自公开主页 `https://scholar.google.com/citations?user=EZSfJd0AAAAJ&hl=en`。初始数据于 2026-09-27 直接读取并与用户截图核对：引用 345 / 341，h-index 7 / 7，i10-index 6 / 6（全部 / 2021 年以来）。柱状图使用主页中的真实年度数值，显示最近七个有数据的年份，不从截图估算，也不按年度柱状图反推总引用数。

`scripts/update_scholar.py` 只使用 Python 标准库，每次请求一次公开主页，不需要 API 密钥。数据通过检查后写入 `assets/scholar/stats.json` 并同时更新中英文论文页。卡片直接写在 HTML 中，本地文件和关闭 JavaScript 时仍可查看。

Google Scholar 可能限制来自 GitHub 的访问；遇到验证页面、访问失败或页面格式变化时，流程保留上次成功的数据与原更新日期，并在 Actions 中记录警告，不会用零值覆盖。自动获取不保证每周都成功。公开仓库长期无活动时 GitHub 可能停用定时工作流，可在 Actions 中重新启用。

本地更新：`python scripts/update_scholar.py`。离线检查：`python check_scholar.py`。请勿手动编辑论文页 `scholar-stats` 标记之间的内容，这一部分会在下次更新时重新生成。

发布包只包含网页、样式、脚本、图标和 `assets/`，不发布 `tmp/`、`original/`、维护文档、检查脚本和文章模板。参见 [GitHub Pages 自定义工作流说明](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 自定义域名解析

注册平台为阿里云万网，DNS 保持 dns27.hichina.com / dns28.hichina.com。

| 类型 | 主机记录 | 记录值 |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | yeyangb.github.io |

线路为默认，TTL 为 600 秒。GitHub Pages 的 Custom domain 设置为 yangboye.com；发布方式为 GitHub Actions，无需添加 CNAME 文件。

## 搜索引擎收录

首页标题与描述同时包含叶洋波 / Yangbo Ye，并通过 ProfilePage / Person 结构化数据关联复旦大学、ORCID、Google Scholar 和 ResearchGate。正式页面使用自引用 canonical 和完整地址的中英文 hreflang；网站地图收录 22 个正式页面，历史研究方向页不参与索引，模板不发布。

- `robots.txt`：允许抓取，指向 `sitemap.xml`。
- `sitemap.xml`：列出两种语言的首页、专栏列表、论文、履历、联系方式与六篇专栏。
- 新增文章、修改首页简介或切换正式网址后，运行 `python scripts/update_search_metadata.py`，然后运行 `python check_site.py`。首页搜索描述在该脚本中维护。
- 当前证书尚未就绪，搜索元数据暂用可访问的 `http://yangboye.com`。验证 HTTPS 正常后，将脚本中的 BASE 改为 `https://yangboye.com` 并重新生成发布；勿把无法访问的 HTTPS 地址提交为规范网址。

下一步需由网站所有者登录 Google Search Console、Bing Webmaster Tools 和百度搜索资源平台完成站点验证，再提交网站地图与首页。尚未代用户提交或完成搜索平台验证；新增元数据不等于已被收录，不保证姓名搜索排名。
