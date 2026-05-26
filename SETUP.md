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

## 三、激活博客同步 Actions

仓库 → **Settings** → **Actions** → **General**：

1. **Actions permissions**：选 `Allow all actions and reusable workflows`
2. **Workflow permissions**：选 **Read and write permissions**（必须，否则 Action 无法 commit README，会报 403）
3. 保存

然后去 **Actions** 标签页：

1. 找到 `Latest blog post workflow`
2. 右上角 `Run workflow` → `Run workflow` 手动触发一次
3. 等 30 秒，刷新 README 应该能看到最近 5 篇博客

之后会每 6 小时自动跑一次，新文章发布后最迟 6 小时同步过来。

## 四、自定义

### 简介文案

`README.md` 里 `## 关于` 那一段一句话简介，直接改文字。

### 打字机文案

`README.md` 顶部的 `<picture>`，`lines=...` 是分号分隔的多句话，需要 URL 编码。**只用英文/数字**，中文很容易把 SVG 渲染服务搞炸。

- 改文案 → 用 https://www.urlencoder.org/ 编码后替换 `lines=` 参数
- 改速度 → `duration=2800`（毫秒）
- 改颜色 → 浅色 `E68282`（珊瑚红）/ 深色 `F2B94B`（琥珀黄）

### 技术栈徽章

shields.io 风格统一 `flat-square`。模板：

```
https://img.shields.io/badge/<显示文字>-<颜色>?style=flat-square&logo=<图标名>&logoColor=white
```

- 图标名查 https://simpleicons.org/
- 主组色 `475569`（深灰，对齐 Butterfly 主文字色）
- 次组色 `94A3B8`（浅灰）
- 主组放核心技术，次组放周边工具，两组之间用 `&nbsp;` 视觉隔开

### 数据卡配色

所有 `<picture>` 块都做了双主题，URL 参数：

| 参数 | 浅色 | 深色 |
|---|---|---|
| 强调色 / icon | `E68282` | `F2B94B` |
| 文字色 | `475569` | `C4C4D0` |
| 背景 | `00000000`（透明） | `00000000`（透明） |
| 标题 | `hide_title=true` | `hide_title=true` |

GitHub 会按访客系统主题自动选版本，无需额外配置。

### 同步频率

`.github/workflows/blog-post-workflow.yml` 里的 cron：

| 表达式 | 频率 |
|---|---|
| `0 */6 * * *` | 每 6 小时（默认） |
| `0 */3 * * *` | 每 3 小时 |
| `0 0 * * *` | 每天 0 点（UTC） |

## 五、常见问题

### README 不显示

仓库名必须**严格等于** `June-PJ`。建错的话去 Settings → General → Repository name 改名，或者删掉重建。

### Action 报 403 / 写不进 README

Settings → Actions → General → **Workflow permissions** 改为 `Read and write permissions`，然后重跑一次 workflow。

### Stats 数据卡破图

`github-readme-stats.vercel.app` 偶尔抽风，等几分钟刷新通常会好。如果某条卡片长期 502，把它的 `<picture>` 块临时注释掉。

### 打字机不动 / 显示乱码

`readme-typing-svg.demolab.com` 对中文 URL 编码兼容很差，**只放英文/数字**。中文留给下面的"关于"段落。

### 想加 streak / activity-graph？

不建议。它们占大版面、信息密度低、还经常破图。这一版有意去掉了。如果真的想加，把对应 `<picture>` 块加回 `## GitHub 数据` 即可。
