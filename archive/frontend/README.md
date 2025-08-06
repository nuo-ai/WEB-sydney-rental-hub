# 前端应用 - 悉尼租房中心

本项目是悉尼租房中心的前端应用，一个使用原生HTML, CSS, 和JavaScript构建的纯静态网站。

## 功能

*   房源列表展示
*   基于多种条件的筛选功能（价格、卧室数量、区域等）
*   根据大学通勤时间对房源进行排序
*   房源详情页
*   收藏夹功能

## 技术栈

*   **HTML5**
*   **CSS3** with **TailwindCSS** (via CDN)
*   **JavaScript (ES6 Modules)**
*   **FontAwesome** for icons
*   **noUiSlider** for price range slider

## 项目结构

```
sydney-rental-hub/
├── scripts/
│   ├── main.js         # 主要应用逻辑
│   ├── config.js       # 配置文件 (API地址等)
│   └── ...
├── index.html          # 主页面框架
├── listings.html       # 房源列表页面 (在iframe中加载)
└── ...
```

## 如何运行

本项目的前端服务可以通过Python的内置HTTP服务器快速启动。

```bash
# 在sydney-rental-hub目录下运行
python -m http.server 8080
```

或者，使用项目根目录的一键启动脚本，它会同时启动前端和后端服务：

```bash
# 在项目根目录运行
python start_all.py
```

启动后，在浏览器中打开 `http://localhost:8080` 即可访问。
