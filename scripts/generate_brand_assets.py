import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='从 assets/branding/app_icon_source.png 生成各平台图标与电视横幅；需要 Pillow。')
parser.add_argument('--output', type=Path, default=root)
options = parser.parse_args()
output = options.output
source = root / 'assets/branding/app_icon_source.png'
if not source.exists():
    raise SystemExit(f'缺少品牌源图：{source}')


def load():
    image = Image.open(source).convert('RGB')
    side = max(image.size)
    canvas = Image.new('RGB', (side, side), '#FFFFFF')
    canvas.paste(image, ((side - image.width) // 2, (side - image.height) // 2))
    return canvas.resize((1024, 1024), Image.Resampling.LANCZOS)


icon = load()
rounded = icon.copy()
corners = Image.new('L', (1024, 1024), 0)
ImageDraw.Draw(corners).rounded_rectangle((0, 0, 1023, 1023), radius=236, fill=255)
rounded.putalpha(corners)
adaptive = Image.new('RGBA', (1536, 1536), (0, 0, 0, 0))
adaptive.paste(icon, (256, 256))
mask = Image.eval(icon.convert('L'), lambda value: 255 - value)
silhouette = Image.new('RGBA', (1024, 1024), (255, 255, 255, 0))
silhouette.putalpha(mask)
monochrome = Image.new('RGBA', (1536, 1536), (0, 0, 0, 0))
monochrome.paste(silhouette, (256, 256), silhouette)


def save(image, name):
    destination = output / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)


contents = json.loads((root / 'ios/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json').read_text())
for entry in contents['images']:
    if 'filename' in entry:
        size = round(float(entry['size'].split('x')[0]) * float(entry['scale'].rstrip('x')))
        save(icon.resize((size, size), Image.Resampling.LANCZOS),
             'ios/Runner/Assets.xcassets/AppIcon.appiconset/' + entry['filename'])
ico = output / 'windows/runner/resources/app_icon.ico'
ico.parent.mkdir(parents=True, exist_ok=True)
try:
    rounded.save(ico, sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
except TypeError:
    rounded.resize((256, 256), Image.Resampling.LANCZOS).save(ico)
macos_canvas = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
macos_badge = rounded.resize((824, 824), Image.Resampling.LANCZOS)
macos_canvas.paste(macos_badge, (100, 100), macos_badge)
macos_contents = json.loads((root / 'macos/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json').read_text())
for entry in macos_contents['images']:
    if 'filename' in entry:
        size = round(float(entry['size'].split('x')[0]) * float(entry['scale'].rstrip('x')))
        save(macos_canvas.resize((size, size), Image.Resampling.LANCZOS),
             'macos/Runner/Assets.xcassets/AppIcon.appiconset/' + entry['filename'])
for density, scale in [('mdpi', 1), ('hdpi', 1.5), ('xhdpi', 2), ('xxhdpi', 3), ('xxxhdpi', 4)]:
    legacy = round(48 * scale)
    layer = round(108 * scale)
    save(rounded.resize((legacy, legacy), Image.Resampling.LANCZOS),
         f'android/app/src/main/res/mipmap-{density}/ic_launcher.png')
    save(adaptive.resize((layer, layer), Image.Resampling.LANCZOS),
         f'android/app/src/main/res/mipmap-{density}/ic_launcher_foreground.png')
    save(monochrome.resize((layer, layer), Image.Resampling.LANCZOS),
         f'android/app/src/main/res/mipmap-{density}/ic_launcher_monochrome.png')
for resource in ('tv_banner', 'tv_banner_all_sources'):
    banner = Image.new('RGB', (640, 360), '#FAF8FC')
    badge = rounded.resize((220, 220), Image.Resampling.LANCZOS)
    banner.paste(badge, (210, 70), badge)
    save(banner, f'android/app/src/main/res/drawable-xhdpi/{resource}.png')
