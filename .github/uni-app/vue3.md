![横幅](https://p9-piu.byteimg.com/tos-cn-i-8jisjyls3a/8c759ddb57d0440986f4768fc644f879~tplv-8jisjyls3a-2:0:0:q75.image)![](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/img/close.7ba0700.png)

[![稀土掘金](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/e08da34488b114bd4c665ba2fa520a31.svg)]()*  * [首页](https://juejin.cn/)

* [AI CodingNEW](https://aicoding.juejin.cn/)
* [沸点](https://juejin.cn/pins)
* [课程](https://juejin.cn/course)
* [直播](https://juejin.cn/live)
* [活动](https://juejin.cn/events/all)
* [AI刷题](https://juejin.cn/problemset)
  [APP](https://juejin.cn/app?utm_source=jj_nav)
* * [ ]

  * 创作者中心
* ![vip](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ffd3e238ee7f46eab42bf88af17f5528~tplv-k3u1fbpfcp-image.image#?w=25&h=26&s=5968&e=svg&a=1&b=dacbbc)

  会员
* [3](https://juejin.cn/notification)
* ![用户36381400650的头像](https://p6-passport.byteacctimg.com/img/mosaic-legacy/3795/3044413937~60x60.awebp)

# 使用VSCode搭建UniApp + TS + Vue3 + Vite项目

[](https://juejin.cn/user/2487565513132180/posts)

2024-09-11**1,123**阅读6分钟

![](https://p3-piu.byteimg.com/tos-cn-i-8jisjyls3a/b37ce6cd3dfa46f699d8fc9c7c888f2f~tplv-8jisjyls3a-3:0:0:q75.png)`uniapp`是一个使用Vue.js开发所有前端应用的框架，开发者编写一套代码，可发布到iOS、Android、以及各种小程序。深受广大前端开发者的喜爱。`uniapp`官方也提供了自己的IDE工具 `HBuilderX`，可以快速开发 `uniapp`项目。但是很多前端的同学已经比较习惯使用 `VSCode`去开发项目，为了开发 `uniapp`项目再去切换开发工具，而且对新的开发工具也要有一定的适应过程，大多数前端的同学肯定是不愿意的。下面我们就看看用 `VSCode`如何搭建 `uniapp`项目。

### 安装node和pnpm

`node`的安装我就不多说了，去官网下载，直接安装就可以了。node安装好以后，我们再来安装 `pnpm`。咦？`node`安装完不是自带 `npm`吗？这个 `pnpm`又是啥？这里简单介绍一下 `npm`和 `pnpm`的区别，不做重点。使用 `npm` 时，依赖每次被不同的项目使用，都会重复安装一次。 而在使用 `pnpm`时，依赖会被存储在一个公共的区域，不同的项目在引入相同的依赖时，会从公共区域去引入，节省了空间。

`pnpm`我们直接全局安装就可以了，执行以下的命令：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-node code-block-extension-codeShowNum" lang="node"><span class="code-block-extension-codeLine" data-line-num="1">npm install -g pnpm</span>
</code></pre>

安装好以后，我们在命令行执行 `pnpm -v`，能够看到版本号就说明安装成功了。

### 创建uniapp项目

由于我们要使用 `VSCode`去开发项目，而且项目要使用 `Vue3`和 `TypeScript`，所以我们要使用命令行去创建 `uniapp`项目。先进入我们存放 `VSCode`的项目目录，我的项目目录是 `D:\VSProjects`，进入后，执行命令如下：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-node code-block-extension-codeShowNum" lang="node"><span class="code-block-extension-codeLine" data-line-num="1">npx degit dcloudio/uni-preset-vue#vite-ts 项目名称</span>
</code></pre>

`项目名称`写你自己真实的项目名称就可以了，我的项目叫做 `my-vue3-uniapp`。这个命令会把官方提供的使用了 `TypeScript`和 `Vite`的 `uniapp`项目模板下载下来，然后我们就可以去开发 `uniapp`项目了。

我们使用 `VSCode`打开项目，项目的目录如下：

![image-20240910201316280.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/659db275e5c64d02a5b5951cbdbdef31~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=1WXPufQcOAcJGJ6wX4h728mw1L8%3D) 我们可以看到 `src`目录里的文件都是 `uniapp`项目的文件，包括页面、样式、静态文件等，`src`目录外是整个项目的文件，如：`vite.config.ts`和 `tsconfig.json`等。然后我们打开终端，使用 `pnpm`命令安装一下依赖，执行命令如下：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-node code-block-extension-codeShowNum" lang="node"><span class="code-block-extension-codeLine" data-line-num="1">pnpm i</span>
</code></pre>

执行完成后，我们熟悉的 `node_modules`目录出现在了项目中，如图：

![image-20240910201915353.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/537ee0c7c9b14aac9471325e9cee6fec~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=JkY5CjAy0WHoJHMCmN%2B7nU0IjGg%3D)

然后我们运行项目，执行命令如下：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-node code-block-extension-codeShowNum" lang="node"><span class="code-block-extension-codeLine" data-line-num="1">pnpm run dev:mp-weixin</span>
</code></pre>

上面的命令会把我们的代码编译成微信小程序代码，如图：

![image-20240910202443268.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f97eb14e44c74d43b050bd57e3134bd4~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=rvxn5azh4u4ghtdwwRytYsKhPuE%3D)

编译完成后，我们的项目中出现了 `dist`目录，这个目录就是编译后的输出目录。然后我们打开微信小程序开发工具，目录选择 `/dist/dev/mp-weixin`，如图：

![image-20240910202838634.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3f66eabf10ac4b789026d49c75324881~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=HG9YsEW3kQcpx2GxfWC2fTHrq6c%3D)

AppID写我们自己的小程序的AppID，点击确定，

![image-20240910203040972.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/89cda7064c8f4062accbe10f4fe31688~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=CrDRAucPAEomx1xgH2DKtrAK%2BLw%3D)

看到这个画面，说明我们的 `uniapp`项目搭建成功了，而且可以通过微信小程序开发工具去预览。我们可以通过 `VSCode`在页面上添加些文字，看看微信小程序开发工具的画面是否有改变。这里就不给大家演示了。

### 添加uni-ui扩展组件

在我们开发项目时，会用到各种组件，仅仅使用uniapp的内置组件是远远不够的，我们还需安装官方提供的扩展组件uni-ui，怎么安装呢？我们同样使用 `pnpm`命令去安装，在具体安装uni-ui扩展组件之前，我们先需要安装 `sass`和 `sass-loader`，

安装sass

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-node code-block-extension-codeShowNum" lang="node"><span class="code-block-extension-codeLine" data-line-num="1"> pnpm i sass -D</span>
</code></pre>

安装sass-loader

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-node code-block-extension-codeShowNum" lang="node"><span class="code-block-extension-codeLine" data-line-num="1">pnpm i sass-loader@v8.x</span>
</code></pre>

由于现在的node版本都是大于16的，所以，我们根据uniapp官方的建议，安装 `v8.x`的版本。

最后我们安装uni-ui，如下：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-node code-block-extension-codeShowNum" lang="node"><span class="code-block-extension-codeLine" data-line-num="1">pnpm i @dcloudio/uni-ui</span>
</code></pre>

uni-ui安装完成后，我们再配置 `easycom`，`easycom`的好处是，可以自动引入uni-ui组件，无需我们手动 `import`，这对于我们开发项目来说非常的方便，我们打开 `src`目录下的 `pages.json` 并添加 `easycom` 节点：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-node code-block-extension-codeShowNum" lang="node"><span class="code-block-extension-codeLine" data-line-num="1">// pages.json</span>
<span class="code-block-extension-codeLine" data-line-num="2">{</span>
<span class="code-block-extension-codeLine" data-line-num="3">    "easycom": {</span>
<span class="code-block-extension-codeLine" data-line-num="4">        "autoscan": true,</span>
<span class="code-block-extension-codeLine" data-line-num="5">        "custom": {</span>
<span class="code-block-extension-codeLine" data-line-num="6">            // uni-ui 规则如下配置</span>
<span class="code-block-extension-codeLine" data-line-num="7">            "^uni-(.*)": "@dcloudio/uni-ui/lib/uni-$1/uni-$1.vue"</span>
<span class="code-block-extension-codeLine" data-line-num="8">        }</span>
<span class="code-block-extension-codeLine" data-line-num="9">    },</span>
<span class="code-block-extension-codeLine" data-line-num="10"></span>
<span class="code-block-extension-codeLine" data-line-num="11">    // 其他内容</span>
<span class="code-block-extension-codeLine" data-line-num="12">    pages:[</span>
<span class="code-block-extension-codeLine" data-line-num="13">        // ...</span>
<span class="code-block-extension-codeLine" data-line-num="14">    ]</span>
<span class="code-block-extension-codeLine" data-line-num="15">}</span>
</code></pre>

这样uni-ui扩展组件就添加到我们的项目中了。

### Json文件的注释

我们在添加 `easycom`的时候，发现 `pages.json`文件中的注释是有错误提示的，我们想让Json文件中可以有注释，至少 `pages.json`和 `manifest.json`两个文件这种可以有注释，这个我们需要在 `VSCode`中配置一下，打开 `文件->首选项->设置`，如图：

![image-20240910205931299.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4cb6fd8a638f4fd299623d4cf4402264~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=AMjV2tWWTmqa6X4eBIqh8yZgzlI%3D)

然后我们在 `文本编辑器`中找到 `文件`，再在 `Associations`中添加项，如下：

![image-20240910210055338.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/366c5c0cb9b244838524bbd680e8b0a3~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=FbxQcBsfLVYOm%2FSYcbLnOeXlCUk%3D)

然后我们回到 `pages.json`和 `manifest.json`这两个文件看一下，注释就不报错了。

### VSCode插件安装

到现在为止，我们的uniapp项目已经搭建起来了，而且已经可以正常运行了，两个比较重要的json文件中，注释文字也不报错了。但这离我们正常开发还差很多，我们在使用uniapp组件的时候，没有提示，这使得我们编写程序很不方便，我们可以安装几个uniapp插件解决这些问题。我们在 `VSCode`的扩展商店中搜索一下uniapp，这里需要安装3个插件：

* uniapp小程序扩展
* uni-create-view
* uni-helper

安装完之后，我们在编写页面时，会有提示：

![image-20240910211248220.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3df1ba1e2e2f477b851a31b5a895e811~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=JzKtcQXQpOweve1%2BsOfYBMm870w%3D)

在新建页面时，会有uniapp相关的选项：

![image-20240910211328112.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/ffd74c8b400b42269f3b3a2d09fda9ef~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=J%2Bjs4aEYY5Hs%2BjE3NQHtQ2TmtGw%3D)

这些对于我们实际开发是非常由帮助的。

### 安装uniapp的types

我们可以看到vue文件中，uniapp的组件并没有变绿，说明ts是没有生效的，我们先把uniapp的类型文件安装一下，如下：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-node code-block-extension-codeShowNum" lang="node"><span class="code-block-extension-codeLine" data-line-num="1">pnpm i -D @uni-helper/uni-app-types @uni-helper/uni-ui-types</span>
</code></pre>

我们在使用pnpm安装时，会报错，我们根据uni-helper的官方文档中的提示，将 `shamefully-hoist` 为 `true`。这个需要我们找到家目录下的 `.npmrc`文件，如图：

![image-20240910213137695.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f1c1b3ee3e9b45308a90bb491aabbe0b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=1StB%2BQ4TzHxYEInJSj5AoXMieQs%3D)

然后在文件中增加：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-properties code-block-extension-codeShowNum" lang="properties"><span class="code-block-extension-codeLine" data-line-num="1">registry=http://registry.npm.taobao.org</span>
<span class="code-block-extension-codeLine" data-line-num="2">shamefully-hoist=true</span>
</code></pre>

然后，我们再执行pnpm命令安装类型文件。安装完成后，在项目根目录下，打开 `tsconfig.json`文件，在 `types`中增加我们安装的类型：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-json code-block-extension-codeShowNum" lang="json"><span class="code-block-extension-codeLine" data-line-num="1">{</span>
<span class="code-block-extension-codeLine" data-line-num="2">  "extends": "@vue/tsconfig/tsconfig.json",</span>
<span class="code-block-extension-codeLine" data-line-num="3">  "compilerOptions": {</span>
<span class="code-block-extension-codeLine" data-line-num="4">    ……</span>
<span class="code-block-extension-codeLine" data-line-num="5">    "types": [</span>
<span class="code-block-extension-codeLine" data-line-num="6">      "@dcloudio/types",</span>
<span class="code-block-extension-codeLine" data-line-num="7">      "@uni-helper/uni-app-types",</span>
<span class="code-block-extension-codeLine" data-line-num="8">      "@uni-helper/uni-ui-types"</span>
<span class="code-block-extension-codeLine" data-line-num="9">    ]</span>
<span class="code-block-extension-codeLine" data-line-num="10">  }</span>
<span class="code-block-extension-codeLine" data-line-num="11">    ……</span>
<span class="code-block-extension-codeLine" data-line-num="12">}</span>
</code></pre>

添加完成后，我们发现 `compilerOptions`是有报错的，鼠标悬停上去发现：

![image-20240910213738482.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/da33ce27a4814e738fc8269707e7c230~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=94UYEK%2BXyvHGyVabfh%2Fv%2F0XWq%2Fs%3D)

报错提示两个选项将要废弃，我们要把这个错误提示去掉，可以在文件中增加 `"ignoreDeprecations": "5.0",`：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-json code-block-extension-codeShowNum" lang="json"><span class="code-block-extension-codeLine" data-line-num="1">{</span>
<span class="code-block-extension-codeLine" data-line-num="2">  "extends": "@vue/tsconfig/tsconfig.json",</span>
<span class="code-block-extension-codeLine" data-line-num="3">  "compilerOptions": {</span>
<span class="code-block-extension-codeLine" data-line-num="4">    "ignoreDeprecations": "5.0",</span>
<span class="code-block-extension-codeLine" data-line-num="5">   ……</span>
<span class="code-block-extension-codeLine" data-line-num="6">  },</span>
<span class="code-block-extension-codeLine" data-line-num="7">  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"]</span>
<span class="code-block-extension-codeLine" data-line-num="8">}</span>
</code></pre>

这样 `compilerOptions`就不报错了。然后我们打开vue文件，发现uniapp的标签都变绿了，但是会有报错，这个 `VSCode`的插件之间有冲突造成的，我们可以配置如下解决，参考官方文档：

![image-20240910215439960.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/26536a102c5a4fd49693cba778fef920~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=jc3wi2fXucb7GhJqokvGkcW6sFg%3D)

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-json code-block-extension-codeShowNum" lang="json"><span class="code-block-extension-codeLine" data-line-num="1">{</span>
<span class="code-block-extension-codeLine" data-line-num="2">  ……</span>
<span class="code-block-extension-codeLine" data-line-num="3">  "vueCompilerOptions": {</span>
<span class="code-block-extension-codeLine" data-line-num="4">    "plugins": ["@uni-helper/uni-app-types/volar-plugin"]</span>
<span class="code-block-extension-codeLine" data-line-num="5">  },</span>
<span class="code-block-extension-codeLine" data-line-num="6">  ……</span>
<span class="code-block-extension-codeLine" data-line-num="7">}</span>
</code></pre>

然后重启 `VSCode`。最后我们发现vue文件的uniapp标签变绿了，而且没有报错：

![image-20240910215154651.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/d5dfc6f546fa46f8914de1697234a933~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg54mb5Yid5Lmd:q75.awebp?rk3s=f64ab15b&x-expires=1760432715&x-signature=LkdqgUx72kXZwWChzmf6cw3mGPM%3D)

最后 `tsconfig.json`的整体内容如下：

<pre><div class="code-block-extension-header"><div class="code-block-extension-headerRight"><div data-v-4fdcfe21="" class="code-tips"><svg data-v-4fdcfe21="" xmlns="http://www.w3.org/2000/svg" width="19" height="14" viewBox="0 0 19 14" fill="none" class=""><defs data-v-4fdcfe21=""><linearGradient data-v-4fdcfe21="" id="paint0_linear_43_148" x1="11" y1="0.999756" x2="2" y2="6.49976" gradientUnits="userSpaceOnUse"></linearGradient></defs></svg></div><div data-v-159ebe90="" class="render"><svg data-v-159ebe90="" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 14 14" fill="none" class="icon"><defs data-v-159ebe90=""><radialGradient data-v-159ebe90="" id="paint0_radial_370_13481" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(12.8336 1.1665) rotate(134.17) scale(17.0784 23.5605)"></radialGradient></defs></svg></div></div></div><code class="hljs language-json code-block-extension-codeShowNum" lang="json"><span class="code-block-extension-codeLine" data-line-num="1">{</span>
<span class="code-block-extension-codeLine" data-line-num="2">  "extends": "@vue/tsconfig/tsconfig.json",</span>
<span class="code-block-extension-codeLine" data-line-num="3">  "compilerOptions": {</span>
<span class="code-block-extension-codeLine" data-line-num="4">    "ignoreDeprecations": "5.0",</span>
<span class="code-block-extension-codeLine" data-line-num="5">    "sourceMap": true,</span>
<span class="code-block-extension-codeLine" data-line-num="6">    "baseUrl": ".",</span>
<span class="code-block-extension-codeLine" data-line-num="7">    "paths": {</span>
<span class="code-block-extension-codeLine" data-line-num="8">      "@/*": ["./src/*"]</span>
<span class="code-block-extension-codeLine" data-line-num="9">    },</span>
<span class="code-block-extension-codeLine" data-line-num="10">    "lib": ["esnext", "dom"],</span>
<span class="code-block-extension-codeLine" data-line-num="11">    "types": [</span>
<span class="code-block-extension-codeLine" data-line-num="12">      "@dcloudio/types",</span>
<span class="code-block-extension-codeLine" data-line-num="13">      "@uni-helper/uni-app-types",</span>
<span class="code-block-extension-codeLine" data-line-num="14">      "@uni-helper/uni-ui-types"</span>
<span class="code-block-extension-codeLine" data-line-num="15">    ]</span>
<span class="code-block-extension-codeLine" data-line-num="16">  },</span>
<span class="code-block-extension-codeLine" data-line-num="17">  "vueCompilerOptions": {</span>
<span class="code-block-extension-codeLine" data-line-num="18">    "plugins": ["@uni-helper/uni-app-types/volar-plugin"]</span>
<span class="code-block-extension-codeLine" data-line-num="19">  },</span>
<span class="code-block-extension-codeLine" data-line-num="20">  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"]</span>
<span class="code-block-extension-codeLine" data-line-num="21">}</span>
</code></pre>

### 最后

到这里，我们的uniapp项目就搭建完成了，而且是使用我们非常熟悉的 `VSCode`，项目中还是用了 `Vue3`，`Typescript`，`Vite`，该装的插件也已经装上了，鼠标悬停会给我们组件的提示，大大提高了我们的开发效率。OK了，去开发我们的项目应用吧~~~

标签：

话题：

评论 0

![avatar](https://p6-passport.byteacctimg.com/img/mosaic-legacy/3795/3044413937~80x80.awebp)

**0** **/ 1000**

发送

[](https://juejin.cn/user/2487565513132180/posts)[](https://juejin.cn/user/2487565513132180/posts)[](https://juejin.cn/user/2487565513132180/posts)[](https://juejin.cn/user/2487565513132180/followers)

关注

已关注

[私信](https://juejin.cn/notification/im?participantId=2487565513132180)

目录

收起

* [安装node和pnpm](https://juejin.cn/post/7412813777559470091#heading-0 "安装node和pnpm")
* [创建uniapp项目](https://juejin.cn/post/7412813777559470091#heading-1 "创建uniapp项目")
* [添加uni-ui扩展组件](https://juejin.cn/post/7412813777559470091#heading-2 "添加uni-ui扩展组件")
* [Json文件的注释](https://juejin.cn/post/7412813777559470091#heading-3 "Json文件的注释")
* [VSCode插件安装](https://juejin.cn/post/7412813777559470091#heading-4 "VSCode插件安装")
* [安装uniapp的types](https://juejin.cn/post/7412813777559470091#heading-5 "安装uniapp的types")
* [最后](https://juejin.cn/post/7412813777559470091#heading-6 "最后")

搜索建议

[ ]

精选内容

[](https://juejin.cn/post/7558320134252576802 "深入解析 Vue 3 源码：computed 的底层实现原理")[](https://juejin.cn/post/7558320134252494882 "前端梳理体系从常问问题去完善-框架篇（react生态)")[](https://juejin.cn/post/7558458025963929609 "WebSocket 连接：实现实时双向通信的前端技术")[](https://juejin.cn/post/7558339664354492425 "超长定时器 long-timeout")[](https://juejin.cn/post/7558320134252052514 "架构进阶 🏗 从 CRUD 升级到“大工程师视野”")

找对属于你的技术圈子

回复「进群」加入官方微信群

![](https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/img/qr-code.4e391ff.png)

**为你推荐**

* * [](https://juejin.cn/user/3661793144604455)
* 1年前
* 1.1k
* 点赞
* 评论
* 
* * [](https://juejin.cn/user/2771188199468606)
* 11月前
* 325
* 点赞
* 评论
* 
* * [](https://juejin.cn/user/1011206429612750)
* 4年前
* 6.7k
* 3
* 评论
* 
* * [](https://juejin.cn/user/2731607218202520)
* 10月前
* 964
* 2
* 评论
* 
* * [](https://juejin.cn/user/4099442643832413)
* 3年前
* 6.4k
* 138
* 15
* 
* * [](https://juejin.cn/user/184373686834391)
* 2年前
* 1.5k
* 9
* 评论
* 
* * [](https://juejin.cn/user/1926000100522360)
* 2年前
* 2.3k
* 24
* 5
* 
* * [](https://juejin.cn/user/3562073405009789)
* 2年前
* 2.9k
* 31
* 8
* 
* * [](https://juejin.cn/user/712139266594743)
* 4年前
* 1.2k
* 13
* 评论
* 
* * [](https://juejin.cn/user/4441682708283191)
* 5年前
* 2.3k
* 16
* 评论
* 
* * [](https://juejin.cn/user/2973496271181086)
* 3年前
* 971
* 2
* 评论
* 
* * [](https://juejin.cn/user/1169536104021335)
* 4年前
* 9.9k
* 89
* 8
* 
* * [](https://juejin.cn/user/140339735966695)
* 11月前
* 5.6k
* 58
* 8
* 
* * [](https://juejin.cn/user/1882842693125517)
* 3年前
* 1.8k
* 点赞
* 1
* 
* * [](https://juejin.cn/user/78820568482141)
* 4年前
* 886
* 1
* 2
* 

# 使用VSCode搭建UniApp + TS + Vue3 + Vite项目

juejin.cn2 min read

![Article main image](https://p3-piu.byteimg.com/tos-cn-i-8jisjyls3a/b37ce6cd3dfa46f699d8fc9c7c888f2f~tplv-8jisjyls3a-3:0:0:q75.png)**uniapp是一个使用Vue.js开发所有前端应用的框架，开发者编写一套代码，可发布到iOS、Android、以及各种小程序。深受广大前端开发者的喜爱。uniapp官方也提供了自己的IDE工具HBuilderX，可以快速开发uniapp项目。但是很多前端的同学已经比较习惯使用VSCode去开发项目，为了开发uniapp项目再去切换开发工具，而且对新的开发工具也要有一定的适应过程，大多数前端的同学肯定是不愿意的。下面我们就看看用VSCode如何搭建uniapp项目。.**

### 安装node和pnpm.

**node的安装我就不多说了，去官网下载，直接安装就可以了。node安装好以后，我们再来安装pnpm。咦？node安装完不是自带npm吗？这个pnpm又是啥？这里简单介绍一下npm和pnpm的区别，不做重点。使用 npm 时，依赖每次被不同的项目使用，都会重复安装一次。 而在使用pnpm时，依赖会被存储在一个公共的区域，不同的项目在引入相同的依赖时，会从公共区域去引入，节省了空间。.**

**pnpm我们直接全局安装就可以了，执行以下的命令：.**

```
npm install -g pnpm.
```

**安装好以后，我们在命令行执行pnpm -v，能够看到版本号就说明安装成功了。.**

### 创建uniapp项目.

**由于我们要使用VSCode去开发项目，而且项目要使用Vue3和TypeScript，所以我们要使用命令行去创建uniapp项目。先进入我们存放VSCode的项目目录，我的项目目录是D:\VSProjects，进入后，执行命令如下：.**

```
npx degit dcloudio/uni-preset-vue#vite-ts 项目名称.
```

**项目名称写你自己真实的项目名称就可以了，我的项目叫做my-vue3-uniapp。这个命令会把官方提供的使用了TypeScript和Vite的uniapp项目模板下载下来，然后我们就可以去开发uniapp项目了。.**

**我们使用VSCode打开项目，项目的目录如下：.**

**我们可以看到src目录里的文件都是uniapp项目的文件，包括页面、样式、静态文件等，src目录外是整个项目的文件，如：vite.config.ts和tsconfig.json等。然后我们打开终端，使用pnpm命令安装一下依赖，执行命令如下：.**

```
pnpm i.
```

**执行完成后，我们熟悉的node_modules目录出现在了项目中，如图：.**

**然后我们运行项目，执行命令如下：.**

```
pnpm run dev:mp-weixin.
```

**上面的命令会把我们的代码编译成微信小程序代码，如图：.**

**编译完成后，我们的项目中出现了dist目录，这个目录就是编译后的输出目录。然后我们打开微信小程序开发工具，目录选择/dist/dev/mp-weixin，如图：.**

**AppID写我们自己的小程序的AppID，点击确定，.**

**看到这个画面，说明我们的uniapp项目搭建成功了，而且可以通过微信小程序开发工具去预览。我们可以通过VSCode在页面上添加些文字，看看微信小程序开发工具的画面是否有改变。这里就不给大家演示了。.**

### 添加uni-ui扩展组件.

**在我们开发项目时，会用到各种组件，仅仅使用uniapp的内置组件是远远不够的，我们还需安装官方提供的扩展组件uni-ui，怎么安装呢？我们同样使用pnpm命令去安装，在具体安装uni-ui扩展组件之前，我们先需要安装sass和sass-loader，.**

**安装sass.**

```
pnpm i sass -D.
```

**安装sass-loader.**

```
pnpm i sass-loader@v8.x.
```

**由于现在的node版本都是大于16的，所以，我们根据uniapp官方的建议，安装v8.x的版本。.**

**最后我们安装uni-ui，如下：.**

```
pnpm i @dcloudio/uni-ui.
```

**uni-ui安装完成后，我们再配置easycom，easycom的好处是，可以自动引入uni-ui组件，无需我们手动import，这对于我们开发项目来说非常的方便，我们打开src目录下的 pages.json 并添加 easycom 节点：.**

```
// pages.json.
{
"easycom": {.
"autoscan": true,.
"custom": {.
// uni-ui 规则如下配置.
"^uni-(.*)": "@dcloudio/uni-ui/lib/uni-$1/uni-$1.vue".
        }
},.

// 其他内容.
pages:[.
// ...
    ]
}
```

**这样uni-ui扩展组件就添加到我们的项目中了。.**

### Json文件的注释.

**我们在添加easycom的时候，发现pages.json文件中的注释是有错误提示的，我们想让Json文件中可以有注释，至少pages.json和manifest.json两个文件这种可以有注释，这个我们需要在VSCode中配置一下，打开文件->首选项->设置，如图：.**

**然后我们在文本编辑器中找到文件，再在Associations中添加项，如下：.**

**然后我们回到pages.json和manifest.json这两个文件看一下，注释就不报错了。.**

### VSCode插件安装.

**到现在为止，我们的uniapp项目已经搭建起来了，而且已经可以正常运行了，两个比较重要的json文件中，注释文字也不报错了。但这离我们正常开发还差很多，我们在使用uniapp组件的时候，没有提示，这使得我们编写程序很不方便，我们可以安装几个uniapp插件解决这些问题。我们在VSCode的扩展商店中搜索一下uniapp，这里需要安装3个插件：.**

* **uniapp小程序扩展.**
* **uni-create-view.**
* **uni-helper.**

**安装完之后，我们在编写页面时，会有提示：.**

**在新建页面时，会有uniapp相关的选项：.**

**这些对于我们实际开发是非常由帮助的。.**

### 安装uniapp的types.

**我们可以看到vue文件中，uniapp的组件并没有变绿，说明ts是没有生效的，我们先把uniapp的类型文件安装一下，如下：.**

```
pnpm i -D @uni-helper/uni-app-types @uni-helper/uni-ui-types.
```

**我们在使用pnpm安装时，会报错，我们根据uni-helper的官方文档中的提示，将 shamefully-hoist 为 true。这个需要我们找到家目录下的.npmrc文件，如图：.**

**然后在文件中增加：.**

```
registry=http://registry.npm.taobao.org.
shamefully-hoist=true.
```

**然后，我们再执行pnpm命令安装类型文件。安装完成后，在项目根目录下，打开tsconfig.json文件，在types中增加我们安装的类型：.**

```
{
  "extends".: "@vue/tsconfig/tsconfig.json".,
  "compilerOptions".: {
…….
    "types".: [
      "@dcloudio/types".,
      "@uni-helper/uni-app-types".,
      "@uni-helper/uni-ui-types".
    ]
  }
…….
}
```

**添加完成后，我们发现compilerOptions是有报错的，鼠标悬停上去发现：.**

**报错提示两个选项将要废弃，我们要把这个错误提示去掉，可以在文件中增加"ignoreDeprecations": "5.0",：.**

```
{
  "extends".: "@vue/tsconfig/tsconfig.json".,
  "compilerOptions".: {
    "ignoreDeprecations".: "5.0".,
…….
  },
  "include".: ["src/**/*.ts"., "src/**/*.d.ts"., "src/**/*.tsx"., "src/**/*.vue".]
}
```

**这样compilerOptions就不报错了。然后我们打开vue文件，发现uniapp的标签都变绿了，但是会有报错，这个VSCode的插件之间有冲突造成的，我们可以配置如下解决，参考官方文档：.**

```
{
…….
  "vueCompilerOptions".: {
    "plugins".: ["@uni-helper/uni-app-types/volar-plugin".]
  },
…….
}
```

**然后重启VSCode。最后我们发现vue文件的uniapp标签变绿了，而且没有报错：.**

**最后tsconfig.json的整体内容如下：.**

```
{
  "extends".: "@vue/tsconfig/tsconfig.json".,
  "compilerOptions".: {
    "ignoreDeprecations".: "5.0".,
    "sourceMap".: true.,
    "baseUrl".: ".".,
    "paths".: {
      "@/*".: ["./src/*".]
    },
    "lib".: ["esnext"., "dom".],
    "types".: [
      "@dcloudio/types".,
      "@uni-helper/uni-app-types".,
      "@uni-helper/uni-ui-types".
    ]
  },
  "vueCompilerOptions".: {
    "plugins".: ["@uni-helper/uni-app-types/volar-plugin".]
  },
  "include".: ["src/**/*.ts"., "src/**/*.d.ts"., "src/**/*.tsx"., "src/**/*.vue".]
}
```

### 最后.

**到这里，我们的uniapp项目就搭建完成了，而且是使用我们非常熟悉的VSCode，项目中还是用了Vue3，Typescript，Vite，该装的插件也已经装上了，鼠标悬停会给我们组件的提示，大大提高了我们的开发效率。OK了，去开发我们的项目应用吧~~~.**
