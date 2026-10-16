#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
html-report-tuner 的构建脚本。

用法：复制这个文件（或直接改这份），把下面 CONFIG 区块的内容换成
本次目标文档读出来的实际判断结果，然后跑一遍，产出可交付的调整工具 HTML。

CONFIG 里每一项怎么填，对应 SKILL.md 里的哪一步，脚本内联注释已经写清楚。
"""
import io
import os
import json
import base64

# 模板文件固定和本脚本放在同一个skill目录下的 templates/ 里，动态算出来，
# 不写死绝对路径——这样整个skill文件夹不管搬到哪台机器、哪个路径下都能正常跑。
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DEFAULT_TEMPLATE_PATH = os.path.join(_SKILL_ROOT, "templates", "tuner-shell.html")

# ════════════════════════════════════════════════════════════════
# CONFIG —— 每次调用本 skill，都要重新读目标文档、重新填这一块
# ════════════════════════════════════════════════════════════════
CONFIG = {
    # 模板文件（通常不用改，除非你要改面板本身的通用逻辑）——默认跟这个脚本自身同目录下的templates/走，
    # 不是写死的绝对路径，整个skill文件夹搬到哪台机器/哪个路径下都不用改这一行
    "template_path": _DEFAULT_TEMPLATE_PATH,

    # 目标文档路径 + 输出路径
    "source_path": r"C:\path\to\target.html",
    "out_path": r"./output/替换成任务名_vN_改动点_日期.html",

    # 浏览器标签页标题（面板本身的"Logo"文字固定是"Style Control Panel"，写死在模板里，不用配置）
    "tool_title": "HTML 调色 + 文字 + 模块 调整工具",

    # 导出文件名前缀（保存按钮下载时用，脚本会自动拼日期）
    "export_filename_prefix": "调整版",

    # 第一步产出：颜色 token。
    # - 若目标文档已有 CSS 变量：color_tokens 留空列表，直接在 color_groups 里引用已存在的变量名即可，
    #   不需要 hex->var 的文本替换这一步。
    # - 若目标文档没有变量（颜色是裸 hex 写死的）：在 color_tokens 里列出 (原始hex, 新变量名)，
    #   脚本会做一次性全局替换 + 在 <style> 开头注入 :root 定义。
    "color_tokens": [
        # ("#0b1120", "--bg-a"),
    ],

    # 面板分组：[{"title": 组标题, "kind": "bg"|"ink"|"accent", "vars": [(变量名, 中文语义标签), ...]}, ...]
    # 这里的变量名必须是最终生效的 CSS 变量名——如果上面做了 color_tokens 替换，就填新变量名；
    # 如果目标文档本来就有变量，就直接填它原有的变量名。
    # kind 必须按组的实际性质标对，决定"配色卡一键切换"时这组按哪种规则适配数量：
    #   "bg"     背景/边框类（数量少，不足取前N、超出按明度趋势外推）
    #   "ink"    文字灰阶类（本质是连续渐变，固定在两端点色间按需要级数插值）
    #   "accent" 分类强调色（互相区分的多色相，不足取前N、超出在色相环空隙里插新色）
    "color_groups": [
        # {"title": "背景 / 边框", "kind": "bg", "vars": [("--bg-a", "基础背景")]},
    ],

    # 第三步：模块边界判断
    # container_selector：目标文档里"一页/一个分区"的内容容器选择器
    "container_selector": ".page .container",
    # group_classes：目标文档自己的"网格/弹性布局、带多个重复子项"的 class 名
    # （读目标文档的 <style> 找，不要抄别的文档用过的名字）
    "group_classes": [],
}


def build(cfg):
    with io.open(cfg["template_path"], "r", encoding="utf-8") as f:
        template = f.read()
    with io.open(cfg["source_path"], "r", encoding="utf-8") as f:
        source = f.read()

    rewritten = source
    tokens = cfg["color_tokens"]
    if tokens:
        for hexv, var in tokens:
            rewritten = rewritten.replace(hexv, f"var({var})")
        # 注入 :root 定义——必须在替换之后做，否则 :root 里的新定义会被自己的替换规则二次改写成循环引用
        root_block = "\n<style>\n:root{\n" + "\n".join(
            f"  {var}: {hexv};" for hexv, var in tokens
        ) + "\n}\n</style>\n"
        idx = rewritten.find("<style>")
        if idx == -1:
            idx = rewritten.lower().find("<head>") + len("<head>")
            rewritten = rewritten[:idx] + root_block + rewritten[idx:]
        else:
            rewritten = rewritten[:idx] + root_block.strip("\n") + "\n" + rewritten[idx:]

    b64 = base64.b64encode(rewritten.encode("utf-8")).decode("ascii")

    out = template
    out = out.replace("__SOURCE_B64_PLACEHOLDER__", b64)
    out = out.replace("__TOOL_TITLE_PLACEHOLDER__", cfg["tool_title"])
    out = out.replace("__EXPORT_FILENAME_PLACEHOLDER__", cfg["export_filename_prefix"])
    out = out.replace("__CONTAINER_SELECTOR_PLACEHOLDER__", cfg["container_selector"])
    out = out.replace("__COLOR_GROUPS_JSON_PLACEHOLDER__", json.dumps(cfg["color_groups"], ensure_ascii=False))
    out = out.replace("__GROUP_CLASSES_JSON_PLACEHOLDER__", json.dumps(cfg["group_classes"], ensure_ascii=False))

    with io.open(cfg["out_path"], "w", encoding="utf-8") as f:
        f.write(out)

    print("written:", cfg["out_path"])
    print("color tokens injected:", len(tokens))
    print("color groups:", len(cfg["color_groups"]))
    print("group classes recognized:", cfg["group_classes"])


if __name__ == "__main__":
    build(CONFIG)
