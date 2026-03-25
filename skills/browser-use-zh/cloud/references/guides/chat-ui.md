# 指南：构建聊天界面

构建一个对话式 UI，用户与 Browser Use 代理聊天并实时观看其工作。

## 目录
- [前置条件](#前置条件)
- [架构](#架构)
- [SDK 设置](#sdk-设置)
- [创建会话](#创建会话)
- [轮询消息](#轮询消息)
- [发送后续消息](#发送后续消息)
- [停止任务](#停止任务)
- [实时浏览器视图](#实时浏览器视图)
- [Python 等效代码](#python-等效代码)
- [SDK 方法汇总](#sdk-方法汇总)

---

## 前置条件

- 你有一个 Web 应用（或正在构建一个）— 下面以 Next.js/React 为例，但 SDK 调用可以从任何后端进行
- 你使用 **Cloud API**，因为需要 `liveUrl` 进行实时浏览器流式传输
- `BROWSER_USE_API_KEY` 来自 https://cloud.browser-use.com/new-api-key

## 架构

两个页面：
1. **首页** — 用户输入任务 → 应用创建空闲会话 → 导航到会话页面 → 分派任务
2. **会话页** — 轮询消息，在 iframe 中显示实时浏览器，让用户发送后续消息

所有 SDK 调用放在一个 API 文件中。核心模式：先创建会话（即时），再分派任务（放弃式），立即导航以便用户在任务启动时看到浏览器。

## SDK 设置

使用两个 SDK 版本 — v3 用于会话/消息，v2 用于配置文件（尚未在 v3 上）。

```typescript
// api.ts
import { BrowserUse as BrowserUseV3 } from "browser-use-sdk/v3";
import { BrowserUse as BrowserUseV2 } from "browser-use-sdk";

const apiKey = process.env.NEXT_PUBLIC_BROWSER_USE_API_KEY ?? "";
const v3 = new BrowserUseV3({ apiKey });
const v2 = new BrowserUseV2({ apiKey });
```

> **警告：** `NEXT_PUBLIC_` 会将 Key 暴露给浏览器。生产环境中，请将 SDK 调用移到 server actions 或 API 路由中。

## 创建会话

两个函数：一个创建空闲会话，另一个向其中分派任务。

```typescript
// api.ts
export async function createSession(opts: {
  model: string;
  profileId?: string;
  proxyCountryCode?: string;
}) {
  return v3.sessions.create({
    model: opts.model as "bu-mini" | "bu-max",
    keepAlive: true,  // 保持会话打开以便后续消息
    ...(opts.profileId && { profileId: opts.profileId }),
    ...(opts.proxyCountryCode && { proxyCountryCode: opts.proxyCountryCode }),
  });
}

export async function sendTask(sessionId: string, task: string) {
  return v3.sessions.create({ sessionId, task, keepAlive: true });
}
```

### 页面流程 — 放弃式分派实现即时导航

```typescript
// page.tsx
async function handleSend(message: string) {
  // 1. 创建空闲会话
  const session = await createSession({ model });

  // 2. 立即导航（用户在任务分派时看到浏览器）
  router.push(`/session/${session.id}`);

  // 3. 放弃式分派任务
  sendTask(session.id, message).catch(console.error);
}
```

### 填充下拉菜单

```typescript
export async function listProfiles() {
  return v2.profiles.list({ pageSize: 100 });
}

export async function listWorkspaces() {
  return v3.workspaces.list({ pageSize: 100 });
}
```

## 轮询消息

以 1 秒间隔轮询会话状态和消息。遇到终态时停止。

```typescript
// api.ts
export async function getSession(id: string) {
  return v3.sessions.get(id);
}

export async function getMessages(id: string, limit = 100) {
  return v3.sessions.messages(id, { limit });
}
```

### React Query 轮询

```typescript
// session-context.tsx
const TERMINAL = new Set(["stopped", "error", "timed_out"]);

// 每 1 秒轮询会话状态
const { data: session } = useQuery({
  queryKey: ["session", sessionId],
  queryFn: () => api.getSession(sessionId),
  refetchInterval: (query) => {
    const s = query.state.data?.status;
    return s && TERMINAL.has(s) ? false : 1000;
  },
});

const isTerminal = !!session && TERMINAL.has(session.status);
const isActive = !!session && !isTerminal;

// 活跃时每 1 秒轮询消息
const { data: rawResponse } = useQuery({
  queryKey: ["messages", sessionId],
  queryFn: () => api.getMessages(sessionId),
  refetchInterval: isActive ? 1000 : false,
});
```

## 发送后续消息

复用 `sendTask` 配合乐观更新，让消息立即出现：

```typescript
const sendMessage = useCallback(async (task: string) => {
  const tempMsg = {
    id: `opt-${Date.now()}`,
    role: "user",
    content: task,
    createdAt: new Date().toISOString(),
  };
  setOptimistic((prev) => [...prev, tempMsg]);

  try {
    await api.sendTask(sessionId, task);
  } catch (err) {
    setOptimistic((prev) => prev.filter((m) => m.id !== tempMsg.id));
  }
}, [sessionId]);
```

## 停止任务

停止当前任务但保持会话活跃以便后续消息：

```typescript
export async function stopTask(id: string) {
  await v3.sessions.stop(id, { strategy: "task" });
}
```

`strategy: "task"` 仅停止运行中的任务。`strategy: "session"` 会完全销毁沙箱。

## 实时浏览器视图

每个会话都有一个 `liveUrl`。在 iframe 中嵌入 — 无 X-Frame-Options 或 CSP 限制：

```tsx
<iframe
  src={session?.liveUrl}
  width="100%"
  height="720"
  style={{ border: "none" }}
/>
```

实时更新，无需轮询。用户也可以直接通过 iframe 与浏览器交互。

## Python 等效代码

使用 asyncio 轮询的相同模式：

```python
import asyncio
from browser_use_sdk.v3 import AsyncBrowserUse

async def main():
    client = AsyncBrowserUse()

    # 创建会话并分派任务
    session = await client.sessions.create(task="Find the top HN post", keep_alive=True)
    print(f"Live: {session.live_url}")

    # 轮询消息
    seen = set()
    while True:
        s = await client.sessions.get(str(session.id))
        msgs = await client.sessions.messages(str(session.id), limit=100)

        for m in msgs.messages:
            if str(m.id) not in seen:
                seen.add(str(m.id))
                print(f"[{m.role}] {m.data[:200]}")

        if s.status.value in ("idle", "stopped", "error", "timed_out"):
            print(f"\nDone — {s.output}")
            break
        await asyncio.sleep(2)

asyncio.run(main())
```

## SDK 方法汇总

| 方法 | 用途 |
|------|------|
| `v3.sessions.create()` | 创建会话，分派任务 |
| `v3.sessions.get()` | 轮询会话状态 |
| `v3.sessions.messages()` | 获取对话历史 |
| `v3.sessions.stop()` | 停止当前任务 |
| `v3.workspaces.list()` | 填充工作区下拉菜单 |
| `v2.profiles.list()` | 填充配置文件下拉菜单 |

完整源码：[github.com/browser-use/chat-ui-example](https://github.com/browser-use/chat-ui-example)
