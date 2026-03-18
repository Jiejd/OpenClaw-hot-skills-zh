#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
用法：
  frame.sh <视频文件> [--time HH:MM:SS] [--index N] --out /path/to/frame.jpg

示例：
  frame.sh video.mp4 --out /tmp/frame.jpg
  frame.sh video.mp4 --time 00:00:10 --out /tmp/frame-10s.jpg
  frame.sh video.mp4 --index 0 --out /tmp/frame0.png
EOF
  exit 2
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
fi

in="${1:-}"
shift || true

time=""
index=""
out=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --time)
      time="${2:-}"
      shift 2
      ;;
    --index)
      index="${2:-}"
      shift 2
      ;;
    --out)
      out="${2:-}"
      shift 2
      ;;
    *)
      echo "未知参数: $1" >&2
      usage
      ;;
  esac
done

if [[ ! -f "$in" ]]; then
  echo "文件未找到: $in" >&2
  exit 1
fi

if [[ "$out" == "" ]]; then
  echo "缺少 --out 参数" >&2
  usage
fi

mkdir -p "$(dirname "$out")"

if [[ "$index" != "" ]]; then
  ffmpeg -hide_banner -loglevel error -y \
    -i "$in" \
    -vf "select=eq(n\\,${index})" \
    -vframes 1 \
    "$out"
elif [[ "$time" != "" ]]; then
  ffmpeg -hide_banner -loglevel error -y \
    -ss "$time" \
    -i "$in" \
    -frames:v 1 \
    "$out"
else
  ffmpeg -hide_banner -loglevel error -y \
    -i "$in" \
    -vf "select=eq(n\\,0)" \
    -vframes 1 \
    "$out"
fi

echo "$out"
