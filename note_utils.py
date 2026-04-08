"""Generate and persist LeetCode Hot100 daily note templates.

This module is intentionally self-contained and avoids external network calls.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict


@dataclass(frozen=True)
class PracticeLink:
    title: str
    reason: str


def slugify(s: str) -> str:
    # Keep simple: remove path-hostile chars
    keep = []
    for ch in s:
        if ch.isalnum() or ch in ("-", "_", " "):
            keep.append(ch)
    return " ".join("".join(keep).split())


def note_filename(problem_id: int, title: str) -> str:
    safe = slugify(title)
    return f"{problem_id:04d}_{safe}.md"


def build_note(problem_id: int, title: str, five_solutions_md: str, practice: List[PracticeLink]) -> str:
    prac_md = "\n".join([f"- {p.title}：{p.reason}" for p in practice]) if practice else "- （无）"

    return f"""# LeetCode Hot100 #{problem_id} — {title}

> 归档规则：按题号保存。来源：每日 13:30 自动推送。

## 五种解法（暴力 → 最优）

{five_solutions_md.strip()}

## 同类题目练习（建议做 3-6 题）

{prac_md}

## 自测清单（像测试用例一样）

- [ ] 最小输入/空输入（若题意允许）
- [ ] 只有 1 个元素/1 个节点/1 个字符
- [ ] 全相同 / 全不同
- [ ] 极值（最大长度、最大/最小数值、负数）
- [ ] 结果不存在（若题意允许）
- [ ] 多解时是否要求任意/唯一/返回索引顺序
"""


def save_note(dir_path: str | Path, problem_id: int, title: str, five_solutions_md: str, practice: List[PracticeLink]) -> Path:
    dir_path = Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    out = dir_path / note_filename(problem_id, title)
    out.write_text(build_note(problem_id, title, five_solutions_md, practice), encoding="utf-8")
    return out
