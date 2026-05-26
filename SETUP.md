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

## 四、自定义

### 简介文案

`README.md` 里 `## 关于` 那一段一句话简介，直接改文字。

### 顶部 Banner（capsule-render）

`README.md` 顶部的 capsule-render `<picture>`，可调参数：

- `type=waving`：波浪。可换 `slice` `rect` `transparent` `shark`
- `color=E68282` / `F2B94B`：背景色（浅 / 深）
- `text=...` `desc=...`：标题 + 副标题（中文要 URL 编码）
- `height=140`：高度

### 打字机文案

`<picture>` 下面那个 `lines=...` 是分号分隔的多句话。**只用英文/数字**，中文很容易把 SVG 渲染服务搞炸。

- 改文案 → 用 https://www.urlencoder.org/ 编码后替换 `lines=` 参数
- 改速度 → `duration=2800`（毫秒）

### 技术栈徽章

shields.io 风格统一 `flat-square`，模板：

```
https://img.shields.io/badge/<显示文字>-<颜色>?style=flat-square&logo=<图标名>&logoColor=white
```

- 图标名查 https://simpleicons.org/
- 主组色 `475569`（深灰，对齐 Butterfly 主文字）
- 次组色 `94A3B8`（浅灰）
- 两组之间用 `&nbsp;&nbsp;&nbsp;&nbsp;` 隔开

### 数据卡 / 连续打卡 / 活动图配色

所有 `<picture>` 块都做了双主题，统一参数：

| 参数 | 浅色 | 深色 |
|---|---|---|
| 强调色 / icon | `E68282` | `F2B94B` |
| 文字色 | `475569` | `C4C4D0` |
| 背景 | `00000000`（透明） | `00000000`（透明） |
| 标题 | `hide_title=true` | `hide_title=true` |

GitHub 按访客系统主题自动选版本。

### 博客同步频率

`.github/workflows/blog-post-workflow.yml` 里的 cron：

| 表达式 | 频率 |
|---|---|
| `0 */6 * * *` | 每 6 小时（默认） |
| `0 */3 * * *` | 每 3 小时 |
| `0 0 * * *` | 每天 0 点（UTC） |

**坑提醒**：`date_format` 用的是 [dateformat](https://www.npmjs.com/package/dateformat) 包语法，月份是**小写 `mm`**，大写 `MM` 是分钟。所以 `yyyy-mm-dd` 才对。

### 贪吃蛇配色

`.github/workflows/snake.yml` 里 `color_snake` 是蛇身颜色，`color_dots` 是 0~4 级贡献格子（从空到最满）。当前配色：

- 浅色：蛇 `E68282`，格子从浅到深 `E5E7EB → F8C5C5 → EFA5A5 → E68282 → D86060`
- 深色：蛇 `F2B94B`，格子从浅到深 `2E2E36 → 5E4F2A → 8A7330 → B89640 → F2B94B`

## 五、常见问题

### README 不显示

仓库名必须**严格等于** `June-PJ`。建错的话去 Settings → General → Repository name 改名，或者删掉重建。

### Action 报 403 / 写不进 README / 没 output 分支

Settings → Actions → General → **Workflow permissions** 改为 `Read and write permissions`，重跑 workflow。

### 贪吃蛇位置破图

`Generate Snake` 还没跑过，`output` 分支不存在。Actions 页手动触发一次，等 30 秒刷新。

### 博客日期变成 `2026-00-08`

date_format 写错了——`MM` 是分钟，月份要用小写 `mm`。已经在 workflow 里修好。

### Stats / Streak / Activity Graph 任意一个破图

`*.vercel.app` 偶尔抽风（被 GitHub IP 限流），等几分钟刷新通常会好。如果某条卡片长期 502，把它的 `<picture>` 块临时注释掉。

### 打字机不动 / 显示乱码

`readme-typing-svg.demolab.com` 对中文 URL 编码兼容差，**只放英文/数字**。
