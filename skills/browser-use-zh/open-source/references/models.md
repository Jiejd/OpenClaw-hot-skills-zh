# 支持的 LLM 模型

## 目录
- [Browser Use（推荐）](#browser-use)
- [Google Gemini](#google-gemini)
- [OpenAI](#openai)
- [Anthropic](#anthropic)
- [Azure OpenAI](#azure-openai)
- [AWS Bedrock](#aws-bedrock)
- [Groq](#groq)
- [OCI（Oracle）](#oci-oracle)
- [Ollama（本地）](#ollama-本地)
- [Vercel AI Gateway](#vercel-ai-gateway)
- [OpenAI 兼容 API](#openai-兼容-api)

---

## Browser Use

专为浏览器自动化优化 — 最高准确率、最快速度、最低 Token 成本。

```python
from browser_use import ChatBrowserUse
llm = ChatBrowserUse()                    # bu-latest（默认）
llm = ChatBrowserUse(model='bu-2-0')      # 高级模型
```

**环境变量：** `BROWSER_USE_API_KEY` — 在 https://cloud.browser-use.com/new-api-key 获取

**模型与定价（每 100 万 Token）：**
| 模型 | 输入 | 缓存 | 输出 |
|------|------|------|------|
| bu-1-0（默认） | $0.20 | $0.02 | $2.00 |
| bu-2-0（高级） | $0.60 | $0.06 | $3.50 |

## Google Gemini

```python
from browser_use import ChatGoogle
llm = ChatGoogle(model="gemini-flash-latest")
```

**环境变量：** `GOOGLE_API_KEY`（在 https://aistudio.google.com/app/u/1/apikey 免费获取）

注意：`GEMINI_API_KEY` 已弃用，请使用 `GOOGLE_API_KEY`。

## OpenAI

```python
from browser_use import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.1-mini")
# 推荐对复杂任务使用 o3
llm = ChatOpenAI(model="o3")
```

**环境变量：** `OPENAI_API_KEY`

支持通过自定义 `base_url` 使用 OpenAI 兼容 API。

## Anthropic

```python
from browser_use import ChatAnthropic
llm = ChatAnthropic(model='claude-sonnet-4-0', temperature=0.0)
```

**环境变量：** `ANTHROPIC_API_KEY`

## Azure OpenAI

```python
from browser_use import ChatAzureOpenAI
llm = ChatAzureOpenAI(
    model="gpt-4o",
    api_version="2025-03-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)
```

**环境变量：** `AZURE_OPENAI_ENDPOINT`、`AZURE_OPENAI_API_KEY`

支持对 `gpt-5.1-codex-mini` 等模型使用 Responses API。

## AWS Bedrock

```python
from browser_use import ChatAWSBedrock
llm = ChatAWSBedrock(model="us.anthropic.claude-sonnet-4-20250514-v1:0", region="us-east-1")

# 或通过 Anthropic 封装
from browser_use import ChatAnthropicBedrock
llm = ChatAnthropicBedrock(model="us.anthropic.claude-sonnet-4-20250514-v1:0", aws_region="us-east-1")
```

**环境变量：** `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`、`AWS_DEFAULT_REGION`

支持通过标准 AWS 凭证链使用配置文件、IAM 角色、SSO。

## Groq

```python
from browser_use import ChatGroq
llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")
```

**环境变量：** `GROQ_API_KEY`

## OCI（Oracle）

```python
from browser_use import ChatOCIRaw
llm = ChatOCIRaw(
    model="meta.llama-3.1-70b-instruct",
    service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
    compartment_id="your-compartment-id",
)
```

需要 `~/.oci/config` 配置。认证类型：`API_KEY`、`INSTANCE_PRINCIPAL`、`RESOURCE_PRINCIPAL`。

## Ollama（本地）

```python
from browser_use import ChatOllama
llm = ChatOllama(model="llama3", num_ctx=32000)
```

需要本地运行 `ollama serve`。使用 `num_ctx` 设置上下文窗口（默认值可能太小）。

## Vercel AI Gateway

通过自动回退代理到多个提供商：

```python
from browser_use import ChatVercel
llm = ChatVercel(
    model='anthropic/claude-sonnet-4',
    provider_options={
        'gateway': {
            'order': ['vertex', 'anthropic'],  # 回退顺序
        }
    },
)
```

**环境变量：** `AI_GATEWAY_API_KEY`（或在 Vercel 上使用 `VERCEL_OIDC_TOKEN`）

## OpenAI 兼容 API

任何提供 OpenAI 兼容端点的提供商都可以通过 `ChatOpenAI` 使用：

### Qwen（阿里云）
```python
llm = ChatOpenAI(model="qwen-vl-max", base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
```
**环境变量：** `ALIBABA_CLOUD`

### ModelScope
```python
llm = ChatOpenAI(model="Qwen/Qwen2.5-VL-72B-Instruct", base_url="https://api-inference.modelscope.cn/v1")
```
**环境变量：** `MODELSCOPE_API_KEY`

### DeepSeek
```python
llm = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com")
```
**环境变量：** `DEEPSEEK_API_KEY`

### Novita
```python
llm = ChatOpenAI(model="deepseek/deepseek-r1", base_url="https://api.novita.ai/v3/openai")
```
**环境变量：** `NOVITA_API_KEY`

### OpenRouter
```python
llm = ChatOpenAI(model="deepseek/deepseek-r1", base_url="https://openrouter.ai/api/v1")
```
**环境变量：** `OPENROUTER_API_KEY`

### Langchain
示例参见 [examples/models/langchain](https://github.com/browser-use/browser-use/tree/main/examples/models/langchain)。
