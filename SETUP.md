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
2. **Workflow permissions**：选 **Read and write permissions**（必须，否则 Action 无法 commit README，会报 403）
3. 保存

然后去 **Actions** 标签页：

| Workflow | 作用 | 触发 |
|---|---|---|
| `Latest blog post workflow` | 同步 atom.xml 最近 5 篇到 README（main 分支） | 每 6 小时自动 + 可手动 |
| `Generate README Assets` | 生成 stats / top-langs / 贪吃蛇 SVG 到 `output` 分支 | **仅手动**触发 |

第一个 workflow 手动跑一次（让博客列表立刻出来），之后不用管。

第二个 workflow 当前 README 里数据 / 足迹两块是注释隐藏状态（仓库 commits / repos 太少撑不起场面），所以不需要触发。等数据多起来想展示时：

1. 打开 `README.md`
2. 找到 `<!-- 暂时藏起来：...` 这段 HTML 注释
3. 把注释开始 `<!--` 和结束 `-->` 两行删掉，保留中间内容
4. 去 Actions 手动触发 `Generate README Assets`，等 1 分钟生成完
5. push 改动，刷新 README

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

| 资源 | 配色来源 |
|---|---|
| stats / top-langs（自己生成） | `.github/scripts/generate_stats.py` 里 `theme_colors()` 函数，浅色 `E68282 / 475569`，深色 `F2B94B / C4C4D0` |
| 贪吃蛇（Platane/snk） | `palette=github-light` / `palette=github-dark` 预设（绿色，跟 GitHub 贡献图自身一致） |

**为什么贪吃蛇不自定义颜色**：尝试过 `color_snake=#E68282` 和 `color_snake=%23E68282` 两种写法都没生效（snk v3 的 GitHub Actions 实际加载产物跟 README 文档脱节）。改用官方 palette 预设最稳。

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

**老问题**：早先用 `github-readme-stats.vercel.app` 直引，国内 TCP 不通；让 runner 去 curl 也是 503（免费实例被限流）。

**当前方案**：runner 用 Python 脚本 `.github/scripts/generate_stats.py` 直接调 GitHub GraphQL API 自己拼 SVG。

如果数据卡还是破图：

1. 检查 `Generate README Assets` 是不是没跑过 → Actions 页手动触发
2. 检查 `output` 分支里 `stats.svg` 是不是存在 → 不存在看 Action 日志，多半是 GraphQL 查询失败（看 step "Generate stats SVGs" 输出）
3. 改 SVG 样式 → 直接编辑 `.github/scripts/generate_stats.py` 里的 `render_stats` / `render_langs` 函数

### 贪吃蛇位置破图 / 全黑

破图：`Generate README Assets` 没跑过，`output` 分支不存在。Actions 页手动触发一次。

全黑：颜色参数没加 `#` 前缀。打开 `.github/workflows/generate-assets.yml`，确认 `color_snake=#E68282` 写法（带井号）。

### 打字机不动 / 显示乱码

`readme-typing-svg.demolab.com` 对中文 URL 编码兼容差，**只放英文/数字**。
