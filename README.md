# HTML Report Tuner

给任意一份已成型的 HTML 报告现场生成一个独立的**HTML报告修改工具**——不再需要耗费大量token和AI反复对话调整细节，而是自己在浏览器里动手编辑内容构成、修改错误表述、调整配色，输出调整完毕的html。

左侧是参数面板（Style Control Panel），右侧供你实时预览目标文档，并且原始文件自始至终不会被覆盖，也不会上传到任何外部服务。

## 工作方式

此Skill让你的AI**现场阅读、理解、解构你的HTML**，最终针对你的HTML报告生成一份标准化的版式色彩调试工具。

## 功能一览

- **颜色**：自动探测或改写 CSS 变量，取色器实时预览；双向"定位" —— 点击颜色查看位置 & 点击想要修改的部分高亮对应颜色。
- **配色卡**：17 套预设，一键切换整套配色。
- **模块拖拽**：自动判断模块边界，适配上下左右拖拽已有模块，添加新模块，帮助你规划报告逻辑。
- **文字编辑**：可增删改已有文字，无需在与AI对话。
- **撤回**：支持撤回颜色、模块的变更。

## 怎么安装

## Install
npx skills add Ria-dong/html-report-tuner


Re-run any time to update. Or copy `SKILL.md` + `scripts/` + `templates/` into:

* Claude Code: `~/.claude/skills/html-report-tuner/`
* Cursor: `.cursor/rules/html-report-tuner.mdc` (body of `SKILL.md`, no frontmatter)
* Codex: `~/.codex/skills/html-report-tuner/` (personal) or `.codex/skills/html-report-tuner/` (project-scoped)

The rule-set lives in `SKILL.md`. The reusable interaction shell (panel UI, drag engine, color math) lives in `templates/tuner-shell.html`; the build script is `scripts/build_tuner.py`.

## 怎么用

在你的AI里触发这个 skill（比如"帮我做个调整工具"）即可一键使用。

## 目录结构

```
html-report-tuner/
├── SKILL.md              # 完整流程、硬规则、已知局限——每次调用前要读的那份
├── templates/
│   └── tuner-shell.html  # 通用壳子：面板UI、颜色数学、拖拽引擎、撤回栈、极光背景
└── scripts/
    └── build_tuner.py    # 构建脚本，CONFIG 是每次要重新填的部分
```

## 局限

- 颜色：浅底徽章/透明度变体类的衍生色不纳入调整范围，固定跟随原值。
- 模块：只做一层展开——嵌套两层以上的重复结构（比如小节内部的引文卡片网格）不会被拆开，整体算一个模块。纯内联 `flex` 分栏、既没有可识别 class 也没有 border/background signature 的布局，不会被自动拆开。
- 拖拽重排后，文档里的页码、章节编号等"位置编码"内容不会自动重新编号。
- 文字编辑不进撤回栈（细碎到逐字符，没法做有意义的"一步"切分；浏览器自带 Ctrl+Z 在可编辑区域本来就管用）。

详细说明、每一条背后的实测证据，见 `SKILL.md`。

## License

MIT，见 [LICENSE](LICENSE)。
