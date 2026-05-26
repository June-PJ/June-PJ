# GitHub Profile README · 部署说明

这套文件展示在 https://github.com/June-PJ 的资料页顶部。

## 一、建仓库

GitHub "Profile README" 的硬性约定：**仓库名必须与用户名完全一致**。

1. 浏览器打开 https://github.com/new
2. **Repository name** 填 `June-PJ`（严格一致，区分大小写）
3. **Public** 公开
4. **不要勾选** "Add a README"（用本目录下的 README.md）
5. 点 Create repository

建完之后 GitHub 会提示这是 profile 仓库（"You found a secret"）。

## 二、推上去

在当前目录（`d:\MyCode\June-PJ`）执行：

```cmd
git init
git branch -M main
git add .
git commit -m "feat: initial profile README"
git remote add origin https://github.com/June-PJ/June-PJ.git
git push -u origin main
```

推完访问 https://github.com/June-PJ ，README 会出现在头像下方。

## 三、激活两个 Workflow

仓库 → **Settings** → **Actions** → **General**：

1. **Actions permissions**：选 `Allow all actions and reusable workflows`
2. **Workflow permissions**：选 **Read and write permissions**（必须，否则 Action 无法 commit README / 创建 output 分支，会报 403）
3. 保存

然后去 **Actions** 标签页手动各跑一次：

| Workflow | 作用 | 频率 |
|---|---|---|
| `Latest blog post workflow` | 同步 atom.xml 最近 5 篇到 README | 每 6 小时 |
| `Generate Snake` | 生成贪吃蛇 SVG 推到 `output` 分支 | 每天 0 点（UTC）|

第一次跑 `Generate Snake` 后，仓库会多一个 `output` 分支，里面有 `github-snake.svg` 和 `github-snake-dark.svg`，README 直接引用这两个文件。**没跑之前贪吃蛇位置会显示破图，正常现象。**

## 四、设计取舍

这一版**保持克制**，砍掉了几个"看起来酷但数据稀疏时显空"的组件：

| 组件 | 状态 | 原因 |
|---|---|---|
| 顶部 banner（capsule-render） | ❌ 已砍 | 大色块，俗气 |
| 贡献热力图（activity-graph） | ❌ 已砍 | 数据稀疏时大片空白 |
| 连续打卡（streak-stats） | ❌ 已砍 | 1 天连击展示反而扣分 |
| 奖杯墙（trophy） | ❌ 已砍 | 没数据撑不起来，且经常 502 |
| 技术栈大徽章 | ❌ 已砍 | 改成纯文字 backtick 列表更克制 |
| 贪吃蛇（snk） | ✅ 保留 | 横向占位刚好能撑场，不像贡献图那样大片空白 |

**保留**：打字机标题、4 个 chip、stats 主卡 + 语言占比卡、贪吃蛇、博客同步、文字技术栈。

## 五、自定义

### 简介文案

`README.md` 里 `### 关于` 那一段一句话简介，直接改文字。

### 打字机文案

顶部 `<picture>` 块的 `lines=...` 是分号分隔的多句话。**只用英文/数字**，中文很容易把 SVG 渲染服务搞炸。

- 改文案 → 用 https://www.urlencoder.org/ 编码后替换 `lines=` 参数
- 改字号 → `size=34`
- 改颜色 → 浅色 `E68282`（珊瑚红）/ 深色 `F2B94B`（琥珀黄）

### 技术栈

`### 技术栈` 那一段是纯文字 inline code（`` `Java` ``）。需要改技术名直接改文字，不用碰图标 / 颜色。

### 数据卡配色

两个 `<picture>` 块都做了双主题，参数：

| 参数 | 浅色 | 深色 |
|---|---|---|
| 强调色 / icon | `E68282` | `F2B94B` |
| 文字色 | `475569` | `C4C4D0` |
| 背景 | `00000000`（透明） | `00000000`（透明） |
| 标题 | `hide_title=true` | `hide_title=true` |

GitHub 按访客系统主题自动切换。

### 博客同步频率

`.github/workflows/blog-post-workflow.yml` 里的 cron：

| 表达式 | 频率 |
|---|---|
| `0 */6 * * *` | 每 6 小时（默认） |
| `0 */3 * * *` | 每 3 小时 |
| `0 0 * * *` | 每天 0 点（UTC） |

**坑提醒**：`date_format` 用的是 [dateformat](https://www.npmjs.com/package/dateformat) 包语法，月份是**小写 `mm`**，大写 `MM` 是分钟。所以 `yyyy-mm-dd` 才对。

## 六、常见问题

### README 不显示

仓库名必须**严格等于** `June-PJ`。建错的话去 Settings → General → Repository name 改名，或者删掉重建。

### Action 报 403 / 写不进 README

Settings → Actions → General → **Workflow permissions** 改为 `Read and write permissions`，重跑 workflow。

### Stats 数据卡破图（502）

`github-readme-stats.vercel.app` 部署在 Vercel 免费额度上，被 GitHub IP 限流时会 502。已经在 URL 加了 `cache_seconds=14400`，第一次成功加载后 4 小时内都从 GitHub 自己的 camo CDN 取，不会重新打 vercel。如果第一次加载就破图，等几分钟刷新通常会好。如果长期破图，可以考虑自己 fork 一份 [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) 部署到自己的 Vercel 账号。

### 贪吃蛇位置破图

`Generate Snake` 还没跑过，`output` 分支不存在。Actions 页手动触发一次，等 30 秒刷新。

### 贪吃蛇配色

`.github/workflows/snake.yml` 里 `color_snake` 是蛇身颜色，`color_dots` 是 0~4 级贡献格子（从空到最满）。当前配色：

- 浅色：蛇 `E68282`，格子从浅到深 `E5E7EB → F8C5C5 → EFA5A5 → E68282 → D86060`
- 深色：蛇 `F2B94B`，格子从浅到深 `2E2E36 → 5E4F2A → 8A7330 → B89640 → F2B94B`

### 打字机不动 / 显示乱码

`readme-typing-svg.demolab.com` 对中文 URL 编码兼容差，**只放英文/数字**。
