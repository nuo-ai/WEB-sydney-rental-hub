Figma UI Kit → 设计 Tokens 映射草稿（初版）

说明
- 目的：将 Figma UI Kit 的基础样式与组件样式，映射到本仓库 tokens/ 下的可执行结构，保持与现有代码最小摩擦。
- 现状：因 Figma API 403 暂无法自动拉取真实数值，本草稿先给出“命名与落地路径”的模板与示例，待解除 403 后填充具体值。
- 对前端表现的解释：每条映射都附“UI 用途/表现”，帮助非技术同学理解该 Token 在页面中的视觉作用（如“按钮主色背景”）。

目录
1) 基础/颜色 colors（brand, neutral）
2) 基础/字体 typography（家族/字号/字重/行高/字间距）
3) 基础/间距 spacing（间距刻度）
4) 基础/圆角 radius（圆角刻度）
5) 基础/阴影 shadows（海拔层级）
6) 组件级 tokens（button/card/chip/input/list-item/search-input/toggle）
7) 主题（themes/light, themes/dark）与语义色建议
8) 待办与下一步

————————————————————————————————————

1) 基础/颜色 colors

现有落地点
- tokens/base/color/brand.json
- tokens/base/color/neutral.json

命名建议（示例）
- 品牌色：brand/{primary|secondary}/{50|100|200|300|400|500|600|700|800|900}
- 中性灰：neutral/{50..900}
- 辅助色（如需要）：success/warning/error/info（建议先收敛到 brand/neutral，辅助色如 UI Kit 有再加）

**用户指示：** 此部分跳过，沿用仓库现有颜色体系。

注意
- 前端表现：颜色不带透明度，透明场景建议通过 alpha 合成派生（如在 themes 层定义），避免在 base 层写死透明度。

————————————————————————————————————

2) 基础/字体 typography

现有落地点
- tokens/base/font.json（建议内含 family/size/weight/lineHeight/letterSpacing 等）

命名建议
- 字体家族：font.family.{sans|serif|mono}
- 字号：font.size.{xs,sm,md,lg,xl,2xl,3xl...}
- 字重：font.weight.{regular,medium,semibold,bold}
- 行高：font.lineHeight.{tight,normal,relaxed}
- 字间距：font.letterSpacing.{tight,normal,wide}

映射模板（根据 raw.json 真实值填充）
- Figma: Heading/H1 → tokens: base/font.size.3xl=32pt, base/font.weight.bold, base/font.lineHeight.tight=120% → UI 用途：一级标题
- Figma: Heading/H2 → tokens: base/font.size.2xl=28pt, base/font.weight.semibold, base/font.lineHeight.tight=120% → UI 用途：二级标题
- Figma: Heading/H3 → tokens: base/font.size.xl=24pt, base/font.weight.semibold, base/font.lineHeight.normal=125% → UI 用途：三级标题
- Figma: Heading/H4 → tokens: base/font.size.lg=20pt, base/font.weight.semibold, base/font.lineHeight.normal=140% → UI 用途：四级标题/卡片标题
- Figma: Body/Medium/Regular → tokens: base/font.size.md=16pt, base/font.weight.regular, base/font.lineHeight.relaxed=150% → UI 用途：正文段落
- Figma: Body/Small/Regular → tokens: base/font.size.sm=14pt, base/font.weight.regular, base/font.lineHeight.normal=140% → UI 用途：辅助说明文字
- Figma: Body/XSmall/Regular → tokens: base/font.size.xs=12pt, base/font.weight.regular, base/font.lineHeight.tight=135% → UI 用途：标签/次要说明

注意
- 前端表现：字号与行高作为分离 tokens，组件层通过引用组合，便于在不同密度下调整。

————————————————————————————————————

3) 基础/间距 spacing

现有落地点
- tokens/base/size/space.json

命名与刻度（已确认）
- size.space.{xxs=4, xs=8, sm=12, md=16, lg=24, xl=32, 2xl=40, 3xl=48} (8pt 基线)

————————————————————————————————————

4) 基础/圆角 radius

现有落地点
- tokens/base/radius.json

命名与刻度（已确认）
- radius.{sm=4, md=8, lg=12, pill=9999}

————————————————————————————————————

5) 基础/阴影 shadows

现有落地点
- tokens/base/shadow.json

命名与层级（已确认）
- shadow.{sm, md, lg, xl, focus}
  - sm：细微浮起（小卡片/悬浮菜单）
  - md：标准浮起（对话框/悬浮层）
  - lg：显著浮起（大型弹出）
  - focus：焦点描边或投影

前端表现说明
- 阴影通常包含 x, y, blur, spread, color（含透明度）。建议以对象存储，构建时序列化为 CSS box-shadow。

————————————————————————————————————

6) 组件级 tokens

现有落地点（已存在文件）
- tokens/components/button.json
- tokens/components/card.json
- tokens/components/chip.json
- tokens/components/input.json
- tokens/components/list-item.json
- tokens/components/search-input.json
- tokens/components/toggle.json

通用命名建议
- 颜色（语义引用）：color.{bg|text|border}.{state}
- 尺寸：padding.{x|y}.{size}、gap.{size}、height.{size}
- 圆角：radius（引用 base/radius）
- 阴影：shadow（引用 base/shadow）
- 状态：{default, hover, active, disabled, focus}

Button（按钮）映射示例（伪 JSON）
{
  "button": {
    "radius": {
      "default": "32px",
      "pill": "100px"
    },
    "padding": {
      "lg": "17px",
      "md": "10px",
      "sm": "8px"
    },
    "typography": {
      "lg": {
        "size": "{base.font.size.md}",
        "weight": "{base.font.weight.bold}"
      },
      "md": {
        "size": "{base.font.size.sm}",
        "weight": "{base.font.weight.semibold}"
      },
      "sm": {
        "size": "{base.font.size.xs}",
        "weight": "{base.font.weight.semibold}"
      }
    },
    "primary": {
      "color": {
        "bg": "{base.color.brand.primary.500}",
        "text": "{base.color.neutral.0}"
      }
    },
    "secondary": {
      "color": {
        "bg": "{base.color.neutral.0}",
        "text": "{base.color.brand.primary.500}"
      }
    }
  }
}
UI 用途/表现
- 按钮组件，包含主要和次要两种类型，大、中、小三种尺寸，并支持带图标和暗黑模式。

Card（卡片）映射示例（伪 JSON）
{
  "card": {
    "size": "156px",
    "radius": "16px",
    "typography": {
      "size": "{base.font.size.md}",
      "weight": "{base.font.weight.semibold}"
    },
    "color": {
      "bg": {
        "default": "{themes.color.surface}",
        "selected": "{themes.color.surface.selected}"
      },
      "border": {
        "default": "{base.color.neutral.200}",
        "selected": "{themes.color.accent}"
      },
      "text": {
        "default": "{themes.color.text.primary}"
      }
    }
  }
}
UI 用途/表现
- 卡片用于展示摘要信息，包含选中和未选中状态，并支持亮色和暗色模式。圆角为16px。

Label（标签）映射示例（根据新 Figma 文件 lgkd1P8o8oJR8lN5Tnu0gW 填充）
{
  "label": {
    "radius": "5px",
    "padding": {
      "x": "{base.size.space.xs}",
      "y": "{base.size.space.xxs}"
    },
    "gap": "{base.size.space.xxs}",
    "typography": {
      "size": "{base.font.size.xs}",
      "weight": "{base.font.weight.medium}"
    }
  }
}
UI 用途/表现
- 标签用于展示少量、简洁的信息，可带图标。圆角为 5px，内边距为 4px 8px，图标与文字间距为 4px。

Chip（纸片）映射示例
{
  "chip": {
    "radius": "100px",
    "padding": {
      "x": "{base.size.space.md}",
      "y": "{base.size.space.xxs}"
    },
    "typography": {
      "size": "{base.font.size.sm}",
      "weight": "{base.font.weight.regular}"
    }
  }
}
UI 用途/表现
- Chip 用于表示小的、可选择的实体，如筛选标签。具有完全圆角。

Button-circle（圆形按钮）映射示例
{
  "button-circle": {
    "size": "32px",
    "radius": "100px",
    "color": {
      "bg": {
        "selected": "{base.color.brand.primary.500}",
        "unselected": {
          "light": "{base.color.neutral.0}",
          "dark": "{base.color.neutral.900}"
        }
      },
      "icon": {
        "selected": "{base.color.neutral.0}",
        "unselected": {
          "light": "{base.color.neutral.400}",
          "dark": "{base.color.neutral.300}"
        }
      }
    }
  }
}
UI 用途/表现
- 用于独立的图标按钮，如收藏。包含选中和未选中状态，并支持亮色和暗色模式。

Pill（胶囊）映射示例
{
  "pill": {
    "radius": {
      "default": "12px",
      "full": "32px"
    },
    "padding": {
      "x": "{base.size.space.md}",
      "y": "10px"
    },
    "gap": "{base.size.space.xs}",
    "typography": {
      "size": "{base.font.size.sm}",
      "weight": "{base.font.weight.regular}"
    }
  }
}
UI 用途/表现
- 胶囊用于下拉选择器或带图标的标签，支持不同圆角和图标位置。

Tabs（标签页）映射示例
{
  "tabs": {
    "rounded": {
      "radius": "100px",
      "padding": "2px",
      "item": {
        "padding": {
          "x": "{base.size.space.lg}",
          "y": "{base.size.space.xs}"
        },
        "radius": "100px",
        "typography": {
          "size": "{base.font.size.sm}",
          "weight": "{base.font.weight.regular}"
        }
      }
    },
    "square": {
      "item": {
        "padding": {
          "y": "{base.size.space.md}"
        },
        "typography": {
          "size": "{base.font.size.sm}",
          "weight": "{base.font.weight.semibold}"
        }
      }
    }
  }
}
UI 用途/表现
- Tabs 用于在不同视图之间切换。提供圆角和方形两种样式，并支持亮色和暗色模式。

Input（输入框）映射示例
{
  "input": {
    "radius": "12px",
    "padding": {
      "x": "{base.size.space.md}",
      "y": "{base.size.space.sm}"
    },
    "typography": {
      "size": "{base.font.size.md}",
      "weight": "{base.font.weight.regular}"
    },
    "color": {
      "text": {
        "default": "{themes.color.text.primary}",
        "placeholder": "{themes.color.text.secondary}"
      },
      "border": {
        "default": "{themes.color.border.default}",
        "focus": "{themes.color.accent}",
        "error": "{themes.color.error}"
      }
    }
  }
}
UI 用途/表现
- 输入框用于用户文本输入，包含默认、焦点、填充和错误等多种状态，并支持内嵌图标。

App Icon（应用图标）映射示例
{
  "app-icon": {
    "size": {
      "large": "64px",
      "small": "32px"
    },
    "radius": {
      "large": "16px",
      "small": "8px"
    },
    "typography": {
      "large": {
        "font-size": "40px"
      },
      "small": {
        "font-size": "24px"
      }
    }
  }
}
UI 用途/表现
- 应用图标，包含 Logogram 和完整的 Renta 文字标志，提供大、小两种尺寸，并对应不同的字号。

View Type（视图切换）映射示例
{
  "view-type": {
    "radius": "12px",
    "padding": {
      "x": "{base.size.space.md}",
      "y": "{base.size.space.sm}"
    },
    "gap": "{base.size.space.sm}",
    "typography": {
      "size": "{base.font.size.md}",
      "weight": "{base.font.weight.medium}"
    }
  }
}
UI 用途/表现
- 用于在列表和网格视图之间切换的控件，包含选中和未选中状态，并支持亮色和暗色模式。

Toggle（切换开关）映射示例
{
  "toggle": {
    "size": {
      "track-width": "44px",
      "track-height": "24px",
      "thumb-size": "20px"
    },
    "radius": {
      "track": "24px",
      "thumb": "9999px"
    },
    "color": {
      "track": {
        "on": "{base.color.brand.primary.500}",
        "off": "{base.color.neutral.200}"
      },
      "thumb": {
        "default": "{base.color.neutral.0}"
      }
    }
  }
}
UI 用途/表现
- 用于切换单个设置的开/关状态。

Checkbox（复选框）映射示例
{
  "checkbox": {
    "size": "24px",
    "radius": "6px",
    "color": {
      "bg": {
        "checked": "{base.color.brand.primary.500}",
        "unchecked": "{base.color.neutral.0}"
      },
      "border": {
        "checked": "{base.color.brand.primary.500}",
        "unchecked": "{base.color.neutral.300}"
      },
      "icon": {
        "default": "{base.color.neutral.0}"
      }
    }
  }
}
UI 用途/表现
- 用于多项选择。

SearchInput（搜索输入框）映射示例
{
  "search-input": {
    "radius": "12px",
    "padding": "12px",
    "gap": "12px",
    "typography": {
      "size": "{base.font.size.sm}",
      "weight": "{base.font.weight.regular}"
    },
    "color": {
      "placeholder": "{themes.color.text.secondary}"
    }
  }
}
UI 用途/表现
- 用于用户输入搜索查询，包含一个搜索图标。

剩余组件（chip/input/list-item/search-input/toggle）
- 请沿用相同结构：将 Figma 的“组件主态/悬浮/按下/禁用/焦点”等属性，映射到 color/bg/text/border + radius + spacing + shadow + typography。
- 特别说明
  - Input/SearchInput：需覆盖 placeholder 文本色、边框 focus/invalid 态；建议引入 semantic: color.border.{default|focus|invalid}
  - ListItem：关注选中态背景/文字色、分隔线颜色与密度（padding）
  - Toggle：需要显式区分 track 与 thumb 的颜色/阴影；大小与交互动效保持一致性

————————————————————————————————————

7) 主题与语义色（themes/light.json, themes/dark.json）

现有落地点
- tokens/themes/light.json
- tokens/themes/dark.json

建议在 themes 中引入语义抽象（示例键）
- color.surface：界面基础背景（卡片/容器背景）
- color.elevated：浮起层背景（弹出层）
- color.text.primary：主文本色
- color.text.secondary：次文本色
- color.border.default：通用描边色
- color.accent：强调色（映射 brand.primary.500）
- color.link：链接色（可与 accent 同步或独立）
- color.success/warning/error：语义反馈色（如 UI Kit 提供）

映射关系（示例）
- light: color.text.primary → neutral.900；dark: → neutral.50
- light: color.surface → neutral.0；dark: → neutral.900（或近黑）
- light/dark 分别调优 hover/active 阶梯，确保对比度符合 WCAG AA

前端表现说明
- 组件层引用 themes 下的语义色，而非直接引用 base/brand/neutral，以便主题切换与可访问性改进。

————————————————————————————————————

8) 待办与下一步

阻塞项
- 无法自动定位 Figma 节点 ID，部分基础样式（间距/圆角/阴影）暂用建议值。

下一步
- 生成 icons-checklist.md：包含图标节点 ID、命名建议（kebab-case）、去重与冲突提示、目标目录 packages/ui/src/icons/
- 评审通过后：批量下载 SVG → 新增 Storybook 对照页（“Figma 基线映射”）
- 评审通过后：批量下载 SVG → 新增 Storybook 对照页（“Figma 基线映射”）

校验清单（在引入真实值后执行）
- 颜色对比度（文本/背景 ≥ AA）
- 交互态阶梯（hover/active/disabled）在 light/dark 下可读可感知
- 组件间距统一（以 space 刻度驱动）
- 主题切换无断层（语义色覆盖全面）
- 命名一致且稳定（避免与已有 tokens 冲突，必要时在 components 层落语义而非 base 层改名）

附注
- 本草稿只定义结构与规范，不强行变更现有 tokens 文件命名；如需重构，将在后续 PR 中通过兼容层（aliases）与迁移脚本渐进推进。
