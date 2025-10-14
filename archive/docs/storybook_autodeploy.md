**透過 Github Action 來幫助我們自動化部署 Storybook、產生 Bundle Size Report、產生 Changelog 等等，今天先來介紹如何使用 Github Action 來部署 Storybook。.**

## Storybook Deployment.

**首先 Storybook 在 build 完之後會產生一個靜態的資料夾 /storybook-static，接著就可以部署到任何靜態網站上，例如 Github Page、Netlify、Vercel 等等，這邊會用 Github Page 與 Vercel 來做為範例。.**

<pre><pre><p><span class="tts-text" data-sentence-index="6" title="Click to read this sentence">design-system.</span></p><p><span class="tts-text" data-sentence-index="7" title="Click to read this sentence">├── storybook-static.</span></p><p><span class="tts-text" data-sentence-index="8" title="Click to read this sentence">...</span></p></pre></pre>

### 部署到 Github Page.

**Github Page 是由 Github 提供的靜態網站服務，只要有 Github 帳號就可以免費使用，而且部署非常簡單，只要多新增 gh-pages 的分支，並且把 storybook-static 資料夾推上去就可以了，本章會用 gh-pages 這個套件幫忙處理上述的步驟！.**

#### 基本設置.

**首先在 design-system 的根目錄安裝 gh-pages：.**

<pre><pre><p><span class="tts-text" data-sentence-index="13" title="Click to read this sentence">design-system > pnpm add -Dw gh-pages.</span></p></pre></pre>

**接著加入兩個指令在 package.json 與新增 homepage:.**

* `build-storybook`：用來 build storybook，並且輸出.`storybook-static`資料夾.
* `deploy-storybook`: 用來部署.`storybook-static`資料夾.

<pre><pre><p><span class="tts-text" data-sentence-index="19" title="Click to read this sentence">{.</span></p><p><span class="tts-text" data-sentence-index="20" title="Click to read this sentence">"scripts": {.</span></p><p><span class="tts-text" data-sentence-index="21" title="Click to read this sentence">...</span></p><p><span class="tts-text" data-sentence-index="22" title="Click to read this sentence">"build:storybook": "storybook build",.</span></p><p><span class="tts-text" data-sentence-index="23" title="Click to read this sentence">"deploy-storybook": "gh-pages -d storybook-static",.</span></p><p><span class="tts-text" data-sentence-index="24" title="Click to read this sentence">...</span></p><p><span class="tts-text" data-sentence-index="25" title="Click to read this sentence">},.</span></p><p><span class="tts-text" data-sentence-index="26" title="Click to read this sentence">"homepage": "https://<username>.github.io/<repository-name>/".</span></p><p><span class="tts-text" data-sentence-index="27" title="Click to read this sentence">}.</span></p></pre></pre>

**這樣將上述改動推上 Github 並 merge 到 main 分支，就會看到 "pages build and deployment" 的 Github Action 開始執行，並且在 Github Page 上看到 Storybook 的畫面了！.**

#### Vercel 部署.

**如果今天想要部署到其他域名底下而非 Github Page，可以透過 Vercel 來協助部署！.**

**1. 登入 Vercel 後，我們可以點擊 "Add New".**

**2. 選擇你要 Import 的 Repo.**

**3. 設置 Config.**

**這邊要注意的地方是要將 Build Command 設置為 turbo run build & storybook build，這樣才能夠正確的 build Storybook，並且輸出 storybook-static 資料夾。.**

**4. 新增新的域名.**

**如果你有自己的域名，可以在這邊新增，如果沒有的話，可以直接使用 Vercel 提供的域名。.**

**這樣就可以到 Vercel 上看到 Storybook 的畫面了！.**
