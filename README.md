# 🤖 AI 每日日报

自动聚合全球 AI 资讯，每天更新，打开即看。

## 功能

- 📰 **最新动态** - 聚合机器之心、量子位、MIT Tech Review 等 AI 新闻
- 📄 **热门论文** - Arxiv 最新 AI/ML 论文
- 💬 **社区热议** - Hacker News 热门 AI 讨论
- ⭐ **今日焦点** - 自动精选 Top 3 头条
- 🌙 **深色模式** - 护眼暗色主题

## 部署步骤

### 1. 创建 GitHub 仓库

1. 打开 [github.com/new](https://github.com/new)
2. 仓库名填写：i-daily-news
3. 选择 **Public**（公开，免费）
4. 点击 **Create repository**

### 2. 上传代码

`ash
git clone https://github.com/你的用户名/ai-daily-news.git
cd ai-daily-news
# 把本项目所有文件复制到该目录
git add .
git commit -m "first commit"
git push
`

### 3. 开启 GitHub Pages

1. 打开仓库页面，点击 **Settings**
2. 左侧找到 **Pages**
3. Source 选择 **Deploy from a branch**
4. Branch 选择 **main**，目录选 **/(root)**
5. 点击 **Save**
6. 等待 1-2 分钟，你的网址就是：https://你的用户名.github.io/ai-daily-news/

### 4. 开启 Actions

1. 打开仓库的 **Actions** 页面
2. 点击 **I understand my workflows, go ahead and enable them**

### 5. 手动运行一次

1. 打开仓库的 **Actions** 页面
2. 左侧点击 **AI Daily News Update**
3. 右侧点击 **Run workflow** → **Run workflow**
4. 等运行完成后，打开网页就能看到日报了

## 技术栈

- Python 定时抓取 RSS
- GitHub Actions 自动运行
- GitHub Pages 免费托管
- 纯前端 HTML + CSS + JavaScript
