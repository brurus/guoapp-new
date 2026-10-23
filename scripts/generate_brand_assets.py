import argparse
import json
from pathlib import Path

from PIL import Image

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='从 assets/branding/app_icon_source.png 生成各平台品牌资源；需要 Pillow。')
parser.add_argument('--output', type=Path, default=root)
parser.add_argument('--source', type=Path, default=root / 'assets/branding/app_icon_source.png')
options = parser.parse_args()
output = options.output
icon = Image.open(options.source).convert('RGB')


def save(image, name):
    destination = output / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)


# iOS 全套图标（按 AppIcon.appiconset/Contents.json 清单）
contents = json.loads((root / 'ios/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json').read_text())
for entry in contents['images']:
    if 'filename' in entry:
        size = round(float(entry['size'].split('x')[0]) * float(entry['scale'].rstrip('x')))
        save(icon.resize((size, size), Image.Resampling.LANCZOS),
             'ios/Runner/Assets.xcassets/AppIcon.appiconset/' + entry['filename'])

# Windows 桌面图标（多尺寸 ico）
save_path = output / 'windows/runner/resources/app_icon.ico'
save_path.parent.mkdir(parents=True, exist_ok=True)
icon.resize((256, 256), Image.Resampling.LANCZOS).save(
    save_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

# Android 桌面图标（各密度）
for density, size in [('mdpi', 48), ('hdpi', 72), ('xhdpi', 96), ('xxhdpi', 144), ('xxxhdpi', 192)]:
    save(icon.resize((size, size), Image.Resampling.LANCZOS),
         f'android/app/src/main/res/mipmap-{density}/ic_launcher.png')

# Android TV 横幅（仅图标，不含文字）
for resource in ('tv_banner', 'tv_banner_all_sources'):
    banner = Image.new('RGB', (640, 360), '#101114')
    banner.paste(icon.resize((180, 180), Image.Resampling.LANCZOS), (44, 90))
    save(banner, f'android/app/src/main/res/drawable-xhdpi/{resource}.png')
