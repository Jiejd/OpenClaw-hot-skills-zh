#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
使用 Google 的 Nano Banana Pro (Gemini 3 Pro Image) API 生成图像。

用法：
    uv run generate_image.py --prompt "你的图像描述" --filename "输出.png" [--resolution 1K|2K|4K] [--api-key KEY]
"""

import argparse
import os
import sys
from pathlib import Path


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def main():
    parser = argparse.ArgumentParser(
        description="使用 Nano Banana Pro (Gemini 3 Pro Image) 生成图像"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="图像描述/提示词"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="输出文件名（例如：sunset-mountains.png）"
    )
    parser.add_argument(
        "--input-image", "-i",
        help="可选的输入图像路径，用于编辑/修改"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default="1K",
        help="输出分辨率：1K（默认）、2K 或 4K"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API 密钥（覆盖 GEMINI_API_KEY 环境变量）"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("错误：未提供 API 密钥。", file=sys.stderr)
        print("请执行以下操作之一：", file=sys.stderr)
        print("  1. 提供 --api-key 参数", file=sys.stderr)
        print("  2. 设置 GEMINI_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    # Import here after checking API key to avoid slow import on error
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    # Initialise client
    client = genai.Client(api_key=api_key)

    # Set up output path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load input image if provided
    input_image = None
    output_resolution = args.resolution
    if args.input_image:
        try:
            input_image = PILImage.open(args.input_image)
            print(f"已加载输入图像：{args.input_image}")

            # Auto-detect resolution if not explicitly set by user
            if args.resolution == "1K":  # Default value
                # Map input image size to resolution
                width, height = input_image.size
                max_dim = max(width, height)
                if max_dim >= 3000:
                    output_resolution = "4K"
                elif max_dim >= 1500:
                    output_resolution = "2K"
                else:
                    output_resolution = "1K"
                print(f"自动检测分辨率：{output_resolution}（来自输入 {width}x{height}）")
        except Exception as e:
            print(f"加载输入图像时出错：{e}", file=sys.stderr)
            sys.exit(1)

    # Build contents (image first if editing, prompt only if generating)
    if input_image:
        contents = [input_image, args.prompt]
        print(f"正在编辑图像，分辨率 {output_resolution}...")
    else:
        contents = args.prompt
        print(f"正在生成图像，分辨率 {output_resolution}...")

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    image_size=output_resolution
                )
            )
        )

        # Process response and convert to PNG
        image_saved = False
        for part in response.parts:
            if part.text is not None:
                print(f"模型响应：{part.text}")
            elif part.inline_data is not None:
                # Convert inline data to PIL Image and save as PNG
                from io import BytesIO

                # inline_data.data is already bytes, not base64
                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    # If it's a string, it might be base64
                    import base64
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                # Ensure RGB mode for PNG (convert RGBA to RGB with white background if needed)
                if image.mode == 'RGBA':
                    rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[3])
                    rgb_image.save(str(output_path), 'PNG')
                elif image.mode == 'RGB':
                    image.save(str(output_path), 'PNG')
                else:
                    image.convert('RGB').save(str(output_path), 'PNG')
                image_saved = True

        if image_saved:
            full_path = output_path.resolve()
            print(f"\n图像已保存：{full_path}")
        else:
            print("错误：响应中未生成图像。", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"生成图像时出错：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
