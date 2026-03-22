#!/usr/bin/env python3
"""
Web Search Plus - 交互式设置向导
==========================================

首次使用时运行（不存在 config.json）来配置提供商和 API 密钥。
创建 config.json 保存你的设置。API 密钥仅存储在本地。

用法：
    python3 scripts/setup.py          # 交互式设置
    python3 scripts/setup.py --reset  # 重置并重新配置
"""

import json
import os
import sys
from pathlib import Path

# 终端输出 ANSI 颜色
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def color(text: str, c: str) -> str:
    """Wrap text in color codes."""
    return f"{c}{text}{Colors.RESET}"

def print_header():
    """Print the setup wizard header."""
    print()
    print(color("╔════════════════════════════════════════════════════════════╗", Colors.CYAN))
    print(color("║          🔍 Web Search Plus - 设置向导                    ║", Colors.CYAN))
    print(color("╚════════════════════════════════════════════════════════════╝", Colors.CYAN))
    print()
    print(color("本向导将帮你配置搜索提供商。", Colors.DIM))
    print(color("API 密钥仅存储在本地的 config.json 中（已 gitignore）。", Colors.DIM))
    print()

def print_provider_info():
    """Print information about each provider."""
    print(color("📚 可用提供商：", Colors.BOLD))
    print()
    
    providers = [
        {
            "name": "Serper",
            "emoji": "🔎",
            "best_for": "Google 结果、购物、本地商家、新闻",
            "free_tier": "2,500 次/月",
            "signup": "https://serper.dev",
            "strengths": ["最快响应时间", "产品价格和规格", "知识图谱", "本地商家数据"]
        },
        {
            "name": "Tavily", 
            "emoji": "📖",
            "best_for": "研究、解释、深度分析",
            "free_tier": "1,000 次/月",
            "signup": "https://tavily.com",
            "strengths": ["AI 合成回答", "完整页面内容", "域名过滤", "学术研究"]
        },
        {
            "name": "Exa",
            "emoji": "🧠",
            "best_for": "语义搜索、查找相似内容、发现",
            "free_tier": "1,000 次/月", 
            "signup": "https://exa.ai",
            "strengths": ["神经/语义理解", "相似页面发现", "创业公司/公司查找", "日期过滤"]
        },
        {
            "name": "You.com",
            "emoji": "🤖",
            "best_for": "RAG 应用、实时资讯、LLM 就绪摘要",
            "free_tier": "有限免费额度",
            "signup": "https://api.you.com",
            "strengths": ["LLM 就绪摘要", "网络 + 新闻合一体", "实时页面爬取", "实时信息"]
        },
        {
            "name": "SearXNG",
            "emoji": "🔒",
            "best_for": "隐私优先搜索、多源聚合、$0 API 费用",
            "free_tier": "免费（自托管）",
            "signup": "https://docs.searxng.org/admin/installation.html",
            "strengths": ["保护隐私（无追踪）", "70+ 搜索引擎", "自托管 = $0 API 费用", "多元结果"]
        }
    ]
    
    for p in providers:
        print(f"  {p['emoji']} {color(p['name'], Colors.BOLD)}")
        print(f"     擅长：{color(p['best_for'], Colors.GREEN)}")
        print(f"     免费额度：{p['free_tier']}")
        print(f"     注册：{color(p['signup'], Colors.BLUE)}")
        print()

def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """Ask a yes/no question."""
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        response = input(f"{prompt} {color(suffix, Colors.DIM)}: ").strip().lower()
        if response == "":
            return default
        if response in ("y", "yes", "是", "确定"):
            return True
        if response in ("n", "no", "否", "不"):
            return False
        print(color("  请输入 'y' 或 'n'", Colors.YELLOW))

def ask_choice(prompt: str, options: list, default: str = None) -> str:
    """Ask user to choose from a list of options."""
    print(f"\n{prompt}")
    for i, opt in enumerate(options, 1):
        marker = color("→", Colors.GREEN) if opt == default else " "
        print(f"  {marker} {i}. {opt}")
    
    while True:
        hint = f" [默认：{default}]" if default else ""
        response = input(f"输入数字 (1-{len(options)}){color(hint, Colors.DIM)}: ").strip()
        
        if response == "" and default:
            return default
        
        try:
            idx = int(response)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        except ValueError:
            pass
        
        print(color(f"  请输入 1 到 {len(options)} 之间的数字", Colors.YELLOW))

def ask_api_key(provider: str, signup_url: str) -> str:
    """Ask for an API key with validation."""
    print()
    print(f"  {color(f'获取你的 {provider} API 密钥：', Colors.DIM)} {color(signup_url, Colors.BLUE)}")
    
    while True:
        key = input(f"  输入你的 {provider} API 密钥：").strip()
        
        if not key:
            print(color("    ⚠️  未输入密钥。该提供商将被禁用。", Colors.YELLOW))
            return None
        
        # Basic validation
        if len(key) < 10:
            print(color("    ⚠️  密钥似乎太短，请检查后重试。", Colors.YELLOW))
            continue
        
        # Mask key for confirmation
        masked = key[:4] + "..." + key[-4:] if len(key) > 12 else key[:2] + "..."
        print(color(f"    ✓ 密钥已保存：{masked}", Colors.GREEN))
        return key


def ask_searxng_instance(docs_url: str) -> str:
    """Ask for SearXNG instance URL with connection test."""
    print()
    print(f"  {color('SearXNG 需要自托管。你需要自己的实例。', Colors.DIM)}")
    print(f"  {color('搭建指南：', Colors.DIM)} {color(docs_url, Colors.BLUE)}")
    print()
    print(f"  {color('示例 URL：', Colors.DIM)}")
    print(f"    • http://localhost:8080（本地 Docker）")
    print(f"    • https://searx.your-domain.com（自托管）")
    print()
    
    while True:
        url = input(f"  输入你的 SearXNG 实例 URL：").strip()
        
        if not url:
            print(color("    ⚠️  未输入 URL。SearXNG 将被禁用。", Colors.YELLOW))
            return None
        
        # Basic URL validation
        if not url.startswith(("http://", "https://")):
            print(color("    ⚠️  URL 必须以 http:// 或 https:// 开头", Colors.YELLOW))
            continue
        
        # SSRF protection: validate URL before connecting
        try:
            import ipaddress
            import socket
            from urllib.parse import urlparse as _urlparse
            _parsed = _urlparse(url)
            _hostname = _parsed.hostname or ""
            _blocked = {"169.254.169.254", "metadata.google.internal", "metadata.internal"}
            if _hostname in _blocked:
                print(color(f"    ❌ 已阻止：{_hostname} 是云元数据端点。", Colors.RED))
                continue
            if not os.environ.get("SEARXNG_ALLOW_PRIVATE", "").strip() == "1":
                _resolved = socket.getaddrinfo(_hostname, _parsed.port or 80, proto=socket.IPPROTO_TCP)
                for _fam, _t, _p, _cn, _sa in _resolved:
                    _ip = ipaddress.ip_address(_sa[0])
                    if _ip.is_loopback or _ip.is_private or _ip.is_link_local or _ip.is_reserved:
                        print(color(f"    ❌ 已阻止：{_hostname} 解析到私有 IP {_ip}。", Colors.RED))
                        print(color(f"       如确需访问内网，请设置 SEARXNG_ALLOW_PRIVATE=1。", Colors.DIM))
                        raise ValueError("private_ip")
        except ValueError as _ve:
            if str(_ve) == "private_ip":
                continue
            raise
        except socket.gaierror:
            print(color(f"    ❌ 无法解析主机名：{_hostname}", Colors.RED))
            continue

        # Test connection
        print(color(f"    正在测试连接 {url}...", Colors.DIM))
        try:
            import urllib.request
            import urllib.error
            
            test_url = f"{url.rstrip('/')}/search?q=test&format=json"
            req = urllib.request.Request(
                test_url,
                headers={"User-Agent": "ClawdBot-WebSearchPlus/2.5", "Accept": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode("utf-8")
                import json
                result = json.loads(data)
                
                # Check if it looks like SearXNG JSON response
                if "results" in result or "query" in result:
                    print(color(f"    ✓ 连接成功！SearXNG 实例正常工作。", Colors.GREEN))
                    return url.rstrip("/")
                else:
                    print(color(f"    ⚠️  已连接但响应不像是 SearXNG JSON。", Colors.YELLOW))
                    if ask_yes_no("    仍然使用此 URL？", default=False):
                        return url.rstrip("/")
                        
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(color(f"    ⚠️  JSON API 已禁用（403 Forbidden）。", Colors.YELLOW))
                print(color(f"       在 settings.yml 中启用 JSON：search.formats: [html, json]", Colors.DIM))
            else:
                print(color(f"    ⚠️  HTTP 错误：{e.code} {e.reason}", Colors.YELLOW))
            
            if ask_yes_no("    尝试其他 URL？", default=True):
                continue
            return None
            
        except urllib.error.URLError as e:
            print(color(f"    ⚠️  无法访问实例：{e.reason}", Colors.YELLOW))
            if ask_yes_no("    尝试其他 URL？", default=True):
                continue
            return None
            
        except Exception as e:
            print(color(f"    ⚠️  错误：{e}", Colors.YELLOW))
            if ask_yes_no("    尝试其他 URL？", default=True):
                continue
            return None

def ask_result_count() -> int:
    """Ask for default result count."""
    options = ["3（快速、精简）", "5（均衡 - 推荐）", "10（全面）"]
    choice = ask_choice("每次搜索默认返回多少条结果？", options, "5（均衡 - 推荐）")
    
    if "3" in choice:
        return 3
    elif "10" in choice:
        return 10
    return 5

def run_setup(skill_dir: Path, force_reset: bool = False):
    """Run the interactive setup wizard."""
    config_path = skill_dir / "config.json"
    example_path = skill_dir / "config.example.json"
    
    # Check if config already exists
    if config_path.exists() and not force_reset:
        print(color("✓ config.json 已存在！", Colors.GREEN))
        print()
        if not ask_yes_no("是否重新配置？", default=False):
            print(color("设置已取消。你现有的配置未改动。", Colors.DIM))
            return False
        print()
    
    print_header()
    print_provider_info()
    
    # Load example config as base
    if example_path.exists():
        with open(example_path) as f:
            config = json.load(f)
    else:
        config = {
            "defaults": {"provider": "serper", "max_results": 5},
            "auto_routing": {"enabled": True, "fallback_provider": "serper"},
            "serper": {},
            "tavily": {},
            "exa": {}
        }
    
    # Remove any existing API keys from example
    for provider in ["serper", "tavily", "exa"]:
        if provider in config:
            config[provider].pop("api_key", None)
    
    enabled_providers = []
    
    # ===== 第 1 步：选择要启用的提供商 =====
    print(color("─" * 60, Colors.DIM))
    print(color("\n📋 第 1 步：选择你的提供商\n", Colors.BOLD))
    print("选择你要启用的搜索提供商。")
    print(color("（你至少需要一个 API 密钥才能使用本技能）", Colors.DIM))
    print()
    
    providers_info = {
        "serper": ("Serper", "https://serper.dev", "Google 结果、购物、本地"),
        "tavily": ("Tavily", "https://tavily.com", "研究、解释、分析"),
        "exa": ("Exa", "https://exa.ai", "语义搜索、相似内容"),
        "you": ("You.com", "https://api.you.com", "RAG 应用、实时资讯"),
        "searxng": ("SearXNG", "https://docs.searxng.org/admin/installation.html", "隐私优先、自托管、$0 费用")
    }
    
    for provider, (name, url, desc) in providers_info.items():
        print(f"  {color(name, Colors.BOLD)}：{desc}")
        
        # Special handling for SearXNG
        if provider == "searxng":
            print(color("    注意：SearXNG 需要自托管实例（无需 API 密钥）", Colors.DIM))
            if ask_yes_no(f"    你有 SearXNG 实例吗？", default=False):
                instance_url = ask_searxng_instance(url)
                if instance_url:
                    if "searxng" not in config:
                        config["searxng"] = {}
                    config["searxng"]["instance_url"] = instance_url
                    enabled_providers.append(provider)
                else:
                    print(color(f"    → {name} 已禁用（无实例 URL）", Colors.DIM))
            else:
                print(color(f"    → {name} 已跳过（无实例）", Colors.DIM))
        else:
            if ask_yes_no(f"    启用 {name}？", default=True):
                # ===== 第 2 步：为每个启用的提供商配置 API 密钥 =====
                api_key = ask_api_key(name, url)
                if api_key:
                    config[provider]["api_key"] = api_key
                    enabled_providers.append(provider)
                else:
                    print(color(f"    → {name} 已禁用（无 API 密钥）", Colors.DIM))
            else:
                print(color(f"    → {name} 已禁用", Colors.DIM))
        print()
    
    if not enabled_providers:
        print()
        print(color("⚠️  没有启用任何提供商！", Colors.RED))
        print("你至少需要一个 API 密钥才能使用 web-search-plus。")
        print("请获取 API 密钥后再次运行此设置向导。")
        return False
    
    # ===== 第 3 步：默认提供商 =====
    print(color("─" * 60, Colors.DIM))
    print(color("\n⚙️  第 2 步：默认设置\n", Colors.BOLD))
    
    if len(enabled_providers) > 1:
        default_provider = ask_choice(
            "哪个提供商作为通用查询的默认？",
            enabled_providers,
            enabled_providers[0]
        )
    else:
        default_provider = enabled_providers[0]
        print(f"默认提供商：{color(default_provider, Colors.GREEN)}（仅启用了一个）")
    
    config["defaults"]["provider"] = default_provider
    config["auto_routing"]["fallback_provider"] = default_provider
    
    # ===== 第 4 步：自动路由 =====
    print()
    print(color("自动路由", Colors.BOLD) + " 会为每次查询自动选择最佳提供商：")
    print(color("  • 'iPhone 价格' → Serper（购物意图）", Colors.DIM))
    print(color("  • 'TCP 是怎么工作的' → Tavily（研究意图）", Colors.DIM))  
    print(color("  • '类似 Stripe 的公司' → Exa（发现意图）", Colors.DIM))
    print()
    
    auto_routing = ask_yes_no("启用自动路由？", default=True)
    config["auto_routing"]["enabled"] = auto_routing
    
    if not auto_routing:
        print(color(f"  → 所有查询将使用 {default_provider}", Colors.DIM))
    
    # ===== 第 5 步：结果数量 =====
    print()
    max_results = ask_result_count()
    config["defaults"]["max_results"] = max_results
    
    # Set disabled providers
    all_providers = ["serper", "tavily", "exa", "you", "searxng"]
    disabled = [p for p in all_providers if p not in enabled_providers]
    config["auto_routing"]["disabled_providers"] = disabled
    
    # ===== 保存配置 =====
    print()
    print(color("─" * 60, Colors.DIM))
    print(color("\n💾 保存配置\n", Colors.BOLD))
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(color(f"✓ 配置已保存到：{config_path}", Colors.GREEN))
    print()
    
    # ===== 摘要 =====
    print(color("📋 配置摘要：", Colors.BOLD))
    print(f"   已启用提供商：{', '.join(enabled_providers)}")
    print(f"   默认提供商：{default_provider}")
    print(f"   自动路由：{'已启用' if auto_routing else '已禁用'}")
    print(f"   每次搜索结果数：{max_results}")
    print()
    
    # ===== 测试建议 =====
    print(color("🚀 准备好搜索了！试试：", Colors.BOLD))
    print(color(f"   python3 scripts/search.py -q \"你的查询内容\"", Colors.CYAN))
    print()
    
    return True

def check_first_run(skill_dir: Path) -> bool:
    """Check if this is the first run (no config.json)."""
    config_path = skill_dir / "config.json"
    return not config_path.exists()

def main():
    # Determine skill directory
    script_path = Path(__file__).resolve()
    skill_dir = script_path.parent.parent
    
    # Check for --reset flag
    force_reset = "--reset" in sys.argv
    
    # Check for --check flag (just check if setup needed)
    if "--check" in sys.argv:
        if check_first_run(skill_dir):
            print("需要设置：未找到 config.json")
            sys.exit(1)
        else:
            print("设置完成：config.json 已存在")
            sys.exit(0)
    
    # Run setup
    success = run_setup(skill_dir, force_reset)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
