"""
LaTeX text conversion utilities.

Converts LaTeX markup to Unicode and Markdown for renderer-agnostic output.
- Accents → Unicode characters (data normalization)
- Text formatting → Markdown (**bold**, *italic*, [links](url))
- Math expressions → passed through as $...$ (universal for KaTeX/MathJax)

Copyright (c) 2024 Personal Robotics Laboratory, University of Washington
Author: Siddhartha Srinivasa <siddh@cs.washington.edu>
MIT License - see LICENSE file for details.
"""

import re

# Comprehensive LaTeX accent → Unicode mapping
# Covers the most common accents found in academic BibTeX files.
# Format: both {\\accent{char}} and {\\accent char} variants are handled
# by the replacement logic below.
LATEX_ACCENTS = {
    # Acute accent \'
    "\\'a": "á", "\\'A": "Á",
    "\\'e": "é", "\\'E": "É",
    "\\'i": "í", "\\'I": "Í",
    "\\'o": "ó", "\\'O": "Ó",
    "\\'u": "ú", "\\'U": "Ú",
    "\\'c": "ć", "\\'C": "Ć",
    "\\'n": "ń", "\\'N": "Ń",
    "\\'s": "ś", "\\'S": "Ś",
    "\\'z": "ź", "\\'Z": "Ź",
    "\\'y": "ý", "\\'Y": "Ý",
    # Grave accent \`
    "\\`a": "à", "\\`A": "À",
    "\\`e": "è", "\\`E": "È",
    "\\`i": "ì", "\\`I": "Ì",
    "\\`o": "ò", "\\`O": "Ò",
    "\\`u": "ù", "\\`U": "Ù",
    # Umlaut/diaeresis \"
    '\\"a': "ä", '\\"A': "Ä",
    '\\"e': "ë", '\\"E': "Ë",
    '\\"i': "ï", '\\"I': "Ï",
    '\\"o': "ö", '\\"O': "Ö",
    '\\"u': "ü", '\\"U': "Ü",
    '\\"y': "ÿ",
    # Circumflex \^
    "\\^a": "â", "\\^A": "Â",
    "\\^e": "ê", "\\^E": "Ê",
    "\\^i": "î", "\\^I": "Î",
    "\\^o": "ô", "\\^O": "Ô",
    "\\^u": "û", "\\^U": "Û",
    # Tilde \~
    "\\~a": "ã", "\\~A": "Ã",
    "\\~n": "ñ", "\\~N": "Ñ",
    "\\~o": "õ", "\\~O": "Õ",
    # Cedilla \c
    "\\c{c}": "ç", "\\c{C}": "Ç",
    "\\c c": "ç", "\\c C": "Ç",
    # Ring \r
    "\\r{a}": "å", "\\r{A}": "Å",
    # Stroke
    "\\l": "ł", "\\L": "Ł",
    "\\o": "ø", "\\O": "Ø",
    # Caron/háček \v
    "\\v{c}": "č", "\\v{C}": "Č",
    "\\v{s}": "š", "\\v{S}": "Š",
    "\\v{z}": "ž", "\\v{Z}": "Ž",
    "\\v{r}": "ř", "\\v{R}": "Ř",
    "\\v{n}": "ň", "\\v{N}": "Ň",
    "\\v{e}": "ě", "\\v{E}": "Ě",
    # Dot above \.
    "\\.z": "ż", "\\.Z": "Ż",
    # Hungarian umlaut \H
    "\\H{o}": "ő", "\\H{O}": "Ő",
    "\\H{u}": "ű", "\\H{U}": "Ű",
    # Special characters
    "\\ss": "ß",
    "\\ae": "æ", "\\AE": "Æ",
    "\\oe": "œ", "\\OE": "Œ",
    "\\aa": "å", "\\AA": "Å",
    "\\i": "ı",
}


def replace_latex_accents(text: str) -> str:
    """Replace LaTeX accent commands with Unicode characters.

    Handles both {\\accent{char}} and {\\accent char} forms commonly
    found in BibTeX files. Braces around accent commands are also removed.
    """
    if not isinstance(text, str):
        return text

    # Handle braced accent forms like {\\'e} or {\\\"u}
    # These are common in BibTeX: {M{\\"u}ller}
    for latex, uni in LATEX_ACCENTS.items():
        # With braces around the whole command: {\'e}
        text = text.replace("{" + latex + "}", uni)
        # With braces around just the char: \'{e} or \"{u}
        if len(latex) >= 2 and latex[-1].isalpha():
            braced = latex[:-1] + "{" + latex[-1] + "}"
            text = text.replace(braced, uni)
        # Plain form
        text = text.replace(latex, uni)

    return text


def latex_to_markdown(text: str) -> str:
    """Convert LaTeX markup to Markdown.

    - Accents → Unicode
    - \\textbf{...} → **...**
    - \\emph{...} → *...*
    - \\href{url}{text} → [text](url)
    - ^{...} → <sup>...</sup> (HTML passthrough, supported by all Markdown renderers)
    - _{...} → <sub>...</sub> (same)
    - $...$ → $...$ (passed through for KaTeX/MathJax)
    - Remaining curly braces removed
    """
    if not isinstance(text, str):
        return text

    # Protect math expressions from further processing
    math_blocks = []

    def protect_math(m):
        math_blocks.append(m.group(1))
        return f"__MATH{len(math_blocks) - 1}__"

    text = re.sub(r'\$(.*?)\$', protect_math, text)

    # Apply accent replacement
    text = replace_latex_accents(text)

    # LaTeX formatting → Markdown
    text = re.sub(r'\\textbf\{(.*?)\}', r'**\1**', text)
    text = re.sub(r'\\textbf\s*', '', text)  # orphaned \textbf
    text = re.sub(r'\\emph\{(.*?)\}', r'*\1*', text)
    text = re.sub(r'\\textit\{(.*?)\}', r'*\1*', text)
    text = re.sub(r'\\href\{(.*?)\}\{(.*?)\}', r'[\2](\1)', text)
    text = re.sub(r'\\href\{(.*?)\}', r'[\1](\1)', text)

    # Super/subscripts → HTML (universally supported in Markdown)
    text = re.sub(r'\^\{(.*?)\}', r'<sup>\1</sup>', text)
    text = re.sub(r'_\{(.*?)\}', r'<sub>\1</sub>', text)

    # Remove remaining curly braces
    text = text.replace('{', '').replace('}', '')

    # Restore math expressions (kept as $...$ for KaTeX/MathJax)
    def restore_math(m):
        return f"${math_blocks[int(m.group(1))]}$"

    text = re.sub(r'__MATH(\d+)__', restore_math, text)

    return text


def latex_to_text(text: str) -> str:
    """Convert LaTeX to plain text (strip all formatting, keep content).

    Useful for fields where Markdown is not appropriate (e.g., sort keys,
    plain-text exports).
    """
    if not isinstance(text, str):
        return text

    text = replace_latex_accents(text)

    # Strip formatting commands, keep content
    text = re.sub(r'\\textbf\{(.*?)\}', r'\1', text)
    text = re.sub(r'\\textbf\s*', '', text)
    text = re.sub(r'\\emph\{(.*?)\}', r'\1', text)
    text = re.sub(r'\\textit\{(.*?)\}', r'\1', text)
    text = re.sub(r'\\href\{(.*?)\}\{(.*?)\}', r'\2', text)
    text = re.sub(r'\\href\{(.*?)\}', r'\1', text)
    text = re.sub(r'\^\{(.*?)\}', r'\1', text)
    text = re.sub(r'_\{(.*?)\}', r'\1', text)

    # Remove remaining curly braces and math delimiters
    text = text.replace('{', '').replace('}', '')

    return text
