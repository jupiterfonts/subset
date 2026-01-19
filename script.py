import os
import shutil
import re
from pathlib import Path
from fontTools import subset

# --- CONFIGURATION ---
INPUT_FONT = "FontFamily.ttf"
OUTPUT_DIR = "dist"
FONT_FAMILY = "Font Family"
FONT_WEIGHT_RANGE = "100 900" 
FONT_STYLE = "normal"

# Subset definitions
SUBSETS = {
    "latin-ext": "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF",
    "latin": "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD",
}

def sanitize_name(name):
    return re.sub(r'[^\w\-]', '', name)

def create_subset(subset_name, unicode_range, target_folder):
    # Pattern: FontFamily_subsetname.woff2
    family_clean = sanitize_name(FONT_FAMILY)
    output_filename = f"{family_clean}_{subset_name}.woff2"
    output_path = target_folder / output_filename
    
    options = subset.Options()
    options.flavor = 'woff2'
    options.layout_features = ['*']
    
    font = subset.load_font(INPUT_FONT, options)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=subset.parse_unicodes(unicode_range))
    subsetter.subset(font)
    
    font.save(str(output_path))
    font.close()
    return output_filename

def generate_css(css_data, target_folder):
    css_path = target_folder / "fonts.css"
    with open(css_path, "w") as f:
        for item in css_data:
            css_block = f"""/* {item['subset_name']} */
@font-face {{
  font-family: '{FONT_FAMILY}';
  font-style: {FONT_STYLE};
  font-weight: {FONT_WEIGHT_RANGE};
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

    css_entries = []
    
    for name, unicode_range in SUBSETS.items():
        print(f"Generating: {FONT_FAMILY} ({name})...")
        try:
            filename = create_subset(name, unicode_range, dist_path)
            css_entries.append({
                "subset_name": name,
                "file": filename,
                "range": unicode_range
            })
        except Exception as e:
            print(f"Skipping {name}: {e}")

    generate_css(css_entries, dist_path)
    print(f"\nCompleted! Files in /{OUTPUT_DIR}:")
    for entry in css_entries:
        print(f" - {entry['file']}")

if __name__ == "__main__":
    main()
    
