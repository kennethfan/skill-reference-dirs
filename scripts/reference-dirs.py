#!/usr/bin/env python3
"""reference-dirs — 解析当前项目可额外引用的目录列表。

从 cwd 向上逐级查找 `.reference-dirs.json`(到 home 为止),合并所有命中的
`refs` 数组(并集+去重,父级在前、子级在后),输出绝对路径列表。

用法:
    reference-dirs.py [--json] [cwd]

默认从当前目录开始查找;`--json` 输出 JSON 数组,否则每行一个绝对路径。
"""

import argparse
import json
import os
import sys
from pathlib import Path

CONFIG_NAME = ".reference-dirs.json"


def expand_ref(ref: str, base_dir: Path) -> Path:
    """解析 refs 中的一条路径:相对 base_dir、~ 开头或绝对路径。"""
    if ref.startswith("~"):
        return Path(os.path.expanduser(ref))
    p = Path(ref)
    if p.is_absolute():
        return p
    return base_dir / p


def collect_levels(start: Path, stop: Path) -> list[Path]:
    """从 start 向上收集到 stop(含)之间的所有目录,顺序为从近到远。"""
    levels: list[Path] = []
    cur = start.resolve()
    stop = stop.resolve()
    while True:
        levels.append(cur)
        if cur == stop:
            break
        parent = cur.parent
        if parent == cur:
            break
        cur = parent
    return levels


def resolve(cwd: str | None = None) -> list[str]:
    """返回合并去重后的引用目录绝对路径列表,父级在前、子级在后。"""
    start = Path(cwd).resolve() if cwd else Path.cwd().resolve()
    home = Path.home()

    levels = collect_levels(start, home)
    # 父级在前、子级在后
    levels.reverse()

    refs: list[str] = []
    seen: set[str] = set()
    for level in levels:
        config = level / CONFIG_NAME
        if not config.is_file():
            continue
        try:
            data = json.loads(config.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            print(f"warning: 解析 {config} 失败: {e}", file=sys.stderr)
            continue
        for ref in data.get("refs", []):
            if not isinstance(ref, str) or not ref.strip():
                continue
            resolved = expand_ref(ref.strip(), level).resolve()
            key = str(resolved)
            if key not in seen:
                seen.add(key)
                refs.append(key)
    return refs


def main() -> int:
    parser = argparse.ArgumentParser(description="解析当前项目可额外引用的目录列表")
    parser.add_argument("--json", action="store_true", help="输出 JSON 数组")
    parser.add_argument("cwd", nargs="?", default=None, help="起始目录(默认当前目录)")
    args = parser.parse_args()

    refs = resolve(args.cwd)
    if args.json:
        print(json.dumps(refs, ensure_ascii=False))
    else:
        for ref in refs:
            print(ref)
    return 0


if __name__ == "__main__":
    sys.exit(main())