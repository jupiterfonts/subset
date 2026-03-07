# Jupiter Fonts Subset Templates
A set of Python script templates for generating subset font files (variable and static) similar to how Google Fonts does it.

**NOTE:** You need `fonttools` and `brotli` installed on your system for the scripts to work. We have included three (3) different scripts for you to use: two (2) variable (one for widths) and one (1) static along with two (2) pre-packaged subset libraries:
 - A Google Fonts-like set of ranges (not the full list of ranges available from Google Fonts; we will add more as we find the need to)
 - The Adeotype Subset Standard (outputs typically fewer, larger files but is more complete for any character set)

All scripts contain fallback code that places any extra non-included glyphs into an orphaned `others` font. If you do not wish to use this font, simply delete the `FONTFAMILY_others.woff2` font file and any calls to it in the generated `font.css` file.

## Copyright
The Python code used in these script templates are Copyright &copy; 2025-onwards the Jupiter Group.

The **Adeotype Subset Standard** is Copyright &copy; 2025-onwards Adeotype (https://adeotype.pages.dev/). All Rights Reserved.

## Licensing
These scripts and pre-defined libraries are currently free for public use and modification, but are not redistributable. They are **not** open-source, rather *source available*.
