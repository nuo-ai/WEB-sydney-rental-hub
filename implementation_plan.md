# Implementation Plan

[Overview]
本计划旨在将现有的 Vue 3 Web 应用重塑为一个专业、现代的微信小程序 MVP，核心是建立一个强大且灵活的设计令牌（Design Token）系统，并以此驱动所有 UI 组件的开发，确保最终产品在视觉和交互上达到行业顶尖水准。

我们将严格遵循“逻辑复用，UI重塑”的战略，最大化保留现有的业务逻辑（Pinia Stores），同时为小程序平台量身定制全新的、体验优先的视图层。整个过程将以“原子设计”和“组件驱动开发”为指导思想，通过 Style Dictionary 实现设计令牌的自动化构建，并以 Storybook 作为组件开发和验证的核心环境。

[Types]
我们将定义一套严格的三层设计令牌结构（Primitive, Semantic, Component），以 JSON 格式进行管理，确保设计语言的系统性和可扩展性。

**1. 原始令牌 (Primitive Tokens)**
*   **路径**: `tokens/base/`
*   **结构**:
    ```json
    // tokens/base/color/brand.json
    {
      "color": {
        "brand": {
          "primary": {
            "50": { "value": "#E6F0FF" },
            "100": { "value": "#B3D1FF" },
            // ...
            "500": { "value": "#0066CC" }, // Juwu-Blue-500
            // ...
            "900": { "value": "#001A33" }
          },
          "accent": {
            "500": { "value": "#EA5420" } // Juwu-Orange-500
          }
        }
      }
    }
    ```

**2. 语义令牌 (Semantic Tokens)**
*   **路径**: `tokens/themes/`
*   **结构**:
    ```json
    // tokens/themes/light.json
    {
      "color": {
        "background": {
          "page": { "value": "{color.neutral.gray.50.value}" },
          "surface": { "value": "{color.base.white.value}" }
        },
        "text": {
          "primary": { "value": "{color.neutral.gray.900.value}" },
          "secondary": { "value": "{color.neutral.gray.600.value}" }
        },
        "action": {
          "primary": { "value": "{color.brand.primary.500.value}" }
        }
      }
    }
    ```

**3. 组件令牌 (Component-Specific Tokens)**
*   **路径**: `tokens/components/`
*   **结构**:
    ```json
    // tokens/components/card.json
    {
      "component": {
        "card": {
          "background-color": { "value": "{color.background.surface.value}" },
          "border-radius": { "value": "{radius.md.value}" },
          "padding": { "value": "{space.lg.value}" },
          "shadow": { "value": "{shadow.sm.value}" }
        }
      }
    }
    ```

[Files]
我们将重构 `tokens` 目录，新建一个小程序应用骨架，并配置 Style Dictionary 自动化流程。

*   **新建文件/目录**:
    *   `apps/mini-program/`: 新建小程序项目根目录。
    *   `apps/mini-program/src/`: 小程序源码目录。
    *   `apps/mini-program/src/main.ts`: 小程序入口文件。
    *   `apps/mini-program/src/app.ts`: 小程序全局配置。
    *   `apps/mini-program/src/pages/`: 页面目录。
    *   `apps/mini-program/src/styles/generated/`: 存放 Style Dictionary 生成的 `wxss` 文件。
    *   `build-tokens.js`: 在项目根目录创建 Style Dictionary 构建脚本。
    *   `tokens/base/color/brand.json`, `tokens/base/color/neutral.json`, `tokens/base/size/space.json`, etc.
    *   `tokens/themes/light.json`, `tokens/themes/dark.json`
    *   `packages/ui/src/components/PropertyCard/PropertyCard.vue`: 新建小程序版的房源卡片组件。

*   **修改的文件**:
    *   `tokens/design-tokens.json`: 将被拆分为上述新的 `tokens/` 目录结构。
    *   `package.json`: 添加 `build:tokens` 脚本，并引入 `style-dictionary` 和 `uni-app` 相关依赖。
    *   `packages/ui/.storybook/preview.js`: 配置 Storybook 以加载生成的 `wxss` 文件，实现小程序组件预览。

*   **删除的文件**:
    *   `tokens/design-tokens.json` (在拆分完成后)。

[Functions]
我们将创建一个核心的 Style Dictionary 构建函数，并重构部分可复用的工具函数。

*   **新建函数**:
    *   `getStyleDictionaryConfig(theme)`: 在 `build-tokens.js` 中，用于动态生成亮色/暗色主题的配置。
    *   `registerWxssFormat()`: 在 `build-tokens.js` 中，注册一个自定义格式，以确保生成的 CSS 变量能被小程序正确识别。

*   **修改的函数**:
    *   `apps/web/src/utils/` 中的纯逻辑函数将被评估，并可能移动到 `packages/utils` 共享包中，供 Web 和小程序共同使用。

[Classes]
本次重构不涉及主要的 Class 变更，重点在于函数式组件和设计令牌。

[Dependencies]
我们将引入 Style Dictionary 用于令牌自动化，并选择 `uni-app` + `ThorUI` 作为小程序的技术栈。

*   **新增依赖 (devDependencies)**:
    *   `style-dictionary`: 核心令牌转换引擎。
    *   `@dcloudio/vite-plugin-uni`: `uni-app` 的 Vite 插件。
    *   `@dcloudio/uni-mp-weixin`: `uni-app` 微信小程序平台支持。
    *   `thorui-uni-app`: ThorUI 组件库。

*   **版本确认**: 所有新依赖将使用最新的稳定版本。

[Testing]
我们将为新的共享组件和工具函数添加单元测试，并在 Storybook 中进行视觉回归测试。

*   **新建测试文件**:
    *   `packages/ui/src/components/PropertyCard/PropertyCard.spec.ts`: `PropertyCard` 组件的单元测试。
    *   `packages/utils/src/format.spec.ts`: 共享工具函数的单元测试。
*   **测试策略**:
    *   **单元测试**: 使用 `Vitest` 对组件的 props 传递和事件触发进行测试。
    *   **视觉测试**: 在 Storybook 中为每个组件创建 stories，覆盖不同 props 和主题（亮/暗）下的视觉表现。

[Implementation Order]
我们将遵循一个严谨的、自下而上的顺序，先建立设计系统基础，再构建组件，最后组装页面。

1.  **环境搭建**: 在 `apps/` 目录下初始化一个新的 `uni-app` 项目 (`mini-program`)。
2.  **令牌系统重构**:
    *   按照 `[Files]` 部分的规划，重构 `tokens/` 目录结构。
    *   使用 `交互式AI设计令牌工作流.html` 工具，与您共同确定最终的 `brand.json` 和 `themes/*.json` 内容。
3.  **自动化管道配置**:
    *   创建并配置 `build-tokens.js` 脚本。
    *   运行 `npm run build:tokens`，生成初始的 `theme-light.wxss` 和 `theme-dark.wxss` 文件。
4.  **Storybook 集成**:
    *   修改 Storybook 配置，使其能够加载并应用生成的 `wxss` 文件。
5.  **原子组件开发**:
    *   基于对 `Domain.com.au` 的分析，优先开发或调整 `packages/ui` 中的核心原子组件（如 `Button`, `Tag`, `Icon`），确保它们在小程序环境（Storybook 预览）中表现正确。
6.  **`PropertyCard` 组件重塑**:
    *   创建 `PropertyCard.vue` 组件，其 `<template>` 部分使用 `uni-app` 的原生组件（如 `<view>`, `<image>`, `<text>`），`<style>` 部分完全使用已定义的语义化令牌。
7.  **页面组装与逻辑注入**:
    *   搭建四个核心页面的静态布局。
    *   将 `Pinia stores` 从 `apps/web` 引入到 `apps/mini-program`，并完成状态和事件的绑定。
8.  **联调与测试**:
    *   进行端到端的功能测试和 UI 视觉走查。
