# skill-reference-dirs

**中文** | [English](README.en.md)

根据当前打开项目所在文件夹，决定该项目可以额外引用的目录列表，供 agent 读取参考（只读）。

## 这是什么

reference-dirs 是一个 OpenCode skill：当 agent 需要读取兄弟项目、共享文档或当前仓库之外的相邻代码时，它通过 `scripts/reference-dirs.py` 从项目文件夹向上逐级收集 `.reference-dirs.json` 配置文件，合并（并集 + 去重，父级在前、子级在后）出当前项目可额外引用的目录列表。

引用目录是**只读参考**，且为叶子目标，不递归展开。

## 使用方法

1. 运行解析器：

   ```
   python3 scripts/reference-dirs.py
   ```

   输出：每行一个绝对路径（加 `--json` 输出 JSON 数组）。

2. 如果输出为空，说明从项目路径到 home 之间没有任何 `.reference-dirs.json`——这很正常，没有可引用的目录。除非用户明确询问，否则无需报告。

3. 将列出的目录作为额外的参考根：搜索它们、读取文件，在当前项目自身上下文不足时查阅其中的代码。

## 如何配置

配置是**分布式**的——每个文件夹都可以放一个 `.reference-dirs.json`，声明"本文件夹下的项目可额外引用哪些目录"：

```json
{
  "refs": ["project-core", "../shared-docs", "~/codes/common"]
}
```

规则：

- 路径**相对配置文件所在文件夹**解析；`~` 展开为 home；绝对路径原样通过。
- 解析器从项目文件夹向上走到 home，合并所有命中的配置：并集 + 去重，父级在前、子级在后。
- 引用目录是叶子目标，不递归展开。
- 要为某个文件夹开启引用，就在那里创建 `.reference-dirs.json`。完整示例见 `examples/.reference-dirs.json.example`。

## 项目结构

```
├── CONTEXT.md                         # 领域术语表
├── SKILL.md                           # skill 定义（agent 读取的步骤说明）
├── docs/adr/                          # 架构决策记录（ADR）
├── examples/
│   └── .reference-dirs.json.example   # 配置示例
├── scripts/
│   └── reference-dirs.py              # 解析器
├── README.md                          # 本文档（中文）
└── README.en.md                       # 英文版
```

## 相关文档

- [CONTEXT.md](CONTEXT.md) — 领域术语定义（引用目录、配置文件、层级合并等）
- [ADR-0001](docs/adr/0001-distributed-config-with-hierarchical-merge.md) — 分布式配置 + 层级合并的设计决策
- [English README](README.en.md) — English version
