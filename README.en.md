# skill-reference-dirs

[中文](README.md) | **English**

Determines the list of directories the currently opened project may additionally reference, for the agent to read as context (read-only).

## What is this

reference-dirs is an OpenCode skill: when the agent needs to read sibling projects, shared docs, or adjacent code beyond the current repo, it walks up from the project folder collecting `.reference-dirs.json` configs via `scripts/reference-dirs.py` and merges them (union + dedupe, parent folders first) into a list of additional reference directories for the current project.

Reference dirs are **read-only** and are leaf targets — never recursively expanded.

## Usage

1. Run the resolver:

   ```
   python3 scripts/reference-dirs.py
   ```

   Output: one absolute path per line (pass `--json` for a JSON array).

2. If the output is **empty**, no `.reference-dirs.json` exists anywhere up the tree — this is normal. Report it only if the user asked explicitly.

3. Use the listed directories as additional reference roots: search them, read their files, and consult their code when the current project's own context is insufficient.

## How reference dirs are configured

Configs are **distributed** — each folder may carry a `.reference-dirs.json` declaring what projects under it may additionally reference:

```json
{
  "refs": ["project-core", "../shared-docs", "~/codes/common"]
}
```

Rules:

- Paths resolve **relative to the config file's folder**; `~` expands to home; absolute paths pass through.
- The resolver walks up from the project folder to home, merging every config found: union + dedupe, parent folders first.
- Reference dirs are leaf targets — never recursively expanded.
- To enable references for a folder, create a `.reference-dirs.json` there. A full example lives in `examples/.reference-dirs.json.example`.

## Project structure

```
├── CONTEXT.md                         # Domain glossary
├── SKILL.md                           # Skill definition (step-by-step instructions for the agent)
├── docs/adr/                          # Architecture Decision Records (ADR)
├── examples/
│   └── .reference-dirs.json.example   # Config example
├── scripts/
│   └── reference-dirs.py              # The resolver
├── README.md                          # This doc (Chinese)
└── README.en.md                       # English version
```

## Related docs

- [CONTEXT.md](CONTEXT.md) — domain glossary (reference dir, config file, hierarchical merge, etc.) — currently written in Chinese
- [ADR-0001](docs/adr/0001-distributed-config-with-hierarchical-merge.md) — design decision: distributed config + hierarchical merge — currently written in Chinese
- [中文 README](README.md) — 中文版
