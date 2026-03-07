import os
import shutil
import re
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

# --- CONFIGURATION ---
INPUT_FONT = "FILE.ttf"
OUTPUT_DIR = "FAMILY"
FONT_FAMILY = "FONT FAMILY"
FONT_WEIGHT_RANGE = ""
FONT_STRETCH_RANGE = "" 
FONT_STYLE = "normal"

# Subset definitions
SUBSETS = {
    # Place subsets here
}

def sanitize_name(name):
    return re.sub(r'[^\w\-]', '', name)

def create_subset(subset_name, unicode_range, target_folder, unicodes=None):

    options = subset.Options()
    options.flavor = "woff2"
    options.layout_features = ["*"]

    font = subset.load_font(INPUT_FONT, options)

    if unicodes is None:
        unicodes = subset.parse_unicodes(unicode_range)

    if not unicodes:
        font.close()
        return None

    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)

    family_clean = sanitize_name(FONT_FAMILY)
    filename = f"{family_clean}_{subset_name}.woff2"
    path = target_folder / filename

    font.save(str(path))
    font.close()

    return filename


def generate_css(css_data, target_folder):

    css_path = target_folder / "fonts.css"

    with open(css_path, "w") as f:
        for item in css_data:

            css_block = f"""/* {item['subset_name']} */
@font-face {{
  font-family: '{FONT_FAMILY}';
  font-style: {FONT_STYLE};
  font-weight: {FONT_WEIGHT_RANGE};
  font-stretch: {FONT_STRETCH_RANGE};
  font-display: swap;
  src: url('{item['file']}') format('woff2-variations'), url('{item['file']}') format('woff2');
  unicode-range: {item['range']};
}}
"""

            f.write(css_block + "\n")


def main():

    dist_path = Path(OUTPUT_DIR)

    if dist_path.exists():
        shutil.rmtree(dist_path)

    dist_path.mkdir(parents=True, exist_ok=True)

    if not os.path.exists(INPUT_FONT):
        print(f"Error: {INPUT_FONT} not found.")
        return

    # Load full font to get all unicodes
    font = TTFont(INPUT_FONT)

    font_unicodes = set()
    for table in font["cmap"].tables:
        font_unicodes.update(table.cmap.keys())

    font.close()

    used_unicodes = set()
    css_entries = []

    for name, unicode_range in SUBSETS.items():

        requested = subset.parse_unicodes(unicode_range)
        intersection = font_unicodes.intersection(requested)

        if not intersection:
            print(f"Skipped: {name} (No characters in font)")
            continue

        filename = create_subset(name, unicode_range, dist_path, intersection)

        if filename:

            used_unicodes.update(intersection)

            css_entries.append({
                "subset_name": name,
                "file": filename,
                "range": unicode_range
            })

            print(f"Generated: {name}")

    # --- CREATE ORPHANED SUBSET ---
    remaining = font_unicodes - used_unicodes

    if remaining:

        filename = create_subset("others", None, dist_path, remaining)

        if filename:

            css_entries.append({
                "subset_name": "others",
                "file": filename,
                "range": "U+0-10FFFF"
            })

            print(f"Generated: others ({len(remaining)} glyphs)")

    generate_css(css_entries, dist_path)

    print(f"\nCompleted! Generated {len(css_entries)} files in /{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
