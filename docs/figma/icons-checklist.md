# Figma 图标清单与导出指南

**目的**：从 Figma UI Kit 中提取所有图标，进行命名规范化，并为批量导出做准备。

**状态**：由于无法一次性扫描整个 Figma 文件，本清单目前仅基于已获取的局部节点数据（如 `1:1038`）生成示例。待获取更多组件节点数据后，将持续更新。

## 图标清单

| 预览 (如有) | Figma 节点名称      | 节点 ID      | 建议命名 (kebab-case) | 状态 | 目标路径 (packages/ui/src/icons/) |
| :---------- | :------------------ | :----------- | :-------------------- | :--- | :-------------------------------- |
|             | `bx:bxs-home-smile` | `1:1216`     | `home-smile`          | 待定 | `home-smile.svg`                  |
|             | `Icon/Comet/Regular`| `1448:12181` | `comet`               | 待定 | `comet.svg`                       |
|             | `Icon/Favorite/Regular`| `858:1138`   | `favorite`            | 待定 | `favorite.svg`                    |
|             | `Icon/Chevron-down/Regular`| `857:926`    | `chevron-down`        | 待定 | `chevron-down.svg`                |
|             | `Icon/Leaf/Regular` | `1264:11028` | `leaf`                | 待定 | `leaf.svg`                        |
|             | `Icon/Alert/Regular`| `1004:3341`  | `alert`               | 待定 | `alert.svg`                       |
|             | `Icon/Eye/Regular`  | `1004:3230`  | `eye`                 | 待定 | `eye.svg`                         |
|             | `Icon/Card/Regular` | `123:354`    | `card`                | 待定 | `card.svg`                        |
|             | `Icon/Info-bold/Regular`| `960:2045`   | `info-bold`           | 待定 | `info-bold.svg`                   |
|             | `Icon/Chevron-up/Regular`| `857:925`    | `chevron-up`          | 待定 | `chevron-up.svg`                  |
|             | `Icon/Wallet/Regular`| `960:2501`   | `wallet`              | 待定 | `wallet.svg`                      |
|             | `Icon/Building-bank/Regular`| `960:2063` | `building-bank`       | 待定 | `building-bank.svg`               |
|             | `Icon/Plus/Regular` | `1:651`      | `plus`                | 待定 | `plus.svg`                        |
|             | `Icon / Check`      | `1:160`      | `check`               | 待定 | `check.svg`                       |
|             | `Icon/Search/Regular` | `1:849`      | `search`              | 待定 | `search.svg`                      |
|             |                     |              |                       |      |                                   |

---

## 导出流程建议

1.  **识别图标节点**：在 Figma 文件中，所有作为图标使用的 `VECTOR`, `COMPONENT`, 或 `INSTANCE` 都应被记录在此清单中。
2.  **规范化命名**：
    *   采用 `kebab-case` 命名法（例如 `arrow-left`）。
    *   命名应反映图标的**功能**而非其视觉表现（例如 `icon-close` 而非 `icon-x`）。
    *   处理冲突：如果多个图标视觉上相似但用途不同，可通过后缀区分（如 `arrow-left-small`）。
3.  **更新清单**：将识别出的图标信息填入上表。
4.  **批量导出**：
    *   使用 Figma API 和此清单中的节点 ID 批量请求 SVG 导出。
    *   确保导出时已应用所有必要的变换，且视图框（viewBox）正确。
5.  **代码集成**：
    *   将导出的 `.svg` 文件存放于 `packages/ui/src/icons/` 目录下。
    *   在 Storybook 中创建一个“Icons”分类，展示所有可用图标及其命名，方便开发者查阅。
