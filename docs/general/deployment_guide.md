# 部署 (Deployment)

Taro小程序 (`sydney-rental-taro`) 已配置为可轻松部署到 [Netlify](https://www.netlify.com/)。

## 部署步骤

1.  **登录 Netlify**: 使用你的 GitHub 账户登录 Netlify。
2.  **导入项目**:
    - 在 Netlify Dashboard 中，点击 "Add new site -> Import an existing project"。
    - 选择 "Deploy with GitHub" 并授权访问此项目的 GitHub 仓库。
3.  **配置项目**:
    - Netlify 会自动检测到 `sydney-rental-taro` 目录。如果未自动检测，请将 **Base directory** 设置为 `sydney-rental-taro`。
    - Netlify 将使用 `sydney-rental-taro/netlify.toml` 中的配置来构建和部署应用。构建命令 (`npm run build:h5`) 和发布目录 (`dist`) 已预先配置好。
4.  **添加环境变量**:
    - 在项目的 "Site settings -> Build & deploy -> Environment" 中，添加后端 API 的地址。例如:
      - `VITE_API_BASE_URL` = `https://your-backend-api.com` (Taro/Vite项目通常使用 `VITE_` 前缀)
5.  **部署**: 点击 "Deploy site" 按钮。Netlify 将会自动安装依赖、构建项目并将其部署到全球CDN。
