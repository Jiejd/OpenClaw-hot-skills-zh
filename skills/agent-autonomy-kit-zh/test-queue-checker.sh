#!/bin/bash
# 队列检查器强制执行测试脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUEUE_CHECKER="$SCRIPT_DIR/check-queue.js"
TEST_QUEUE_DIR="$(mktemp -d)"
TEST_QUEUE="$TEST_QUEUE_DIR/QUEUE.md"

echo "🧪 测试队列检查器强制执行"
echo "===================================="
echo ""

# 测试 1：空队列
echo "测试 1：空队列（应返回 0）"
mkdir -p "$TEST_QUEUE_DIR/tasks"
cat > "$TEST_QUEUE_DIR/tasks/QUEUE.md" << 'EOF'
# Task Queue

## 🔥 High Priority

## 🟡 Medium Priority

## ✅ Done
EOF

cd "$TEST_QUEUE_DIR"
if node "$QUEUE_CHECKER"; then
  echo "✅ 通过：空队列返回退出码 0"
else
  echo "❌ 失败：空队列应返回 0"
  exit 1
fi
echo ""

# 测试 2：仅 LOW 优先级任务
echo "测试 2：仅 LOW 优先级任务（应返回 0）"
cat > "$TEST_QUEUE_DIR/tasks/QUEUE.md" << 'EOF'
# Task Queue

## 🔥 High Priority
- [ ] [LOW] Update documentation
- [ ] [LOW] Refactor old code

## ✅ Done
EOF

if node "$QUEUE_CHECKER"; then
  echo "✅ 通过：LOW 优先级任务返回退出码 0"
else
  echo "❌ 失败：LOW 优先级任务应返回 0"
  exit 1
fi
echo ""

# 测试 3：存在 HIGH 优先级任务
echo "测试 3：存在 HIGH 优先级任务（应返回 1）"
cat > "$TEST_QUEUE_DIR/tasks/QUEUE.md" << 'EOF'
# Task Queue

## 🔥 High Priority
- [ ] **Fix critical authentication bug**
- [ ] [LOW] Update docs

## ✅ Done
EOF

if node "$QUEUE_CHECKER"; then
  echo "❌ 失败：HIGH 优先级任务应返回退出码 1"
  exit 1
else
  echo "✅ 通过：HIGH 优先级任务返回退出码 1"
fi
echo ""

# 测试 4：存在 CRITICAL 优先级任务
echo "测试 4：存在 CRITICAL 优先级任务（应返回 1）"
cat > "$TEST_QUEUE_DIR/tasks/QUEUE.md" << 'EOF'
# Task Queue

## 🔥 High Priority
- [ ] [CRITICAL] 🔥 Production database down

## ✅ Done
EOF

if node "$QUEUE_CHECKER"; then
  echo "❌ 失败：CRITICAL 任务应返回退出码 1"
  exit 1
else
  echo "✅ 通过：CRITICAL 任务返回退出码 1"
fi
echo ""

# 测试 5：Done 分区中的任务被忽略
echo "测试 5：Done 分区中已完成的 HIGH 任务（应返回 0）"
cat > "$TEST_QUEUE_DIR/tasks/QUEUE.md" << 'EOF'
# Task Queue

## 🔥 High Priority

## ✅ Done
- [x] **Fixed authentication bug**
- [x] [HIGH] Deployed hotfix
EOF

if node "$QUEUE_CHECKER"; then
  echo "✅ 通过：已完成任务被忽略，返回退出码 0"
else
  echo "❌ 失败：已完成任务应被忽略"
  exit 1
fi
echo ""

# 测试 6：In Progress 中的任务
echo "测试 6：HIGH 优先级任务进行中（应返回 0 - 已在处理）"
cat > "$TEST_QUEUE_DIR/tasks/QUEUE.md" << 'EOF'
# Task Queue

## 🔥 High Priority

## 🟡 In Progress
- [ ] **Fix authentication bug** (@kai working on it)

## ✅ Done
EOF

if node "$QUEUE_CHECKER"; then
  echo "✅ 通过：In Progress 任务不阻塞（退出码 0）"
else
  echo "❌ 失败：In Progress 任务应返回 0"
  exit 1
fi
echo ""

# 测试 7：Blocked 分区中的任务
echo "测试 7：HIGH 优先级任务已阻塞（应返回 0 - 无法处理）"
cat > "$TEST_QUEUE_DIR/tasks/QUEUE.md" << 'EOF'
# Task Queue

## 🔥 High Priority

## 🔵 Blocked
- [ ] **Deploy to production** (needs: Ryan's approval)

## ✅ Done
EOF

if node "$QUEUE_CHECKER"; then
  echo "✅ 通过：Blocked 任务不阻塞心跳（退出码 0）"
else
  echo "❌ 失败：Blocked 任务应返回 0"
  exit 1
fi
echo ""

# 测试 8：混合优先级 - HIGH 优先
echo "测试 8：混合优先级（应因 HIGH 返回 1）"
cat > "$TEST_QUEUE_DIR/tasks/QUEUE.md" << 'EOF'
# Task Queue

## 🔥 High Priority
- [ ] [LOW] Update docs
- [ ] **Fix security vulnerability**
- [ ] [LOW] Refactor code

## ✅ Done
EOF

if node "$QUEUE_CHECKER"; then
  echo "❌ 失败：在 LOW 中存在 HIGH 应返回 1"
  exit 1
else
  echo "✅ 通过：在 LOW 任务中检测到 HIGH 优先级（退出码 1）"
fi
echo ""

# 清理
rm -rf "$TEST_QUEUE_DIR"

echo "================================"
echo "✅ 所有测试通过！"
echo ""
echo "队列检查器强制执行工作正常。"
echo "智能体无法跳过 HIGH/CRITICAL 任务。"
