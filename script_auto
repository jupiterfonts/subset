import os
import shutil
import re
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

# --- CONFIGURATION ---
INPUT_FONT = "FontFamily.ttf"
OUTPUT_DIR = "dist"
FONT_FAMILY = "FontFamily"
FONT_WEIGHT_RANGE = "400" 
FONT_STYLE = "normal"

# Subset definitions (remains the same)
SUBSETS = {
    "latin": "U+0000-007F",
    "latin-supplement": "U+0080-00FF",
    "latin-extended-a": "U+0100-017F",
    "latin-extended-b": "U+0180-024F",
    "ipa-extensions": "U+0250-02AF",
    "spacing-modifier-letters": "U+02B0-02FF",
    "combining-diacritical-marks": "U+0300-036F",
    "greek-and-coptic": "U+0370-03FF",
    "cyrillic": "U+0400-04FF",
    "cyrillic-supplement": "U+0500-052F",
    "armenian": "U+0530-058F",
    "hebrew": "U+0590-05FF",
    "arabic": "U+0600-06FF",
    "syriac": "U+0700-074F",
    "arabic-supplement": "U+0750-077F",
    "thaana": "U+0780-07BF",
    "nko": "U+07C0-07FF",
    "samaritan": "U+0800-083F",
    "mandaic": "U+0840-085F",
    "syriac-supplement": "U+0860-086F",
    "arabic-extended-a": "U+08A0-08FF",
    "devanagari": "U+0900-097F",
    "bengali": "U+0980-09FF",
    "gurmukhi": "U+0A00-0A7F",
    "gujarati": "U+0A80-0AFF",
    "oriya": "U+0B00-0B7F",
    "tamil": "U+0B80-0BFF",
    "telugu": "U+0C00-0C7F",
    "kannada": "U+0C80-0CFF",
    "malayalam": "U+0D00-0D7F",
    "sinhala": "U+0D80-0DFF",
    "thai": "U+0E00-0E7F",
    "lao": "U+0E80-0EFF",
    "tibetan": "U+0F00-0FFF",
    "myanmar": "U+1000-109F",
    "georgian": "U+10A0-10FF",
    "hangul-jamo": "U+1100-11FF",
    "ethiopic": "U+1200-137F",
    "ethiopic-supplement": "U+1380-139F",
    "cherokee": "U+13A0-13FF",
    "unified-canadian-aboriginal-syllabics": "U+1400-167F",
    "ogham": "U+1680-169F",
    "runic": "U+16A0-16FF",
    "tagalog": "U+1700-171F",
    "hanunoo": "U+1720-173F",
    "buhid": "U+1740-175F",
    "tagbanwa": "U+1760-177F",
    "khmer": "U+1780-17FF",
    "mongolian": "U+1800-18AF",
    "unified-canadian-aboriginal-syllabics-extended": "U+18B0-18FF",
    "limbu": "U+1900-194F",
    "tai-le": "U+1950-197F",
    "new-tai-lue": "U+1980-19DF",
    "khmer-symbols": "U+19E0-19FF",
    "buginese": "U+1A00-1A1F",
    "tai-tham": "U+1A20-1AAF",
    "combining-diacritical-marks-extended": "U+1AB0-1AFF",
    "balinese": "U+1B00-1B7F",
    "sundanese": "U+1B80-1BBF",
    "batak": "U+1BC0-1BFF",
    "lepcha": "U+1C00-1C4F",
    "ol-chiki": "U+1C50-1C7F",
    "cyrillic-extended-c": "U+1C80-1C8F",
    "georgian-extended": "U+1C90-1CBF",
    "sundanese-supplement": "U+1CC0-1CCF",
    "vedic-extensions": "U+1CD0-1CFF",
    "phonetic-extensions": "U+1D00-1D7F",
    "phonetic-extensions-supplement": "U+1D80-1DBF",
    "combining-diacritical-marks-supplement": "U+1DC0-1DFF",
    "latin-extended-additional": "U+1E00-1EFF",
    "greek-extended": "U+1F00-1FFF",
    "general-punctuation": "U+2000-206F",
    "superscripts-and-subscripts": "U+2070-209F",
    "currency-symbols": "U+20A0-20CF",
    "combining-diacritical-marks-for-symbols": "U+20D0-20FF",
    "letterlike-symbols": "U+2100-214F",
    "number-forms": "U+2150-218F",
    "arrows": "U+2190-21FF",
    "mathematical-operators": "U+2200-22FF",
    "miscellaneous-technical": "U+2300-23FF",
    "control-pictures": "U+2400-243F",
    "optical-character-recognition": "U+2440-245F",
    "enclosed-alphanumerics": "U+2460-24FF",
    "box-drawing": "U+2500-257F",
    "block-elements": "U+2580-259F",
    "geometric-shapes": "U+25A0-25FF",
    "miscellaneous-symbols": "U+2600-26FF",
    "dingbats": "U+2700-27BF",
    "miscellaneous-mathematical-symbols-a": "U+27C0-27EF",
    "supplemental-arrows-a": "U+27F0-27FF",
    "braille-patterns": "U+2800-28FF",
    "supplemental-arrows-b": "U+2900-297F",
    "miscellaneous-mathematical-symbols-b": "U+2980-29FF",
    "supplemental-mathematical-operators": "U+2A00-2AFF",
    "miscellaneous-symbols-and-arrows": "U+2B00-2BFF",
    "glagolitic": "U+2C00-2C5F",
    "latin-extended-c": "U+2C60-2C7F",
    "coptic": "U+2C80-2CFF",
    "georgian-supplement": "U+2D00-2D2F",
    "tifinagh": "U+2D30-2D7F",
    "ethiopic-extended": "U+2D80-2DDF",
    "cyrillic-extended-a": "U+2DE0-2DFF",
    "supplemental-punctuation": "U+2E00-2E7F",
    "cjk-radicals-supplement": "U+2E80-2EFF",
    "kangxi-radicals": "U+2F00-2FDF",
    "ideographic-description-characters": "U+2FF0-2FFF",
    "cjk-symbols-and-punctuation": "U+3000-303F",
    "hiragana": "U+3040-309F",
    "katakana": "U+30A0-30FF",
    "bopomofo": "U+3100-312F",
    "hangul-compatibility-jamo": "U+3130-318F",
    "kanbun": "U+3190-319F",
    "bopomofo-extended": "U+31A0-31BF",
    "cjk-strokes": "U+31C0-31EF",
    "katakana-phonetic-extensions": "U+31F0-31FF",
    "enclosed-cjk-letters-and-months": "U+3200-32FF",
    "cjk-compatibility": "U+3300-33FF",
    "cjk-unified-ideographs-extension-a": "U+3400-4DBF",
    "yijing-hexagram-symbols": "U+4DC0-4DFF",
    "cjk-unified-ideographs": "U+4E00-9FFF",
    "yi-syllables": "U+A000-A48F",
    "yi-radicals": "U+A490-A4CF",
    "lisu": "U+A4D0-A4FF",
    "vai": "U+A500-A63F",
    "cyrillic-extended-b": "U+A640-A69F",
    "bamum": "U+A6A0-A6FF",
    "modifier-tone-letters": "U+A700-A71F",
    "latin-extended-d": "U+A720-A7FF",
    "syloti-nagri": "U+A800-A82F",
    "common-indic-number-forms": "U+A830-A83F",
    "phags-pa": "U+A840-A87F",
    "saurashtra": "U+A880-A8DF",
    "devanagari-extended": "U+A8E0-A8FF",
    "kayah-li": "U+A900-A92F",
    "rejang": "U+A930-A95F",
    "hangul-jamo-extended-a": "U+A960-A97F",
    "javanese": "U+A980-A9DF",
    "myanmar-extended-b": "U+A9E0-A9FF",
    "cham": "U+AA00-AA5F",
    "myanmar-extended-a": "U+AA60-AA7F",
    "tai-viet": "U+AA80-AADF",
    "meetei-mayek-extensions": "U+AAE0-AAFF",
    "ethiopic-extended-a": "U+AB00-AB2F",
    "latin-extended-e": "U+AB30-AB6F",
    "cherokee-supplement": "U+AB70-ABBF",
    "meetei-mayek": "U+ABC0-ABFF",
    "hangul-syllables": "U+AC00-D7AF",
    "hangul-jamo-extended-b": "U+D7B0-D7FF",
    "high-surrogates": "U+D800-DB7F",
    "high-private-use-surrogates": "U+DB80-DBFF",
    "low-surrogates": "U+DC00-DFFF",
    "private-use-area": "U+E000-F8FF",
    "cjk-compatibility-ideographs": "U+F900-FAFF",
    "alphabetic-presentation-forms": "U+FB00-FB4F",
    "arabic-presentation-forms-a": "U+FB50-FDFF",
    "variation-selectors": "U+FE00-FE0F",
    "vertical-forms": "U+FE10-FE1F",
    "combining-half-marks": "U+FE20-FE2F",
    "cjk-compatibility-forms": "U+FE30-FE4F",
    "small-form-variants": "U+FE50-FE6F",
    "arabic-presentation-forms-b": "U+FE70-FEFF",
    "halfwidth-and-fullwidth-forms": "U+FF00-FFEF",
    "specials": "U+FFF0-FFFF",
    "linear-b-syllabary": "U+10000-1007F",
    "linear-b-ideograms": "U+10080-100FF",
    "aegean-numbers": "U+10100-1013F",
    "ancient-greek-numbers": "U+10140-1018F",
    "ancient-symbols": "U+10190-101CF",
    "phaistos-disc": "U+101D0-101FF",
    "lycian": "U+10280-1029F",
    "carian": "U+102A0-102DF",
    "coptic-epact-numbers": "U+102E0-102FF",
    "old-italic": "U+10300-1032F",
    "gothic": "U+10330-1034F",
    "old-permic": "U+10350-1037F",
    "ugaritic": "U+10380-1039F",
    "old-persian": "U+103A0-103DF",
    "deseret": "U+10400-1044F",
    "shavian": "U+10450-1047F",
    "osmanya": "U+10480-104AF",
    "osage": "U+104B0-104FF",
    "elbasan": "U+10500-1052F",
    "caucasian-albanian": "U+10530-1056F",
    "linear-a": "U+10600-1077F",
    "cypriot-syllabary": "U+10800-1083F",
    "imperial-aramaic": "U+10840-1085F",
    "palmyrene": "U+10860-1087F",
    "nabataean": "U+10880-108AF",
    "hatran": "U+108E0-108FF",
    "phoenician": "U+10900-1091F",
    "lydian": "U+10920-1093F",
    "meroitic-hieroglyphs": "U+10980-1099F",
    "meroitic-cursive": "U+109A0-109FF",
    "kharoshthi": "U+10A00-10A5F",
    "old-south-arabian": "U+10A60-10A7F",
    "old-north-arabian": "U+10A80-10A9F",
    "manichaean": "U+10AC0-10AFF",
    "avestan": "U+10B00-10B3F",
    "inscriptional-parthian": "U+10B40-10B5F",
    "inscriptional-pahlavi": "U+10B60-10B7F",
    "psalter-pahlavi": "U+10B80-10BAF",
    "old-turkic": "U+10C00-10C4F",
    "old-hungarian": "U+10C80-10CFF",
    "hanifi-rohingya": "U+10D00-10D3F",
    "rumi-numeral-symbols": "U+10E60-10E7F",
    "old-sogdian": "U+10F00-10F2F",
    "sogdian": "U+10F30-10F6F",
    "elymaic": "U+10FE0-10FFF",
    "brahmi": "U+11000-1107F",
    "kaithi": "U+11080-110CF",
    "sora-sompeng": "U+110D0-110FF",
    "chakma": "U+11100-1114F",
    "mahajani": "U+11150-1117F",
    "sharada": "U+11180-111DF",
    "sinhala-archaic-numbers": "U+111E0-111FF",
    "khojki": "U+11200-1124F",
    "multani": "U+11280-112AF",
    "khudawadi": "U+112B0-112FF",
    "grantha": "U+11300-1137F",
    "newa": "U+11400-1147F",
    "tirhuta": "U+11480-114DF",
    "siddham": "U+11580-115FF",
    "modi": "U+11600-1165F",
    "mongolian-supplement": "U+11660-1167F",
    "takri": "U+11680-116CF",
    "ahom": "U+11700-1173F",
    "dogra": "U+11800-1184F",
    "warang-citi": "U+118A0-118FF",
    "nandinagari": "U+119A0-119FF",
    "zanabazar-square": "U+11A00-11A4F",
    "soyombo": "U+11A50-11AAF",
    "pau-cin-hau": "U+11AC0-11AFF",
    "bhaiksuki": "U+11C00-11C6F",
    "marchen": "U+11C70-11CBF",
    "masaram-gondi": "U+11D00-11D5F",
    "gunjala-gondi": "U+11D60-11DAF",
    "makasar": "U+11EE0-11EFF",
    "tamil-supplement": "U+11FC0-11FFF",
    "cuneiform": "U+12000-123FF",
    "cuneiform-numbers-and-punctuation": "U+12400-1247F",
    "early-dynastic-cuneiform": "U+12480-1254F",
    "egyptian-hieroglyphs": "U+13000-1342F",
    "egyptian-hieroglyph-format-controls": "U+13430-1343F",
    "anatolian-hieroglyphs": "U+14400-1467F",
    "bamum-supplement": "U+16800-16A3F",
    "mro": "U+16A40-16A6F",
    "bassa-vah": "U+16AD0-16AFF",
    "pahawh-hmong": "U+16B00-16B8F",
    "medefaidrin": "U+16E40-16E9F",
    "miao": "U+16F00-16F9F",
    "ideographic-symbols-and-punctuation": "U+16FE0-16FFF",
    "tangut": "U+17000-187FF",
    "tangut-components": "U+18800-18AFF",
    "kana-supplement": "U+1B000-1B0FF",
    "kana-extended-a": "U+1B100-1B12F",
    "small-kana-extension": "U+1B130-1B16F",
    "nushu": "U+1B170-1B2FF",
    "duployan": "U+1BC00-1BC9F",
    "shorthand-format-controls": "U+1BCA0-1BCAF",
    "byzantine-musical-symbols": "U+1D000-1D0FF",
    "musical-symbols": "U+1D100-1D1FF",
    "ancient-greek-musical-notation": "U+1D200-1D24F",
    "mayan-numerals": "U+1D2E0-1D2FF",
    "tai-xuan-jing-symbols": "U+1D300-1D35F",
    "counting-rod-numerals": "U+1D360-1D37F",
    "mathematical-alphanumeric-symbols": "U+1D400-1D7FF",
    "sutton-signwriting": "U+1D800-1DAAF",
    "glagolitic-supplement": "U+1E000-1E02F",
    "nyiakeng-puachue-hmong": "U+1E100-1E14F",
    "wancho": "U+1E2C0-1E2FF",
    "mende-kikakui": "U+1E800-1E8DF",
    "adlam": "U+1E900-1E95F",
    "indic-siyaq-numbers": "U+1EC70-1ECBF",
    "ottoman-siyaq-numbers": "U+1ED00-1ED4F",
    "arabic-mathematical-alphabetic-symbols": "U+1EE00-1EEFF",
    "mahjong-tiles": "U+1F000-1F02F",
    "domino-tiles": "U+1F030-1F09F",
    "playing-cards": "U+1F0A0-1F0FF",
    "enclosed-alphanumeric-supplement": "U+1F100-1F1FF",
    "enclosed-ideographic-supplement": "U+1F200-1F2FF",
    "miscellaneous-symbols-and-pictographs": "U+1F300-1F5FF",
    "emoticons": "U+1F600-1F64F",
    "ornamental-dingbats": "U+1F650-1F67F",
    "transport-and-map-symbols": "U+1F680-1F6FF",
    "alchemical-symbols": "U+1F700-1F77F",
    "geometric-shapes-extended": "U+1F780-1F7FF",
    "supplemental-arrows-c": "U+1F800-1F8FF",
    "supplemental-symbols-and-pictographs": "U+1F900-1F9FF",
    "chess-symbols": "U+1FA00-1FA6F",
    "symbols-and-pictographs-extended-a": "U+1FA70-1FAFF",
    "cjk-unified-ideographs-extension-b": "U+20000-2A6DF",
    "cjk-unified-ideographs-extension-c": "U+2A700-2B73F",
    "cjk-unified-ideographs-extension-d": "U+2B740-2B81F",
    "cjk-unified-ideographs-extension-e": "U+2B820-2CEAF",
    "cjk-unified-ideographs-extension-f": "U+2CEB0-2EBEF",
    "cjk-compatibility-ideographs-supplement": "U+2F800-2FA1F",
    "tags": "U+E0000-E007F",
    "variation-selectors-supplement": "U+E0100-E01EF",
    "supplementary-private-use-area-a": "U+F0000-FFFFF",
    "supplementary-private-use-area-b": "U+100000-10FFFF"
}

def sanitize_name(name):
    return re.sub(r'[^\w\-]', '', name)

def create_subset(subset_name, unicode_range, target_folder):
    # Load the font and check character coverage first
    options = subset.Options()
    options.flavor = 'woff2'
    options.layout_features = ['*']
    
    font = subset.load_font(INPUT_FONT, options)
    
    # Get set of all unicodes in the font
    font_unicodes = set()
    for table in font['cmap'].tables:
        font_unicodes.update(table.cmap.keys())
    
    # Parse the requested subset range
    requested_unicodes = subset.parse_unicodes(unicode_range)
    
    # Check for intersection
    intersection = font_unicodes.intersection(requested_unicodes)
    if not intersection:
        font.close()
        return None # Indicate skipping

    # Proceed with subsetting if characters exist
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=requested_unicodes)
    subsetter.subset(font)
    
    family_clean = sanitize_name(FONT_FAMILY)
    output_filename = f"{family_clean}_{subset_name}.woff2"
    output_path = target_folder / output_filename
    
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
        try:
            filename = create_subset(name, unicode_range, dist_path)
            
            if filename:
                print(f"Generated: {FONT_FAMILY} ({name})")
                css_entries.append({
                    "subset_name": name,
                    "file": filename,
                    "range": unicode_range
                })
            else:
                print(f"Skipped: {name} (No matching characters in source font)")
                
        except Exception as e:
            print(f"Error processing {name}: {e}")

    generate_css(css_entries, dist_path)
    print(f"\nCompleted! Generated {len(css_entries)} files in /{OUTPUT_DIR}:")

if __name__ == "__main__":
    main()
