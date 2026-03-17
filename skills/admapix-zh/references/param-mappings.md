# 参数映射参考表

## 创意类型 (creative_team)

| 用户说（英文） | 用户说（中文） | 代码 | 含义 |
|---|---|---|---|
| image, single image | 图片、单图 | "100" | 单图 |
| double image | 双图 | "200" | 双图 |
| triple image | 三图 | "300" | 三图 |
| multi-image | 多图 | "400" | 多图（3张以上） |
| video | 视频 | "010" | 视频 |
| playable, playable ad | 试玩、试玩广告、playable | "001" | 试玩广告 |
| image + video | 单图+视频 | "110" | 图片+视频组合 |
| double image + video | 双图+视频 | "210" | 双图+视频 |
| video + playable | 视频+试玩 | "011" | 视频+试玩 |
| all images | 所有图片 | ["100","200","300","400"] | 所有图片类型 |

**组合规则：** 三位代码表示"图片数量-视频-试玩"。如 "110" = 1张图 + 视频 + 无试玩。

## 地区 → 国家代码映射

| 地区（英文） | 地区（中文） | 国家代码 |
|---|---|---|
| Southeast Asia | 东南亚 | TH, VN, ID, MY, PH, SG, MM, KH, LA, BN |
| South Asia | 南亚 | IN, PK, BD, LK, NP, BT, MV |
| East Asia | 东亚 | JP, KR, CN, TW, HK, MO |
| Japan & Korea | 日韩 | JP, KR |
| HK/Macau/Taiwan | 港澳台 | HK, MO, TW |
| North America | 北美 | US, CA |
| United States | 美国 | US |
| Europe | 欧洲 | GB, DE, FR, IT, ES, NL, PL, SE, NO, DK, FI, AT, CH, BE, PT, IE, CZ, RO, HU, GR |
| Western Europe | 西欧 | GB, DE, FR, IT, ES, NL, BE, AT, CH, PT, IE |
| Northern Europe | 北欧 | SE, NO, DK, FI, IS |
| Middle East | 中东 | SA, AE, QA, KW, BH, OM, IL, TR, EG, JO, LB, IQ |
| Latin America | 拉美 | BR, MX, AR, CO, CL, PE, VE, EC |
| Africa | 非洲 | ZA, NG, KE, EG, GH, TZ, ET, MA |
| Oceania | 大洋洲 | AU, NZ |
| CIS/Eastern Europe | 独联体/东欧 | RU, UA, KZ, BY, UZ, GE, AZ, AM |
| Global (no filter) | 全球（无需过滤） | 省略 country_ids 参数 |

### 常见单个国家速查

| 国家（英文） | 国家（中文） | 代码 |
|---|---|---|
| United States | 美国 | US |
| United Kingdom | 英国 | GB |
| Japan | 日本 | JP |
| South Korea | 韩国 | KR |
| India | 印度 | IN |
| Brazil | 巴西 | BR |
| Germany | 德国 | DE |
| France | 法国 | FR |
| Indonesia | 印尼 | ID |
| Thailand | 泰国 | TH |
| Vietnam | 越南 | VN |
| Philippines | 菲律宾 | PH |
| Malaysia | 马来西亚 | MY |
| Singapore | 新加坡 | SG |
| Saudi Arabia | 沙特 | SA |
| UAE | 阿联酋 | AE |
| Turkey | 土耳其 | TR |
| Australia | 澳大利亚 | AU |
| Canada | 加拿大 | CA |
| Mexico | 墨西哥 | MX |
| Russia | 俄罗斯 | RU |
| Spain | 西班牙 | ES |
| Italy | 意大利 | IT |
| Netherlands | 荷兰 | NL |
| Poland | 波兰 | PL |
| Egypt | 埃及 | EG |
| South Africa | 南非 | ZA |
| New Zealand | 新西兰 | NZ |

## 排序方式

| 用户说（英文） | 用户说（中文） | sort_field | sort_rule | 含义 |
|---|---|---|---|---|
| newest, by date (default) | 最新、按时间（默认） | "3" | "desc" | 首次发现降序 |
| oldest, date ascending | 最早、时间正序 | "3" | "asc" | 首次发现升序 |
| most relevant, relevance | 最相关、相关性 | "11" | "desc" | 按相关性 |
| most popular, most impressions | 最热、曝光最多 | "15" | "desc" | 预估曝光降序 |
| least impressions | 曝光最少 | "15" | "asc" | 预估曝光升序 |
| longest running | 投放最久、持续时间最长 | "4" | "desc" | 投放天数降序 |
| shortest running | 投放最短 | "4" | "asc" | 投放天数升序 |

## 时间范围计算

| 用户说（英文） | 用户说（中文） | 计算方式 |
|---|---|---|
| last week / last 7 days | 最近一周 / 近7天 | start_date = 今天 - 7天，end_date = 今天 |
| last 2 weeks / last 14 days | 最近两周 / 近14天 | start_date = 今天 - 14天，end_date = 今天 |
| last month / last 30 days (default) | 最近一个月 / 近30天（默认） | start_date = 今天 - 30天，end_date = 今天 |
| last 3 months / last 90 days | 最近三个月 / 近90天 | start_date = 今天 - 90天，end_date = 今天 |
| previous month | 上个月 | start_date = 上月1号，end_date = 上月最后一天 |
| today | 今天 | start_date = end_date = 今天 |
| YYYY-MM-DD ~ YYYY-MM-DD | YYYY-MM-DD ~ YYYY-MM-DD | 使用用户提供的具体日期 |

**日期格式：** YYYY-MM-DD（如 2026-03-10）

## 每页数量

| 用户说（英文） | 用户说（中文） | page_size |
|---|---|---|
| default | 默认 | 20 |
| show more | 多看一些 | 40 |
| maximum | 最多 | 60（上限） |
| show fewer / brief | 少看几条 / 简要 | 10 |
