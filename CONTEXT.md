# reference-dirs

一个 OpenCode skill,根据当前打开项目所在文件夹,决定该项目可以额外引用的目录列表,供 agent 读取参考。

## Language

**引用目录 (reference dir)**:
当前项目可额外读取参考的目录,由配置文件声明。只读参考,不递归展开。
_Avoid_: 依赖目录, 关联目录

**配置文件 (.reference-dirs.json)**:
分布式配置文件,声明"本文件夹下的项目可额外引用哪些目录"。
_Avoid_: 映射表, 索引文件

**项目路径 (project path)**:
当前打开的项目目录(即 cwd)。
_Avoid_: 工作区, 根目录

**层级合并 (hierarchical merge)**:
从项目路径向上逐级收集配置文件,所有命中的 `refs` 并集+去重,父级在前、子级在后。
_Avoid_: 覆盖, 就近优先