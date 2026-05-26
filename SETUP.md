# GitHub Profile README · 部署说明

这套文件是给你 GitHub 资料页（`https://github.com/June-PJ`）做的展示 README。

## 一、建仓库

GitHub 的"个人介绍 README"约定：**仓库名必须与你的用户名完全一致**。

你的用户名是 `June-PJ`，所以新建一个名为 `June-PJ` 的公开仓库：

1. 浏览器打开 https://github.com/new
2. **Repository name** 填 `June-PJ`（必须严格一致，区分大小写）
3. **Public** 公开
4. **不要勾选** "Add a README"（我们用本目录下的 README.md）
5. 点 Create repository

GitHub 创建后会提示"You found a secret!"或类似文案，告诉你这是 profile README 仓库。

## 二、推上去

把当前目录（`githubProfile/`）的内容搬出博客仓库 → 推到刚建的仓库。

```cmd
move d:\MyCode\JuneBlog\githubProfile d:\MyCode\June-PJ
cd /d d:\MyCode\June-PJ
git init
git branch -M main
git add .
git commit -m "feat: initial profile README"
git remote add origin https://github.com/June-PJ/June-PJ.git
git push -u origin main
```

推上去后访问 https://github.com/June-PJ ，README 会显示在头像下方。

## 三、激活博客同步 Actions

仓库 → **Settings** → **Actions** → **General**：

1. **Actions permissions**：选 `Allow all actions and reusable workflows`
2. **Workflow permissions**：选 `Read and write permissions`（让 Action 能 commit README）
3. 保存

然后去 **Actions** 标签页：

1. 找到 `Latest blog post workflow`
2. 点 `Run workflow` → `Run workflow` 手动触发一次
3. 等 30 秒左右刷新 README，应该能看到最近 5 篇博客文章

之后这个 workflow 会每 6 小时自动跑一次，博客发新文章后最迟 6 小时同步过来。

## 四、自定义

### 文案 / 简介

`README.md` 顶部 `## 🌱 关于我` 那个 yaml 风格代码块就是简介，直接改文字就行。

### 打字机标题

第一行的 `<picture>` 块，里面 `lines=...` 参数是分号分隔的多句话。需要改的话先 URL 编码（中文要 `encodeURIComponent`）：

- 想改文案 → 用 https://www.urlencoder.org/ 编码后替换 `lines=` 参数
- 想改速度 → `duration=2800`（毫秒，每个字符停留时间）
- 想改颜色 → `color=...`（深色版 `F2B94B`，浅色版 `E68282`）

### 技术栈徽章

shields.io 风格：`https://img.shields.io/badge/<显示文字>-<颜色>?style=for-the-badge&logo=<图标名>&logoColor=white`

图标名查 https://simpleicons.org/ ，颜色我已经统一为：
- 主红色 `E68282`：核心语言
- 黄色 `F2B94B`：后端框架
- 灰色 `99A9BF`：前端 / 博客
- 中性灰 `858585`：工具

### 博客同步频率

`.github/workflows/blog-post-workflow.yml` 里的 `cron: "0 */6 * * *"`：

- `0 */6 * * *` 每 6 小时
- `0 */3 * * *` 每 3 小时
- `0 0 * * *`   每天 0 点
- `*/30 * * * *` 每 30 分钟（不建议，没必要）

### 数据卡片配色

`README.md` 里所有 `<picture>` 块的 URL 参数都已对齐你 junePortal 的双主题：

- 浅色：`E68282` 珊瑚红
- 深色：`F2B94B` 琥珀黄

GitHub 会读用户的主题设置，自动展示对应版本。

## 五、常见问题

### Q: 推上去之后 README 不显示？

仓库名必须**严格等于** `June-PJ`。如果建错了名字，删掉重建，或在 Settings → General → Repository name 改名。

### Q: 博客同步 Actions 报 403 / 写不进去？

Settings → Actions → General → **Workflow permissions** 改为 `Read and write permissions`。

### Q: 打字机 / 数据卡显示破图？

这些第三方服务（demolab.com / vercel.app）偶尔抽风，等几分钟刷新通常就好。如果某个服务长期挂掉，告诉我换其他服务。

### Q: 想加更多模块？

常见可选项：
- **GitHub Trophies**：奖杯墙 https://github.com/ryo-ma/github-profile-trophy
- **WakaTime 编码统计**：每周写代码时长 https://wakatime.com/
- **Spotify 现在播放**：实时显示在听什么 https://github.com/JeffreyCA/spotify-now-playing-readme
- **贡献蛇**：吃格子动画 https://github.com/Platane/snk

需要的话告诉我加哪个，我直接给你接进来。
