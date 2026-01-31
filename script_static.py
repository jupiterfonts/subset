import os
import shutil
import re
from pathlib import Path
from fontTools import subset

# ================= CONFIG =================

FONT_FAMILY = "FontFamily"
OUTPUT_DIR = "dist"

# Define all font files in the family
FONTS = [
    {"file": "FontFamily-Regular.ttf", "weight": "400", "style": "normal"},
    {"file": "FontFamily-Italic.ttf", "weight": "400", "style": "italic"},
    {"file": "FontFamily-Bold.ttf", "weight": "700", "style": "normal"},
    {"file": "FontFamily-BoldItalic.ttf", "weight": "700", "style": "italic"},
]

# SUBSETS = {...}
# (you will paste your full subset dictionary here)

IGNORED_UNICODES = {
    0x0000,  # NULL
    0x0009,  # TAB
    0x000A,  # LF
    0x000D,  # CR
    0x0020,  # SPACE
    0x00A0,  # NO-BREAK SPACE
}

MIN_GLYPHS = 5

# ==========================================


def sanitize_name(name: str) -> str:
    return re.sub(r"[^\w\-]", "", name)


def font_supported_unicodes(font):
    unicodes = set()
    for table in font["cmap"].tables:
        unicodes.update(table.cmap.keys())
    return unicodes


def create_subset(
    font_path: str,
    subset_name: str,
    unicode_range: str,
    target_dir: Path,
    weight: str,
    style: str,
):
    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]

    font = subset.load_font(font_path, options)

    font_unicodes = font_supported_unicodes(font)
    requested = subset.parse_unicodes(unicode_range)

    meaningful = (
        font_unicodes
        .intersection(requested)
        .difference(IGNORED_UNICODES)
    )

    if len(meaningful) < MIN_GLYPHS:
        font.close()
        return None

    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=requested)
    subsetter.subset(font)

    family = sanitize_name(FONT_FAMILY)
    filename = f"{family}_{weight}-{style}_{subset_name}.woff2"
    output_path = target_dir / filename

    font.save(str(output_path))
    font.close()

    return filename


def generate_css(entries, target_dir: Path):
    css_path = target_dir / "fonts.css"

    with open(css_path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(
                f"""/* {e['subset']} */
@font-face {{
  font-family: '{FONT_FAMILY}';
  font-style: {e['style']};
  font-weight: {e['weight']};
  font-display: swap;
  src: url('{e['file']}') format('woff2');
  unicode-range: {e['range']};
}}

"""
            )


def main():
    out_dir = Path(OUTPUT_DIR)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    css_entries = []

    for font in FONTS:
        font_path = font["file"]
        weight = font["weight"]
        style = font["style"]

        if not os.path.exists(font_path):
            print(f"Missing font file: {font_path}")
            continue

        for subset_name, unicode_range in SUBSETS.items():
            try:
                filename = create_subset(
                    font_path,
                    subset_name,
                    unicode_range,
                    out_dir,
                    weight,
                    style,
                )

                if filename:
                    print(
                        f"Generated: {FONT_FAMILY} {weight} {style} ({subset_name})"
                    )
                    css_entries.append(
                        {
                            "file": filename,
                            "subset": subset_name,
                            "range": unicode_range,
                            "weight": weight,
                            "style": style,
                        }
                    )

            except Exception as e:
                print(f"Error: {font_path} / {subset_name}: {e}")

    generate_css(css_entries, out_dir)

    print(f"\nDone. Generated {len(css_entries)} font files.")


if __name__ == "__main__":
    main()
