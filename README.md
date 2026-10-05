# Onsite Robots.txt Checking

独立的 `onsite-audit-robots` skill，用于检查 10.1–10.7，并生成 Excel。输入网站 URL、已有 Screaming Frog crawl／导出及 run config。

## 与 HTTPS flow 共用配置

沿用 HTTPS flow 的连接与运行配置结构，但本仓库模板只包含 robots 适用的字段。共用 `site`、`source`、`mcp`、预算和输出设置；各 flow 分别保留自己的检查设置及 requirements.txt。完整字段分工见 [config.md](references/config.md)。

- 同一 agent 可传入同一份 resolved config，复用 SF crawl、MCP 连接和 AUDIT_PYTHON。
- robots 模板已移除 HTTP/mixed-content/hostname 检查开关和 preferred_origin；整合配置仍可携带这些字段，但由 HTTPS flow 使用。
- 原始证据与 usage.json 可共用；请求/MCP 预算累计，不能每个 flow 重新归零。访问同一 SF 实例须串行。
- `source.allow_new_crawl` 默认 false。发现候选 URL 不自动授权新 crawl；可先生成 URL 清单，复用已有证据或等待 SF 导出。
- robots 临时清单上限 1,000 页、深度 5、候选上限 100、请求每秒 1 次；这些是上限，仍受共用请求预算约束，不保证全部覆盖。
- 不写死用户名、盘符、SF 端口或运行机路径。沿用已有 MCP/runtime 配置，无需建立第二个 server。
- collector 固定复用同一 run/origin 的证据；新采集需要新 run。模板不提供未实现的 force_refresh、TTL、自动重试或连续错误停止开关。
- 空 robots.txt 必须报问题是固定 audit 规则，不再提供 empty_file_is_issue 开关。

## 分工与检查

| 组件 | 负责内容 |
| --- | --- |
| Python | 获取并缓存 robots.txt、提取 sitemap 声明、准备候选 URL、整理证据及生成 Excel |
| Screaming Frog | 实际抓取响应、Googlebot robots 权限、Meta Robots、X-Robots-Tag、canonical、CSS/JS 及渲染证据 |
| Agent | 根据页面内容分类，按预设策略判断，编写 Findings、问题描述与修复方法 |

| Check | 标准 |
| --- | --- |
| 10.1 | 有效 robots.txt；空文件、空白、仅注释必须报问题 |
| 10.2 | sitemap／临时清单中的重要页面可抓取且可访问。Yes 表示没有误挡，避免原问句产生反向含义 |
| 10.3 | 实际确认应限制抓取的 URL 被有效规则阻挡；没有 Disallow 时说明实际情况 |
| 10.4 | 必要 CSS/JS 允许抓取且可访问，明确动态资源覆盖 |
| 10.5 | 候选路径枚举 + 真实链接补充 + 内容验证，按页面类别检查合适策略 |
| 10.6 | 小写 `/robots.txt` 入口有效 |
| 10.7 | robots.txt 包含有效 `Sitemap:` URL 声明 |

10.5 采用 **Are special pages handled appropriately?**：购物车／普通感谢页接受有效 Disallow 或可读取 noindex；后台／私人账户内容必须有授权控制；重复内容按 canonical、重定向或 noindex 判断。公开登录／注册页按约定 SEO 策略检查。不统一要求所有类别 Disallow。

未发现候选不能证明页面不存在。NA 必须写明原因、尝试范围和发现限制。超时、403、缺字段等无法确认时 Result 使用 Needs Review 并解释。SF 的 Non-Indexable 不等于 noindex；忽略 robots 后读到 noindex，不代表 Google 能读取。此 flow 不执行交易、登录私人账户或完整安全扫描。

### 默认／插件规则的边界

robots.txt 中的 add-to-cart、woocommerce 上传目录或日志路径，只作为候选线索，不证明网站有购物车、插件仍启用或敏感文件公开。区分“有规则”“测试 URL 被规则阻挡”“实际页面存在”。只有内容及真实流程证据支持后，才套用对应类别策略。无可验证购物流程时，购物车子项 NA 并写明范围；其他类别仍独立判断。通用规则无实际负面影响，不自动生成 Issue 或建议删除。admin-ajax 的 Allow 也不单独视为后台泄露。详细规则见 [robots-rules.md](references/robots-rules.md)。

## Excel schema

| Sheet | Columns |
| --- | --- |
| Checklist | Check · Result · Findings · Coverage |
| Issues | Issue · Issue Description · How to Fix · Address |

Result 使用 Yes / No / NA / Needs Review；未确认或未执行必须写 Needs Review，不能留空。每个 NA 必须提供原因，每个 No 必须关联具体 issue。Issues 只写确认的问题，单元格内换行列点，Address 每个完整 URL 一行。两张表始终保留。完整输入定义见 [report-schema.md](references/report-schema.md)。

文件名：`{site name}_robots_audit_{YYYY-MM-DD}.xlsx`，日期按用户时区；已有文件不覆盖。

## 使用

将仓库作为 skill 导入，入口是根目录 [SKILL.md](SKILL.md)。默认可自动发现，也可显式调用 `$onsite-audit-robots`。导入 skill 不等于安装 Python 或连接 MCP。安装位置由你的客户端确定；仓库不自动改全局客户端设置。

当前两个 flow 的第三方运行依赖均为 `openpyxl>=3.1,<4`，robots 下载使用 Python 标准库 urllib；因此可共用已验证的 Python 3.9+／venv。各仓库仍独立维护 requirements.txt，未来整合环境安装兼容的依赖并集；版本冲突时使用独立 venv，不直接覆盖既有环境。PyYAML 仅用于 skill 作者校验，不是 audit 运行依赖。

使用已有 AUDIT_PYTHON；没有环境时，在当前执行机创建 venv 并安装 requirements.txt。Windows 使用 `.venv/Scripts/python.exe`，Mac/Linux 使用 `.venv/bin/python`。不要复制其他电脑的 venv。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/test_report.py
.venv/bin/python scripts/test_collect.py
```

复制 config.template.json 到唯一 run 目录并填写实际网站、crawl/export 来源、MCP 与日期。示例（路径需换成实际 run）：

```bash
.venv/bin/python scripts/collect_robots.py --config runs/example/config.json --run-dir runs/example
.venv/bin/python scripts/build_report.py --input runs/example/findings.json --output-dir runs/example --site-name Example --date 2026-10-05
```

collect_robots.py 仅获取 robots 文件及生成候选，不自动验证候选或爬取 sitemap。SF 拉取、页面分类和 findings.json 由执行 agent 完成。需要字段/候选证据但当前工具无法取得时，保留未确认结论，不能补猜结果。

## 验证范围

离线测试使用合成证据，验证分类、候选生成、两张表字段、NA 原因、No/Issues 关联、URL/query 保留、公式注入防护与禁止覆盖。未执行真实网站或 SF MCP 端到端测试，不能把样例当客户 audit。规则依据见 [robots-rules.md](references/robots-rules.md)，本机 MCP 事实以实际工具 schema 为准。
