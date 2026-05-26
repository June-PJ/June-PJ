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
| `Latest blog post workflow` | 同步 atom.xml 最近 5 篇到 README（main 分支） | 每 6 小时 |
| `Generate README Assets` | 在 GitHub 美国机房预生成所有 SVG 资源到 `output` 分支 | 每天 0 点（UTC）|

### 为什么要 `Generate README Assets`

`*.vercel.app` 在国内**根本访问不通**（HTTP 000，TCP 连接被重置）。GitHub README 上的图虽然走 camo 代理，但 camo 缓存不稳，国内访客经常看到破图。

解决方案：让 GitHub Action runner（位于美国机房，访问 vercel 没问题）每天预先把数据卡 / 贪吃蛇等 SVG 下载好，推到 `output` 分支。README 通过 `raw.githubusercontent.com` 引用 → 国内访问稳定。

第一次跑 `Generate README Assets` 后，仓库会多一个 `output` 分支，里面有：

- `stats.svg` / `stats-dark.svg`
- `top-langs.svg` / `top-langs-dark.svg`
- `github-snake.svg` / `github-snake-dark.svg`

**没跑之前所有数据卡 + 贪吃蛇都会破图，正常现象。**

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

### 数据卡 / 贪吃蛇配色

所有 SVG 资源都在 `.github/workflows/generate-assets.yml` 里生成。配色按双主题区分：

| 资源 | 浅色 | 深色 |
|---|---|---|
| stats / top-langs 强调色 | `E68282` | `F2B94B` |
| stats / top-langs 文字色 | `475569` | `C4C4D0` |
| 背景 | `00000000`（透明） | `00000000`（透明） |
| 贪吃蛇蛇身 | `#E68282` | `#F2B94B` |
| 贪吃蛇格子（0~4） | `#E5E7EB → #D86060` | `#2E2E36 → #F2B94B` |

GitHub 按访客系统主题自动加载对应文件（`*-dark.svg` 用 `prefers-color-scheme: dark`）。

**注意：贪吃蛇颜色参数必须带 `#` 前缀（按 [Platane/snk 官方文档](https://github.com/Platane/snk) 字面量用 `#`，不是 `%23`），否则解析失败 fallback 成黑色。**

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

### Stats 数据卡破图

第一次跑 `Generate README Assets` 之前，所有数据卡都是破图，正常。Actions 页手动触发一次。

如果跑过之后还是破图，去 `output` 分支看看 `stats.svg` 是否存在。不存在的话看 Action 日志，多半是 vercel 在间歇 502，重跑一次 workflow 通常就好。

### 贪吃蛇位置破图 / 全黑

破图：`Generate README Assets` 没跑过，`output` 分支不存在。Actions 页手动触发一次。

全黑：颜色参数没加 `#` 前缀。打开 `.github/workflows/generate-assets.yml`，确认 `color_snake=#E68282` 写法（带井号）。

### 打字机不动 / 显示乱码

`readme-typing-svg.demolab.com` 对中文 URL 编码兼容差，**只放英文/数字**。
