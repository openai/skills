# 飞书表格公式规则

> 生成或改写飞书电子表格公式时的参考规则。飞书不像 Excel 365 默认 spill，普通公式对区域默认“投影”（只取当前行/列对应的单值），必须显式使用 `ARRAYFORMULA` 或原生数组函数才能逐项展开。

## 写入方式

公式必须使用对象格式写入（参见 SKILL.md「单元格数据类型」）：

```bash
--values '[[{"type":"formula","text":"=SUM(A1:A10)"}]]'
```

## ARRAYFORMULA 判断流程

1. 结果是**标量**（单值）→ 不需要
2. 结果是**数组**，且公式中**有**原生数组函数 → 不需要（数组语义自动传播）
3. 结果是**数组**，且公式中**无**原生数组函数，对区域做标量计算 → 加 `ARRAYFORMULA`

```text
# 有原生数组函数，无需包裹
=FILTER(A2:A10,B2:B10="x")+1          ✓
=XLOOKUP(E2:E10,A2:A10,B2:B10)*100    ✓
=MAP(A2:A10,LAMBDA(x,x*2))-1          ✓

# 无原生数组函数，必须包裹
=ARRAYFORMULA(A2:A100*B2:B100)         ✓
=ARRAYFORMULA(IF(A2:A100>0,B2:B100,""))✓
```

## 原生数组函数清单（无需 ARRAYFORMULA）

`ARRAYFORMULA` `ARRAY_CONSTRAIN` `BYCOL` `BYROW` `CELL` `CHOOSECOLS` `CHOOSEROWS` `DROP` `EXPAND` `FILTER` `FLATTEN` `FREQUENCY` `GROWTH` `HSTACK` `IMPORTDATA` `IMPORTFEED` `IMPORTHTML` `IMPORTRANGE` `IMPORTXML` `LINEST` `LOGEST` `LOOKUP` `MAKEARRAY` `MAP` `MINVERSE` `MMULT` `MUNIT` `QUERY` `RANDARRAY` `REDUCE` `REGEXEXTRACT` `SCAN` `SEQUENCE` `SORT` `SORTBY` `SORTN` `SPLIT` `SUMPRODUCT` `SWITCH` `TAKE` `TEXTSPLIT` `TOCOL` `TOROW` `TRANSPOSE` `TREND` `UNIQUE` `VSTACK` `WRAPCOLS` `WRAPROWS` `XLOOKUP`

## 高风险函数：INDEX / OFFSET / ROW / COLUMN / MATCH

行号/列号/偏移量本身是数组时，必须显式包裹：

```text
=ARRAYFORMULA(INDEX(...))
=ARRAYFORMULA(ROW(...))
```

例外：结果直接交给聚合函数消费时不需要：`=SUM(INDEX(A1:B2,0,1))` ✓

## 隐式逐项求值 → MAP/LAMBDA

Excel 中 `SUBTOTAL`、`INDIRECT`、`OFFSET` 等在 `SUMPRODUCT` 内会隐式逐行求值，飞书不会。用 `MAP` 显式遍历：

```text
# Excel
=SUMPRODUCT(SUBTOTAL(103,INDIRECT("E"&ROW($E$16:$E$387))))

# 飞书
=SUMPRODUCT(MAP(ARRAYFORMULA(ROW($E$16:$E$387)),LAMBDA(r,SUBTOTAL(103,INDIRECT("E"&r)))))
```

同类场景：`SUMIF/COUNTIF/SUMIFS` 的范围参数来自 `INDIRECT/OFFSET` 时也需要 `MAP`。

## 多维结果降维

飞书公式结果只能是二维，不能返回“区域的列表”。合并多个区域时：

| 需求 | 写法 |
|------|------|
| 上下堆叠 | `=VSTACK(a, b, c)` |
| 左右拼接 | `=HSTACK(a, b, c)` |
| 压成单列 | `=TOCOL(...)` |
| 压成单行 | `=TOROW(...)` |
| 归约为标量 | `=REDUCE(init, arr, LAMBDA(acc, x, ...))` |

## 日期差

| 需求 | 正确写法 | 错误写法 |
|------|---------|---------|
| 天数差 | `=DAYS(B2,A2)` 或 `=DATEDIF(A2,B2,"D")` 或 `=B2-A2` | `=DAY(B2-A2)` |
| 月份差 | `=DATEDIF(A2,B2,"M")` | `=MONTH(B2-A2)` |
| 年份差 | `=DATEDIF(A2,B2,"Y")` | `=YEAR(B2-A2)` |
| 工作日差 | `=NETWORKDAYS(A2,B2)` | — |

## 飞书不支持的 Excel 语法

| Excel 语法 | 飞书替代 |
|-----------|---------|
| `=@A1:A10`（隐式交叉） | `=A1:A10`（飞书默认投影，去掉 `@`） |
| `=A1#`（spill range） | 改成明确范围，或用 `TAKE`/`DROP`/`ARRAY_CONSTRAIN` |
| `=SUM(Table1[Amount])`（结构化引用） | `=SUM(A2:A100)`（改为 A1 区域） |
| `{=A1:A10*B1:B10}`（CSE 花括号） | `=ARRAYFORMULA(A1:A10*B1:B10)` |
| `STOCKHISTORY` / `WEBSERVICE` / `CUBE*` | 飞书无等价函数 |
