import os
import shutil
import re
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

# ================= CONFIG =================

FONT_FAMILY = "FONT FAMILY"
OUTPUT_DIR = "FAMILY"

FONTS = [
    {"file": "FONTFILE-REGULAR.ttf", "weight": "400", "style": "normal"},
    {"file": "FONTFILE-ITALIC.ttf", "weight": "400", "style": "italic"},
    {"file": "FONTFILE-BOLD.ttf", "weight": "700", "style": "normal"},
    {"file": "FONTFILE-BOLDITALIC.ttf", "weight": "700", "style": "italic"},
]

SUBSETS = {
    # Place subsets here
}

IGNORED_UNICODES = {
    0x0000,
    0x0009,
    0x000A,
    0x000D,
    0x0020,
    0x00A0,
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


def create_subset_from_unicodes(
    font_path,
    subset_name,
    unicodes,
    unicode_range,
    target_dir,
    weight,
    style,
):

    if not unicodes:
        return None

    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]

    font = subset.load_font(font_path, options)

    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=unicodes)
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

        base_font = TTFont(font_path)
        font_unicodes = font_supported_unicodes(base_font)
        base_font.close()

        used_unicodes = set()

        # ----------- NORMAL SUBSETS -----------

        for subset_name, unicode_range in SUBSETS.items():

            try:

                requested = subset.parse_unicodes(unicode_range)

                meaningful = (
                    font_unicodes
                    .intersection(requested)
                    .difference(IGNORED_UNICODES)
                )

                if len(meaningful) < MIN_GLYPHS:
                    continue

                filename = create_subset_from_unicodes(
                    font_path,
                    subset_name,
                    requested,
                    unicode_range,
                    out_dir,
                    weight,
                    style,
                )

                if filename:

                    used_unicodes.update(requested)

                    css_entries.append(
                        {
                            "file": filename,
                            "subset": subset_name,
                            "range": unicode_range,
                            "weight": weight,
                            "style": style,
                        }
                    )

                    print(
                        f"Generated: {FONT_FAMILY} {weight} {style} ({subset_name})"
                    )

            except Exception as e:

                print(f"Error: {font_path} / {subset_name}: {e}")

        # ----------- ORPHAN SUBSET -----------

        remaining = font_unicodes.difference(used_unicodes).difference(IGNORED_UNICODES)

        if remaining:

            filename = create_subset_from_unicodes(
                font_path,
                "others",
                remaining,
                "U+0-10FFFF",
                out_dir,
                weight,
                style,
            )

            if filename:

                css_entries.append(
                    {
                        "file": filename,
                        "subset": "others",
                        "range": "U+0-10FFFF",
                        "weight": weight,
                        "style": style,
                    }
                )

                print(
                    f"Generated: {FONT_FAMILY} {weight} {style} (others) "
                    f"[{len(remaining)} glyphs]"
                )

    generate_css(css_entries, out_dir)

    print(f"\nDone. Generated {len(css_entries)} font files.")


if __name__ == "__main__":
    main()
