"""生成「盘研高参」应用图标：深蓝渐变圆底 + 白色"盘"字 + 红色上升箭头。"""
import math
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
OUT_DIR = "apps/dsa-desktop/build"
FONT = "C:/Windows/Fonts/msyhbd.ttc"


def radial_gradient(size, center_color, edge_color):
    """逐像素径向渐变，中心亮、边缘深。"""
    img = Image.new("RGB", (size, size))
    cx = cy = size / 2
    max_d = math.hypot(cx, cy)
    for y in range(size):
        for x in range(size):
            d = math.hypot(x - cx, y - cy) / max_d
            r = int(center_color[0] + (edge_color[0] - center_color[0]) * d)
            g = int(center_color[1] + (edge_color[1] - center_color[1]) * d)
            b = int(center_color[2] + (edge_color[2] - center_color[2]) * d)
            img.putpixel((x, y), (r, g, b))
    return img


def main():
    base = radial_gradient(SIZE, (59, 130, 246), (23, 37, 84))  # 蓝-400 → 蓝-950

    # 圆形蒙版（图标边缘留透明）
    icon = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse([8, 8, SIZE - 8, SIZE - 8], fill=255)
    icon.paste(base, (0, 0), mask)

    draw = ImageDraw.Draw(icon)
    # 顶部红色上升箭头（三折线）
    arrow = [(70, 118), (108, 82), (148, 100), (186, 56)]
    draw.line(arrow, fill=(239, 68, 68), width=14, joint="curve")

    # 中央"盘"字
    font = ImageFont.truetype(FONT, 96)
    bbox = draw.textbbox((0, 0), "盘", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((SIZE - tw) / 2 - bbox[0], (SIZE - th) / 2 - bbox[1] + 6), "盘", font=font, fill="white")

    import os
    os.makedirs(OUT_DIR, exist_ok=True)
    icon.save(f"{OUT_DIR}/icon.png")
    icon.save(f"{OUT_DIR}/icon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print("图标已生成:", OUT_DIR)


if __name__ == "__main__":
    main()
