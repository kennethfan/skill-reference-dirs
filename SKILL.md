---
name: reference-dirs
description: Resolve the directories outside the current project that may be referenced for context — 额外引用目录. Use when the agent needs to read sibling projects, shared docs, or adjacent code beyond the current repo, or when the user asks 引用其他目录 / 兄弟项目 / 参考外部目录 / reference other projects. Runs scripts/reference-dirs.py, which walks up from the project folder collecting .reference-dirs.json configs and merges them (parent-first, deduped).
---

Resolve the current project's additional reference directories and use them as read-only context sources.

## Steps

1. Run the resolver:

   ```
   python3 scripts/reference-dirs.py
   ```

   Output: one absolute path per line (use `--json` for a JSON array).

2. If the output is **empty**, no `.reference-dirs.json` exists anywhere up the tree — this is normal. There is nothing to reference. Report this only if the user asked explicitly.

3. Use the listed directories as additional reference roots: search them, read their files, and consult their code when the current project's own context is insufficient.

## How reference dirs are configured

Configs are **distributed** — each folder may carry a `.reference-dirs.json` declaring what projects under it may additionally reference:

```json
{
  "refs": ["project-core", "../shared-docs", "~/codes/common"]
}
```

- Paths resolve **relative to the config file's folder**; `~` expands to home; absolute paths pass through.
- The resolver walks up from the project folder to home, merging every config found: union + dedupe, parent folders first.
- Reference dirs are leaf targets — never recursively expanded.
- To enable references for a folder, create `.reference-dirs.json` there. A full example lives in `examples/.reference-dirs.json.example`.
