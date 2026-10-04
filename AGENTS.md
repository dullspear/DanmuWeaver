# 代码规范

## 导入规则

- `__init__.py` 中使用相对路径（`from .module import xxx`）进行包导入。
- 除 `__init__.py` 外，其余所有文件一律只能使用绝对路径导入（`from src.backend.xxx import yyy`），禁止使用 `from .module import xxx` 或 `from module import xxx` 这类相对/裸导入。

原因：**不是为了防循环依赖**——相对导入和绝对导入在 Python 内部会解析成同一个模块对象，对是否存在循环依赖没有任何影响（循环依赖是模块间依赖结构的问题，要用拆依赖/延迟导入/`TYPE_CHECKING` 守卫解决，和导入语法无关）。用绝对路径的真实理由：
1. 文件可以被单独当脚本运行调试，不依赖"作为包的一部分被 import"这个前提（相对导入脱离包上下文直接跑会报 `attempted relative import with no known parent package`）。
2. 方便 grep／定位引用，不用心算 `.`/`..` 对应哪一层目录，目录层级越深（比如 `algorithms/` 下以后要并排放多个算法）优势越明显。
3. 移动文件时，没改的导入要么还对、要么直接报错，不会出现"路径算错了但恰好还能跑"这种隐蔽错误。
