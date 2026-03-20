---
name: ui-ux-pro-max
description: "UI/UX 设计智能指南，适用于 Web 和移动端。包含 50+ 种风格、161 种配色方案、57 种字体搭配、161 种产品类型、99 条 UX 准则和 25 种图表类型，覆盖 10 大技术栈（React、Next.js、Vue、Svelte、SwiftUI、React Native、Flutter、Tailwind、shadcn/ui 和 HTML/CSS）。支持的操作：规划、构建、创建、设计、实现、审查、修复、改进、优化、增强、重构和检查 UI/UX 代码。项目类型：网站、落地页、仪表盘、管理后台、电商、SaaS、作品集、博客和移动应用。组件元素：按钮、模态框、导航栏、侧边栏、卡片、表格、表单和图表。设计风格：玻璃拟态、粘土拟态、极简主义、野兽派、新拟态、Bento Grid、暗色模式、响应式、拟物化和扁平化设计。涵盖主题：颜色系统、无障碍、动画、布局、排版、字体搭配、间距、交互状态、阴影和渐变。集成：shadcn/ui MCP 用于组件搜索和示例。"
---

# UI/UX Pro Max - 设计智能指南

全面的设计指南，适用于 Web 和移动应用。包含 50+ 种风格、161 种配色方案、57 种字体搭配、161 种带推理规则的产品类型、99 条 UX 准则和 25 种图表类型，覆盖 10 大技术栈。支持搜索的数据库，提供基于优先级的推荐。

## 何时使用

当任务涉及 **UI 结构、视觉设计决策、交互模式或用户体验质量控制** 时，应使用此技能。

### 必须使用

在以下情况下必须调用此技能：

- 设计新页面（落地页、仪表盘、管理后台、SaaS、移动应用）
- 创建或重构 UI 组件（按钮、模态框、表单、表格、图表等）
- 选择配色方案、字体系统、间距标准或布局系统
- 审查 UI 代码的用户体验、无障碍性或视觉一致性
- 实现导航结构、动画或响应式行为
- 做出产品级别的设计决策（风格、信息层级、品牌表达）
- 改善界面的感知质量、清晰度或可用性

### 推荐使用

在以下情况下推荐使用此技能：

- UI 看起来"不够专业"但原因不明确
- 收到关于可用性或体验的反馈
- 发布前的 UI 质量优化
- 跨平台设计对齐（Web / iOS / Android）
- 构建设计系统或可复用组件库

### 无需使用

在以下情况下不需要此技能：

- 纯后端逻辑开发
- 仅涉及 API 或数据库设计
- 与界面无关的性能优化
- 基础设施或 DevOps 工作
- 非可视化脚本或自动化任务

**决策标准**：如果任务会改变功能的 **外观、感觉、动效或交互方式**，则应使用此技能。

## 按优先级排列的规则类别

*供人类/AI 参考：按优先级 1→10 决定首先关注哪个规则类别；需要时使用 `--domain <Domain>` 查询详情。脚本不读取此表。*

| 优先级 | 类别 | 影响 | 领域 | 关键检查（必须有） | 反模式（避免） |
|----------|----------|--------|--------|------------------------|------------------------|
| 1 | 无障碍性 | 关键 | `ux` | 对比度 4.5:1、替代文本、键盘导航、Aria 标签 | 移除焦点环、无标签的纯图标按钮 |
| 2 | 触控与交互 | 关键 | `ux` | 最小尺寸 44×44px、8px+ 间距、加载反馈 | 仅依赖悬停、瞬时状态变化（0ms） |
| 3 | 性能 | 高 | `ux` | WebP/AVIF、懒加载、预留空间（CLS &lt; 0.1） | 布局抖动、累积布局偏移 |
| 4 | 风格选择 | 高 | `style`, `product` | 匹配产品类型、一致性、SVG 图标（不用 emoji） | 随机混合扁平与拟物化、用 emoji 作为图标 |
| 5 | 布局与响应式 | 高 | `ux` | 移动优先断点、Viewport meta、无横向滚动 | 横向滚动、固定 px 容器宽度、禁用缩放 |
| 6 | 排版与颜色 | 中 | `typography`, `color` | 基础 16px、行高 1.5、语义化颜色令牌 | 正文文本 &lt; 12px、灰底灰字、组件中使用原始 hex |
| 7 | 动画 | 中 | `ux` | 持续时间 150–300ms、动效传达意义、空间连续性 | 纯装饰性动画、动画 width/height、无 reduced-motion |
| 8 | 表单与反馈 | 中 | `ux` | 可见标签、错误靠近字段、帮助文本、渐进式披露 | 仅用占位符作标签、错误仅在顶部、一开始就堆砌信息 |
| 9 | 导航模式 | 高 | `ux` | 可预测的返回、底部导航 ≤5 项、深度链接 | 导航过载、返回行为异常、无深度链接 |
| 10 | 图表与数据 | 低 | `chart` | 图例、工具提示、无障碍颜色 | 仅依靠颜色传达意义 |

## 快速参考

### 1. 无障碍性（关键）

- `color-contrast` - 普通文本最小对比度 4.5:1（大文本 3:1）；Material Design
- `focus-states` - 交互元素上可见的焦点环（2–4px；Apple HIG, MD）
- `alt-text` - 有意义的图片需要描述性替代文本
- `aria-labels` - 纯图标按钮使用 aria-label；原生端使用 accessibilityLabel（Apple HIG）
- `keyboard-nav` - Tab 顺序与视觉顺序一致；完整键盘支持（Apple HIG）
- `form-labels` - 使用 label 配合 for 属性
- `skip-links` - 为键盘用户提供跳转到主内容的链接
- `heading-hierarchy` - 顺序使用 h1→h6，不跳级
- `color-not-only` - 不要仅靠颜色传达信息（添加图标/文本）
- `dynamic-type` - 支持系统文字缩放；避免文字增长时被截断（Apple Dynamic Type, MD）
- `reduced-motion` - 尊重 prefers-reduced-motion；请求时减少/禁用动画（Apple Reduced Motion API, MD）
- `voiceover-sr` - 有意义的 accessibilityLabel/accessibilityHint；VoiceOver/屏幕阅读器的逻辑阅读顺序（Apple HIG, MD）
- `escape-routes` - 在模态框和多步骤流程中提供取消/返回选项（Apple HIG）
- `keyboard-shortcuts` - 保留系统和无障碍快捷键；为拖放提供键盘替代方案（Apple HIG）

### 2. 触控与交互（关键）

- `touch-target-size` - 最小 44×44pt（Apple）/ 48×48dp（Material）；必要时扩展点击区域超出视觉边界
- `touch-spacing` - 触控目标之间最小 8px/8dp 间距（Apple HIG, MD）
- `hover-vs-tap` - 使用点击/轻触作为主要交互；不要仅依赖悬停
- `loading-buttons` - 异步操作期间禁用按钮；显示加载指示器或进度
- `error-feedback` - 在问题附近显示清晰的错误消息
- `cursor-pointer` - 为可点击元素添加 cursor-pointer（Web）
- `gesture-conflicts` - 避免在主要内容上使用水平滑动；优先使用垂直滚动
- `tap-delay` - 使用 touch-action: manipulation 减少 300ms 延迟（Web）
- `standard-gestures` - 一致使用平台标准手势；不要重新定义（如滑动返回、捏合缩放）（Apple HIG）
- `system-gestures` - 不要阻止系统手势（控制中心、返回滑动等）（Apple HIG）
- `press-feedback` - 按压时的视觉反馈（波纹/高亮；MD 状态层）
- `haptic-feedback` - 使用触觉反馈确认重要操作；避免过度使用（Apple HIG）
- `gesture-alternative` - 不要仅依赖手势交互；始终为关键操作提供可见控件
- `safe-area-awareness` - 将主要触控目标远离刘海、灵动岛、手势条和屏幕边缘
- `no-precision-required` - 避免需要像素级精确点击的小图标或细边缘
- `swipe-clarity` - 滑动操作必须显示清晰的提示或暗示（箭头、标签、教程）
- `drag-threshold` - 在开始拖动前使用移动阈值以避免意外拖动

### 3. 性能（高）

- `image-optimization` - 使用 WebP/AVIF、响应式图片（srcset/sizes）、懒加载非关键资源
- `image-dimension` - 声明 width/height 或使用 aspect-ratio 防止布局偏移（Core Web Vitals: CLS）
- `font-loading` - 使用 font-display: swap/optional 避免不可见文本（FOIT）；预留空间减少布局偏移（MD）
- `font-preload` - 仅预加载关键字体；避免在每个变体上过度使用预加载
- `critical-css` - 优先处理首屏 CSS（内联关键 CSS 或提前加载样式表）
- `lazy-loading` - 通过动态导入/路由级分割懒加载非核心组件
- `bundle-splitting` - 按路由/功能分割代码（React Suspense / Next.js dynamic）以减少初始加载和 TTI
- `third-party-scripts` - 异步/延迟加载第三方脚本；审查并移除不必要的脚本（MD）
- `reduce-reflows` - 避免频繁的布局读取/写入；批量 DOM 读取然后写入
- `content-jumping` - 为异步内容预留空间以避免布局跳动（Core Web Vitals: CLS）
- `lazy-load-below-fold` - 对首屏以下的图片和重型媒体使用 loading="lazy"
- `virtualize-lists` - 对 50+ 项的列表进行虚拟化以提高内存效率和滚动性能
- `main-thread-budget` - 每帧工作保持在 ~16ms 以内以实现 60fps；将繁重任务移出主线程（HIG, MD）
- `progressive-loading` - 对超过 1 秒的操作使用骨架屏/闪烁效果而非长时间阻塞的加载指示器（Apple HIG）
- `input-latency` - 点击/滚动的输入延迟保持在 ~100ms 以内（Material 响应性标准）
- `tap-feedback-speed` - 在点击后 100ms 内提供视觉反馈（Apple HIG）
- `debounce-throttle` - 对高频事件（滚动、调整大小、输入）使用防抖/节流
- `offline-support` - 提供离线状态消息和基本回退（PWA / 移动端）
- `network-fallback` - 为慢速网络提供降级模式（低分辨率图片、更少动画）

### 4. 风格选择（高）

- `style-match` - 将风格与产品类型匹配（使用 `--design-system` 获取推荐）
- `consistency` - 所有页面使用相同风格
- `no-emoji-icons` - 使用 SVG 图标（Heroicons、Lucide），不用 emoji
- `color-palette-from-product` - 从产品/行业选择配色方案（搜索 `--domain color`）
- `effects-match-style` - 阴影、模糊、圆角与所选风格对齐（玻璃 / 扁平 / 粘土等）
- `platform-adaptive` - 尊重平台惯例（iOS HIG vs Material）：导航、控件、排版、动效
- `state-clarity` - 使悬停/按下/禁用状态在视觉上明显区分，同时保持风格一致（Material 状态层）
- `elevation-consistent` - 对卡片、抽屉、模态框使用一致的高度/阴影层级；避免随机阴影值
- `dark-mode-pairing` - 同时设计浅色/深色变体以保持品牌、对比度和风格一致
- `icon-style-consistent` - 整个产品使用一套图标集/视觉语言（描边宽度、圆角）
- `system-controls` - 优先使用原生/系统控件而非完全自定义；仅在品牌需要时自定义（Apple HIG）
- `blur-purpose` - 使用模糊表示背景消失（模态框、抽屉），而非作为装饰（Apple HIG）
- `primary-action` - 每个屏幕应该只有一个主要 CTA；次要操作在视觉上从属（Apple HIG）

### 5. 布局与响应式（高）

- `viewport-meta` - width=device-width initial-scale=1（永远不要禁用缩放）
- `mobile-first` - 移动优先设计，然后扩展到平板和桌面
- `breakpoint-consistency` - 使用系统性断点（如 375 / 768 / 1024 / 1440）
- `readable-font-size` - 移动端正文文本最小 16px（避免 iOS 自动缩放）
- `line-length-control` - 移动端每行 35–60 个字符；桌面端 60–75 个字符
- `horizontal-scroll` - 移动端无横向滚动；确保内容适合视口宽度
- `spacing-scale` - 使用 4pt/8dp 增量间距系统（Material Design）
- `touch-density` - 保持组件间距对触控友好：不太拥挤，也不导致误触
- `container-width` - 桌面端使用一致的最大宽度（max-w-6xl / 7xl）
- `z-index-management` - 定义分层 z-index 层级（如 0 / 10 / 20 / 40 / 100 / 1000）
- `fixed-element-offset` - 固定导航栏/底栏必须为底层内容预留安全边距
- `scroll-behavior` - 避免干扰主滚动体验的嵌套滚动区域
- `viewport-units` - 移动端优先使用 min-h-dvh 而非 100vh
- `orientation-support` - 保持横向模式下布局可读和可操作
- `content-priority` - 移动端优先显示核心内容；折叠或隐藏次要内容
- `visual-hierarchy` - 通过大小、间距、对比度建立层级 —— 而非仅靠颜色

### 6. 排版与颜色（中）

- `line-height` - 正文文本使用 1.5-1.75
- `line-length` - 限制每行 65-75 个字符
- `font-pairing` - 匹配标题/正文字体个性
- `font-scale` - 一致的字体比例（如 12 14 16 18 24 32）
- `contrast-readability` - 浅色背景使用深色文本（如白色上的 slate-900）
- `text-styles-system` - 使用平台字体系统：iOS 11 Dynamic Type 样式 / Material 5 字体角色（display、headline、title、body、label）（HIG, MD）
- `weight-hierarchy` - 使用 font-weight 强化层级：粗体标题（600–700）、常规正文（400）、中等标签（500）（MD）
- `color-semantic` - 定义语义化颜色令牌（primary、secondary、error、surface、on-surface），组件中不使用原始 hex（Material 颜色系统）
- `color-dark-mode` - 深色模式使用去饱和/较浅的色调变体，而非反转颜色；单独测试对比度（HIG, MD）
- `color-accessible-pairs` - 前景/背景配对必须满足 4.5:1（AA）或 7:1（AAA）；使用工具验证（WCAG, MD）
- `color-not-decorative-only` - 功能性颜色（错误红、成功绿）必须包含图标/文本；避免仅靠颜色传达意义（HIG, MD）
- `truncation-strategy` - 优先换行而非截断；截断时使用省略号并通过工具提示/展开提供完整文本（Apple HIG）
- `letter-spacing` - 尊重每个平台的默认字间距；避免正文文本使用紧凑字距（HIG, MD）
- `number-tabular` - 数据列、价格和计时器使用等宽数字以防止布局偏移
- `whitespace-balance` - 有意使用空白分组相关项目并分隔部分；避免视觉混乱（Apple HIG）

### 7. 动画（中）

- `duration-timing` - 微交互使用 150–300ms；复杂过渡 ≤400ms；避免 >500ms（MD）
- `transform-performance` - 仅使用 transform/opacity；避免动画 width/height/top/left
- `loading-states` - 加载超过 300ms 时显示骨架或进度指示器
- `excessive-motion` - 每个视图最多动画 1-2 个关键元素
- `easing` - 进入使用 ease-out，退出使用 ease-in；UI 过渡避免线性
- `motion-meaning` - 每个动画必须表达因果关系，而非仅作装饰（Apple HIG）
- `state-transition` - 状态变化（悬停 / 激活 / 展开 / 折叠 / 模态）应该平滑动画，而非突然
- `continuity` - 页面/屏幕过渡应保持空间连续性（共享元素、方向性滑动）（Apple HIG）
- `parallax-subtle` - 谨慎使用视差；必须尊重 reduced-motion 且不引起眩晕（Apple HIG）
- `spring-physics` - 优先使用弹性/物理曲线而非线性或 cubic-bezier 以获得自然感觉（Apple HIG 流体动画）
- `exit-faster-than-enter` - 退出动画比进入短（约进入持续时间的 60–70%）以感觉响应（MD 动效）
- `stagger-sequence` - 列表/网格项入场按每项 30–50ms 错开；避免同时或过慢显示（MD）
- `shared-element-transition` - 屏幕间使用共享元素/英雄过渡实现视觉连续性（MD, HIG）
- `interruptible` - 动画必须可中断；用户点击/手势立即取消进行中的动画（Apple HIG）
- `no-blocking-animation` - 动画期间永远不要阻止用户输入；UI 必须保持可交互（Apple HIG）
- `fade-crossfade` - 同一容器内的内容替换使用交叉淡入淡出（MD）
- `scale-feedback` - 可点击的卡片/按钮按压时微妙缩放（0.95–1.05）；释放时恢复（HIG, MD）
- `gesture-feedback` - 拖动、滑动和捏合必须提供跟随手指的实时视觉响应（MD Motion）
- `hierarchy-motion` - 使用 translate/scale 方向表达层级：从下方进入 = 更深，向上退出 = 返回（MD）
- `motion-consistency` - 全局统一持续时间/缓动令牌；所有动画共享相同的节奏和感觉
- `opacity-threshold` - 淡入淡出元素不应停留在 opacity 0.2 以下；要么完全淡出要么保持可见
- `modal-motion` - 模态框/抽屉应该从触发源动画（缩放+淡入或滑入）以提供空间上下文（HIG, MD）
- `navigation-direction` - 前进导航向左/上动画；后退向右/下 —— 保持方向逻辑一致（HIG）
- `layout-shift-avoid` - 动画不得引起布局重排或 CLS；位置变化使用 transform

### 8. 表单与反馈（中）

- `input-labels` - 每个输入有可见标签（非仅占位符）
- `error-placement` - 在相关字段下方显示错误
- `submit-feedback` - 提交时显示加载然后成功/错误状态
- `required-indicators` - 标记必填字段（如星号）
- `empty-states` - 无内容时显示有用的消息和操作
- `toast-dismiss` - 3-5 秒后自动关闭 toast
- `confirmation-dialogs` - 破坏性操作前确认
- `input-helper-text` - 在复杂输入下方提供持久的帮助文本，而非仅占位符（Material Design）
- `disabled-states` - 禁用元素使用降低的不透明度（0.38–0.5）+ 光标变化 + 语义属性（MD）
- `progressive-disclosure` - 渐进式揭示复杂选项；不要一开始就压倒用户（Apple HIG）
- `inline-validation` - 在失焦时验证（而非按键）；仅在用户完成输入后显示错误（MD）
- `input-type-keyboard` - 使用语义化输入类型（email、tel、number）触发正确的移动键盘（HIG, MD）
- `password-toggle` - 为密码字段提供显示/隐藏切换（MD）
- `autofill-support` - 使用 autocomplete / textContentType 属性以便系统自动填充（HIG, MD）
- `undo-support` - 允许对破坏性或批量操作撤销（如"撤销删除" toast）（Apple HIG）
- `success-feedback` - 用简短的视觉反馈确认已完成的操作（勾选、toast、颜色闪烁）（MD）
- `error-recovery` - 错误消息必须包含清晰的恢复路径（重试、编辑、帮助链接）（HIG, MD）
- `multi-step-progress` - 多步骤流程显示步骤指示器或进度条；允许返回导航（MD）
- `form-autosave` - 长表单应该自动保存草稿以防止意外关闭导致数据丢失（Apple HIG）
- `sheet-dismiss-confirm` - 关闭有未保存更改的抽屉/模态框前确认（Apple HIG）
- `error-clarity` - 错误消息必须说明原因 + 如何修复（而非仅"输入无效"）（HIG, MD）
- `field-grouping` - 逻辑分组相关字段（fieldset/legend 或视觉分组）（MD）
- `read-only-distinction` - 只读状态应该在视觉和语义上与禁用状态不同（MD）
- `focus-management` - 提交错误后，自动聚焦第一个无效字段（WCAG, MD）
- `error-summary` - 对于多个错误，在顶部显示摘要并带有指向每个字段的锚链接（WCAG）
- `touch-friendly-input` - 移动端输入高度 ≥44px 以满足触控目标要求（Apple HIG）
- `destructive-emphasis` - 破坏性操作使用语义化危险颜色（红色）并与主要操作视觉分离（HIG, MD）
- `toast-accessibility` - Toast 不得抢夺焦点；使用 aria-live="polite" 进行屏幕阅读器通知（WCAG）
- `aria-live-errors` - 表单错误使用 aria-live 区域或 role="alert" 通知屏幕阅读器（WCAG）
- `contrast-feedback` - 错误和成功状态颜色必须满足 4.5:1 对比度（WCAG, MD）
- `timeout-feedback` - 请求超时必须显示清晰的反馈并提供重试选项（MD）

### 9. 导航模式（高）

- `bottom-nav-limit` - 底部导航最多 5 项；使用带标签的图标（Material Design）
- `drawer-usage` - 使用抽屉/侧边栏作为次要导航，而非主要操作（Material Design）
- `back-behavior` - 返回导航必须可预测且一致；保留滚动/状态（Apple HIG, MD）
- `deep-linking` - 所有关键屏幕必须可通过深度链接 / URL 访问以便分享和通知（Apple HIG, MD）
- `tab-bar-ios` - iOS：使用底部 Tab Bar 进行顶级导航（Apple HIG）
- `top-app-bar-android` - Android：使用带导航图标的 Top App Bar 作为主要结构（Material Design）
- `nav-label-icon` - 导航项必须同时有图标和文本标签；纯图标导航损害可发现性（MD）
- `nav-state-active` - 当前位置必须在导航中视觉高亮（颜色、粗细、指示器）（HIG, MD）
- `nav-hierarchy` - 主要导航（标签/底栏）与次要导航（抽屉/设置）必须清晰分离（MD）
- `modal-escape` - 模态框和抽屉必须提供清晰的关闭/取消方式；移动端支持下滑关闭（Apple HIG）
- `search-accessible` - 搜索必须易于访问（顶栏或标签）；提供最近/建议查询（MD）
- `breadcrumb-web` - Web：对于 3+ 层级深度使用面包屑帮助定位（MD）
- `state-preservation` - 返回导航必须恢复之前的滚动位置、过滤状态和输入（HIG, MD）
- `gesture-nav-support` - 支持系统手势导航（iOS 滑动返回、Android 预测返回）而不冲突（HIG, MD）
- `tab-badge` - 谨慎使用导航项徽章表示未读/待处理；用户访问后清除（HIG, MD）
- `overflow-menu` - 当操作超过可用空间时，使用溢出/更多菜单而非挤在一起（MD）
- `bottom-nav-top-level` - 底部导航仅用于顶级屏幕；永远不要在其中嵌套子导航（MD）
- `adaptive-navigation` - 大屏幕（≥1024px）优先使用侧边栏；小屏幕使用底部/顶部导航（Material Adaptive）
- `back-stack-integrity` - 永远不要静默重置导航栈或意外跳转到首页（HIG, MD）
- `navigation-consistency` - 导航位置在所有页面必须保持相同；不要按页面类型改变
- `avoid-mixed-patterns` - 不要在同一层级混合使用 Tab + Sidebar + Bottom Nav
- `modal-vs-navigation` - 模态框不得用于主要导航流程；它们会打断用户路径（HIG）
- `focus-on-route-change` - 页面过渡后，将焦点移至主内容区域供屏幕阅读器用户（WCAG）
- `persistent-nav` - 核心导航必须从深层页面可达；不要在子流程中完全隐藏（HIG, MD）
- `destructive-nav-separation` - 危险操作（删除账户、登出）必须与普通导航项视觉和空间分离（HIG, MD）
- `empty-nav-state` - 当导航目标不可用时，解释原因而非静默隐藏（MD）

### 10. 图表与数据（低）

- `chart-type` - 将图表类型与数据类型匹配（趋势 → 折线图、比较 → 柱状图、比例 → 饼图/环形图）
- `color-guidance` - 使用无障碍配色方案；避免仅使用红/绿配对供色盲用户（WCAG, MD）
- `data-table` - 为无障碍提供表格替代方案；仅图表对屏幕阅读器不友好（WCAG）
- `pattern-texture` - 用图案、纹理或形状补充颜色，使数据在没有颜色的情况下也可区分（WCAG, MD）
- `legend-visible` - 始终显示图例；位置靠近图表，而非分离在滚动折叠下方（MD）
- `tooltip-on-interact` - 在悬停（Web）或点击（移动端）时提供工具提示/数据标签显示精确值（HIG, MD）
- `axis-labels` - 用单位和可读比例标注轴；避免移动端标签截断或旋转
- `responsive-chart` - 图表必须在小屏幕上重排或简化（如水平柱而非垂直、更少的刻度）
- `empty-data-state` - 无数据时显示有意义的空状态（"暂无数据" + 指引），而非空白图表（MD）
- `loading-chart` - 图表数据加载时使用骨架或闪烁占位符；不要显示空坐标轴框架
- `animation-optional` - 图表入场动画必须尊重 prefers-reduced-motion；数据应该立即可读（HIG）
- `large-dataset` - 对于 1000+ 数据点，聚合或采样；提供下钻详情而非渲染全部（MD）
- `number-formatting` - 在轴和标签上使用本地化感知的数字、日期、货币格式（HIG, MD）
- `touch-target-chart` - 交互式图表元素（点、段）必须有 ≥44pt 点击区域或在触摸时扩展（Apple HIG）
- `no-pie-overuse` - 超过 5 个类别避免饼图/环形图；切换到柱状图以清晰
- `contrast-data` - 数据线/柱与背景对比度 ≥3:1；数据文本标签 ≥4.5:1（WCAG）
- `legend-interactive` - 图例应该可点击以切换系列可见性（MD）
- `direct-labeling` - 对于小数据集，直接在图表上标注值以减少眼球移动
- `tooltip-keyboard` - 工具提示内容必须可通过键盘访问，不依赖悬停（WCAG）
- `sortable-table` - 数据表必须支持排序，使用 aria-sort 指示当前排序状态（WCAG）
- `axis-readability` - 轴刻度不得拥挤；保持可读间距，小屏幕自动跳过
- `data-density` - 限制每张图表的信息密度以避免认知过载；需要时拆分为多张图表
- `trend-emphasis` - 强调数据趋势而非装饰；避免遮挡数据的重渐变/阴影
- `gridline-subtle` - 网格线应该低对比度（如 gray-200）以便不与数据竞争
- `focusable-elements` - 交互式图表元素（点、柱、扇区）必须可通过键盘导航（WCAG）
- `screen-reader-summary` - 为屏幕阅读器提供描述图表关键洞察的文本摘要或 aria-label（WCAG）
- `error-state-chart` - 数据加载失败必须显示带重试操作的错误消息，而非损坏/空白图表
- `export-option` - 对于数据密集型产品，提供图表数据的 CSV/图片导出
- `drill-down-consistency` - 下钻交互必须保持清晰的返回路径和层级面包屑
- `time-scale-clarity` - 时间序列图表必须清晰标注时间粒度（日/周/月）并允许切换

## 如何使用

使用下面的 CLI 工具搜索特定领域。

---

## 前置条件

检查是否安装了 Python：

```bash
python3 --version || python --version
```

如果未安装 Python，根据用户的操作系统安装：

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## 如何使用此技能

当用户请求以下任何内容时使用此技能：

| 场景 | 触发示例 | 从哪里开始 |
|----------|-----------------|------------|
| **新项目 / 页面** | "构建一个落地页"、"构建一个仪表盘" | 步骤 1 → 步骤 2（设计系统） |
| **新组件** | "创建一个定价卡片"、"添加一个模态框" | 步骤 3（领域搜索：style, ux） |
| **选择风格 / 颜色 / 字体** | "什么风格适合金融科技应用？"、"推荐一个配色方案" | 步骤 2（设计系统） |
| **审查现有 UI** | "审查此页面的 UX 问题"、"检查无障碍性" | 上面的快速参考检查清单 |
| **修复 UI bug** | "按钮悬停有问题"、"加载时布局偏移" | 快速参考 → 相关部分 |
| **改进 / 优化** | "让这更快"、"改善移动体验" | 步骤 3（领域搜索：ux, react） |
| **实现深色模式** | "添加深色模式支持" | 步骤 3（领域：style "dark mode"） |
| **添加图表 / 数据可视化** | "添加一个分析仪表盘图表" | 步骤 3（领域：chart） |
| **技术栈最佳实践** | "React 性能技巧"、"SwiftUI 导航" | 步骤 4（技术栈搜索） |

按以下工作流程操作：

### 步骤 1：分析用户需求

从用户请求中提取关键信息：
- **产品类型**：娱乐（社交、视频、音乐、游戏）、工具（扫描器、编辑器、转换器）、生产力（任务管理器、笔记、日历）或混合
- **目标受众**：C 端消费者用户；考虑年龄段、使用场景（通勤、休闲、工作）
- **风格关键词**：趣味、活力、极简、深色模式、内容优先、沉浸式等
- **技术栈**：React Native（此项目唯一的技术栈）

### 步骤 2：生成设计系统（必需）

**始终从 `--design-system` 开始** 以获取带推理的全面推荐：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<产品类型> <行业> <关键词>" --design-system [-p "项目名称"]
```

此命令：
1. 并行搜索领域（product、style、color、landing、typography）
2. 应用 `ui-reasoning.csv` 中的推理规则选择最佳匹配
3. 返回完整设计系统：模式、风格、颜色、排版、效果
4. 包含要避免的反模式

**示例：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "美容 spa 养生 服务" --design-system -p "宁静 Spa"
```

### 步骤 2b：持久化设计系统（主文件 + 覆盖模式）

要保存设计系统以实现**跨会话的分层检索**，添加 `--persist`：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<查询>" --design-system --persist -p "项目名称"
```

这将创建：
- `design-system/MASTER.md` — 包含所有设计规则的全局真实来源
- `design-system/pages/` — 页面特定覆盖的文件夹

**带页面特定覆盖：**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<查询>" --design-system --persist -p "项目名称" --page "dashboard"
```

这还会创建：
- `design-system/pages/dashboard.md` — 与主文件的页面特定偏差

**分层检索的工作原理：**
1. 构建特定页面（如"结账"）时，首先检查 `design-system/pages/checkout.md`
2. 如果页面文件存在，其规则**覆盖**主文件
3. 如果不存在，则仅使用 `design-system/MASTER.md`

**上下文感知检索提示：**
```
我正在构建 [页面名称] 页面。请阅读 design-system/MASTER.md。
同时检查 design-system/pages/[page-name].md 是否存在。
如果页面文件存在，优先使用其规则。
如果不存在，则仅使用主文件规则。
现在，生成代码...
```

### 步骤 3：用详细搜索补充（按需）

获取设计系统后，使用领域搜索获取额外详情：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<关键词>" --domain <domain> [-n <max_results>]
```

**何时使用详细搜索：**

| 需求 | 领域 | 示例 |
|------|--------|---------|
| 产品类型模式 | `product` | `--domain product "娱乐 社交"` |
| 更多风格选项 | `style` | `--domain style "玻璃拟态 深色"` |
| 配色方案 | `color` | `--domain color "娱乐 活力"` |
| 字体搭配 | `typography` | `--domain typography "趣味 现代"` |
| 图表推荐 | `chart` | `--domain chart "实时 仪表盘"` |
| UX 最佳实践 | `ux` | `--domain ux "动画 无障碍"` |
| 替代字体 | `typography` | `--domain typography "优雅 奢华"` |
| 单个 Google 字体 | `google-fonts` | `--domain google-fonts "无衬线 热门 可变"` |
| 落地页结构 | `landing` | `--domain landing "英雄区 社交证明"` |
| React Native 性能 | `react` | `--domain react "重渲染 memo 列表"` |
| 应用界面无障碍 | `web` | `--domain web "accessibilityLabel 触控 安全区域"` |
| AI 提示词 / CSS 关键词 | `prompt` | `--domain prompt "极简主义"` |

### 步骤 4：技术栈指南（React Native）

获取 React Native 实现特定的最佳实践：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<关键词>" --stack react-native
```

---

## 搜索参考

### 可用领域

| 领域 | 用途 | 示例关键词 |
|--------|---------|------------------|
| `product` | 产品类型推荐 | SaaS、电商、作品集、医疗、美容、服务 |
| `style` | UI 风格、颜色、效果 | 玻璃拟态、极简主义、深色模式、野兽派 |
| `typography` | 字体搭配、Google 字体 | 优雅、趣味、专业、现代 |
| `color` | 按产品类型的配色方案 | saas、ecommerce、healthcare、beauty、fintech、service |
| `landing` | 页面结构、CTA 策略 | 英雄区、英雄中心、推荐、定价、社交证明 |
| `chart` | 图表类型、库推荐 | 趋势、比较、时间线、漏斗、饼图 |
| `ux` | 最佳实践、反模式 | 动画、无障碍、z-index、加载 |
| `google-fonts` | 单个 Google 字体查找 | 无衬线、等宽、日文、可变字体、热门 |
| `react` | React/Next.js 性能 | 瀑布流、打包、suspense、memo、重渲染、缓存 |
| `web` | 应用界面指南（iOS/Android/React Native） | accessibilityLabel、触控目标、安全区域、Dynamic Type |
| `prompt` | AI 提示词、CSS 关键词 | （风格名称） |

### 可用技术栈

| 技术栈 | 重点 |
|-------|-------|
| `react-native` | 组件、导航、列表 |

---

## 示例工作流程

**用户请求：** "制作一个 AI 搜索主页。"

### 步骤 1：分析需求
- 产品类型：工具（AI 搜索引擎）
- 目标受众：寻找快速、智能搜索的 C 端用户
- 风格关键词：现代、极简、内容优先、深色模式
- 技术栈：React Native

### 步骤 2：生成设计系统（必需）

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "AI 搜索 工具 现代 极简" --design-system -p "AI 搜索"
```

**输出：** 完整的设计系统，包含模式、风格、颜色、排版、效果和反模式。

### 步骤 3：用详细搜索补充（按需）

```bash
# 获取现代工具产品的风格选项
python3 skills/ui-ux-pro-max/scripts/search.py "极简主义 深色模式" --domain style

# 获取搜索交互和加载的 UX 最佳实践
python3 skills/ui-ux-pro-max/scripts/search.py "搜索 加载 动画" --domain ux
```

### 步骤 4：技术栈指南

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "列表 性能 导航" --stack react-native
```

**然后：** 综合设计系统 + 详细搜索并实现设计。

---

## 输出格式

`--design-system` 标志支持两种输出格式：

```bash
# ASCII 框（默认）- 最适合终端显示
python3 skills/ui-ux-pro-max/scripts/search.py "金融科技 加密" --design-system

# Markdown - 最适合文档
python3 skills/ui-ux-pro-max/scripts/search.py "金融科技 加密" --design-system -f markdown
```

---

## 获得更好结果的技巧

### 查询策略

- 使用**多维关键词** — 组合产品 + 行业 + 调性 + 密度：`"娱乐 社交 活力 内容密集"` 而非仅 `"app"`
- 对同一需求尝试不同关键词：`"趣味 霓虹"` → `"活力 深色"` → `"内容优先 极简"`
- 首先使用 `--design-system` 获取完整推荐，然后对任何不确定的维度使用 `--domain` 深入
- 始终添加 `--stack react-native` 获取实现特定的指导

### 常见问题

| 问题 | 怎么做 |
|---------|---------|
| 无法决定风格/颜色 | 用不同关键词重新运行 `--design-system` |
| 深色模式对比度问题 | 快速参考 §6：`color-dark-mode` + `color-accessible-pairs` |
| 动画感觉不自然 | 快速参考 §7：`spring-physics` + `easing` + `exit-faster-than-enter` |
| 表单 UX 差 | 快速参考 §8：`inline-validation` + `error-clarity` + `focus-management` |
| 导航感觉混乱 | 快速参考 §9：`nav-hierarchy` + `bottom-nav-limit` + `back-behavior` |
| 小屏幕布局错乱 | 快速参考 §5：`mobile-first` + `breakpoint-consistency` |
| 性能 / 卡顿 | 快速参考 §3：`virtualize-lists` + `main-thread-budget` + `debounce-throttle` |

### 交付前检查清单

- 实现 before 运行 `--domain ux "动画 无障碍 z-index 加载"` 作为 UX 验证
- 作为最终审查运行快速参考 **§1–§3**（关键 + 高）
- 在 375px（小手机）和横向方向测试
- 验证启用 **reduced-motion** 和 **Dynamic Type** 最大尺寸时的行为
- 独立检查深色模式对比度（不要假设浅色模式值有效）
- 确认所有触控目标 ≥44pt 且没有内容隐藏在安全区域后面

---

## 专业 UI 的通用规则

这些是经常被忽视的使 UI 看起来不专业的问题：
范围说明：以下规则适用于应用 UI（iOS/Android/React Native/Flutter），而非桌面 Web 交互模式。

### 图标与视觉元素

| 规则 | 标准 | 避免 | 为什么重要 |
|------|----------|--------|----------------|
| **不用 Emoji 作为结构图标** | 使用矢量图标（如 Lucide、react-native-vector-icons、@expo/vector-icons）。 | 使用 emoji（🎨 🚀 ⚙️）作为导航、设置或系统控件。 | Emoji 依赖字体，跨平台不一致，无法通过设计令牌控制。 |
| **仅矢量资源** | 使用 SVG 或平台矢量图标，可干净缩放并支持主题化。 | 会模糊或像素化的栅格 PNG 图标。 | 确保可扩展性、清晰渲染和深色/浅色模式适应性。 |
| **稳定的交互状态** | 使用颜色、不透明度或高度过渡作为按压状态，不改变布局边界。 | 移动周围内容或触发视觉抖动的布局偏移变换。 | 防止不稳定交互并保持移动端流畅动效/感知质量。 |
| **正确的品牌 Logo** | 使用官方品牌资源并遵循其使用指南（间距、颜色、留白）。 | 猜测 Logo 路径、非官方重新着色或修改比例。 | 防止品牌误用并确保法律/平台合规。 |
| **一致的图标大小** | 将图标大小定义为设计令牌（如 icon-sm、icon-md = 24pt、icon-lg）。 | 随机混合任意值如 20pt / 24pt / 28pt。 | 在整个界面中保持节奏和视觉层级。 |
| **描边一致性** | 在同一视觉层级内使用一致的描边宽度（如 1.5px 或 2px）。 | 任意混合粗细描边样式。 | 不一致的描边降低感知精致度和凝聚力。 |
| **填充 vs 轮廓纪律** | 每个层级使用一种图标风格。 | 在同一层级混合填充和轮廓图标。 | 保持语义清晰和风格连贯。 |
| **触控目标最小值** | 最小 44×44pt 交互区域（如果图标更小则使用 hitSlop）。 | 没有扩展点击区域的小图标。 | 满足无障碍和平台可用性标准。 |
| **图标对齐** | 将图标对齐到文本基线并保持一致的填充。 | 图标错位或周围间距不一致。 | 防止降低感知质量的微妙视觉不平衡。 |
| **图标对比度** | 遵循 WCAG 对比度标准：小元素 4.5:1，较大 UI 图标最小 3:1。 | 融入背景的低对比度图标。 | 确保浅色和深色模式下的无障碍性。 |


### 交互（应用）

| 规则 | 做 | 不 |
|------|----|----- |
| **点击反馈** | 在 80-150ms 内提供清晰的按压反馈（波纹/不透明度/高度） | 点击时无视觉响应 |
| **动画时机** | 使用平台原生缓动保持微交互约 150-300ms | 瞬时过渡或慢动画（>500ms） |
| **无障碍焦点** | 确保屏幕阅读器焦点顺序与视觉顺序一致且标签具有描述性 | 未标记的控件或混乱的焦点遍历 |
| **禁用状态清晰度** | 使用禁用语义（`disabled`/原生禁用 props）、降低强调且无点击动作 | 看起来可点击但什么都不做的控件 |
| **触控目标最小值** | 保持点击区域 >=44x44pt（iOS）或 >=48x48dp（Android），图标较小时扩展点击区域 | 微小的点击目标或没有填充的仅图标点击区域 |
| **手势冲突预防** | 每个区域保持一个主要手势并避免嵌套点击/拖动冲突 | 导致意外操作的重叠手势 |
| **语义原生控件** | 优先使用原生交互原语（`Button`、`Pressable`、平台等效物）并具有正确的无障碍角色 | 用作主要控件但没有语义的通用容器 |

### 浅色/深色模式对比度

| 规则 | 做 | 不 |
|------|----|----- |
| **表面可读性（浅色）** | 保持卡片/表面与背景清晰分离，具有足够的不透明度/高度 | 过度透明的表面模糊层级 |
| **文本对比度（浅色）** | 保持正文文本与浅色表面的对比度 >=4.5:1 | 低对比度灰色正文文本 |
| **文本对比度（深色）** | 在深色表面保持主要文本对比度 >=4.5:1，次要文本 >=3:1 | 深色模式文本融入背景 |
| **边框和分隔线可见性** | 确保分隔线在两个主题中都可见（不仅仅是浅色模式） | 主题特定的边框在一个模式中消失 |
| **状态对比度对等** | 在浅色和深色主题中保持按压/聚焦/禁用状态同样可区分 | 仅为一个主题定义交互状态 |
| **令牌驱动主题化** | 在应用表面/文本/图标上使用每个主题映射的语义颜色令牌 | 每个屏幕硬编码的十六进制值 |
| **遮罩和模态可读性** | 使用足够强的模态遮罩隔离前景内容（通常 40-60% 黑色） | 弱遮罩让背景视觉竞争 |

### 布局与间距

| 规则 | 做 | 不 |
|------|----|----- |
| **安全区域合规** | 尊重所有固定页眉、标签栏和 CTA 栏的顶部/底部安全区域 | 将固定 UI 放置在刘海、状态栏或手势区域下 |
| **系统栏间隙** | 为状态/导航栏和手势主指示器添加间距 | 让可点击内容与 OS 边框碰撞 |
| **一致的内容宽度** | 每个设备类别保持可预测的内容宽度（手机/平板） | 在屏幕之间混合任意宽度 |
| **8dp 间距节奏** | 对填充/间隙/部分间距使用一致的 4/8dp 间距系统 | 没有节奏的随机间距增量 |
| **可读文本度量** | 在大设备上保持长文本可读（避免平板上边缘到边缘的段落） | 伤害可读性的全宽长文本 |
| **部分间距层级** | 按层级定义清晰的垂直节奏层级（如 16/24/32/48） | 具有不一致间距的相似 UI 层级 |
| **按断点自适应边距** | 在较大宽度和横向上增加水平内边距 | 在所有设备大小/方向上使用相同的窄边距 |
| **滚动和固定元素共存** | 添加底部/顶部内容内边距，使列表不被固定栏隐藏 | 滚动内容被粘性页眉/页脚遮挡 |

---

## 交付前检查清单

在交付 UI 代码之前，验证以下项目：
范围说明：此检查清单适用于应用 UI（iOS/Android/React Native/Flutter）。

### 视觉质量
- [ ] 没有使用 emoji 作为图标（改用 SVG）
- [ ] 所有图标来自一致的图标系列和风格
- [ ] 使用官方品牌资源，比例和留白正确
- [ ] 按压状态视觉不改变布局边界或引起抖动
- [ ] 一致使用语义主题令牌（没有临时的每屏幕硬编码颜色）

### 交互
- [ ] 所有可点击元素提供清晰的按压反馈（波纹/不透明度/高度）
- [ ] 触控目标满足最小尺寸（>=44x44pt iOS，>=48x48dp Android）
- [ ] 微交互时机保持在 150-300ms 范围内，具有原生感觉的缓动
- [ ] 禁用状态视觉清晰且不可交互
- [ ] 屏幕阅读器焦点顺序与视觉顺序一致，交互标签具有描述性
- [ ] 手势区域避免嵌套/冲突交互（点击/拖动/返回滑动冲突）

### 浅色/深色模式
- [ ] 主要文本对比度在浅色和深色模式下均 >=4.5:1
- [ ] 次要文本对比度在浅色和深色模式下均 >=3:1
- [ ] 分隔线/边框和交互状态在两个模式中都可区分
- [ ] 模态/抽屉遮罩不透明度足够强以保持前景可读性（通常 40-60% 黑色）
- [ ] 交付前测试两个主题（不是从单一主题推断）

### 布局
- [ ] 页眉、标签栏和底部 CTA 栏遵守安全区域
- [ ] 滚动内容不被固定/粘性栏隐藏
- [ ] 在小手机、大手机和平板上验证（纵向 + 横向）
- [ ] 水平内边距/边距按设备大小和方向正确适应
- [ ] 在组件、部分和页面级别保持 4/8dp 间距节奏
- [ ] 长文本度量在大设备上保持可读（无边缘到边缘段落）

### 无障碍
- [ ] 所有有意义的图片/图标都有无障碍标签
- [ ] 表单字段有标签、提示和清晰的错误消息
- [ ] 颜色不是唯一的指示器
- [ ] 支持 reduced motion 和动态文本大小而不破坏布局
- [ ] 无障碍特征/角色/状态（选中、禁用、展开）正确宣告
