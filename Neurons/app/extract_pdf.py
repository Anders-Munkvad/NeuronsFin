import fitz  # PyMuPDF
from io import BytesIO

def extract_font_styles(pdf_path):
    doc = fitz.open(stream=BytesIO(pdf_path), filetype="pdf")
    font_styles = {}

    for page in doc:
        text = page.get_text()
        lines = text.splitlines()

        for i, line in enumerate(lines):
            if line.strip().lower() == "primary" and i + 1 < len(lines):
                font_styles["Primary"] = lines[i + 1].strip()
            elif line.strip().lower() == "secondary" and i + 1 < len(lines):
                font_styles["Secondary"] = lines[i + 1].strip()

    doc.close()
    return font_styles

def extract_logo_safezone_styles(pdf_path):
    doc = fitz.open(stream=BytesIO(pdf_path), filetype="pdf")
    logo_safezone = {}

    for page in doc:
        text = page.get_text()
        if "the safe zone" in text.lower():
            lines = text.splitlines()
            buffer = []
            found_section = False

            for i, line in enumerate(lines):
                if "the safe zone" in line.lower():
                    found_section = True
                    buffer.append(line.strip())
                    continue
                if found_section:
                    # Stop if we've reached a new section (heuristic: a blank line or unrelated header)
                    if line.strip() == "" or line.strip().lower() in ["yes", "no"]:
                        break
                    buffer.append(line.strip())

            # Join the buffer into a paragraph
            safezone_text = " ".join(buffer)

            # Extract value and requirements from the paragraph
            if "x is" in safezone_text.lower():
                # Extract the value using a simple split
                value_part = next((s for s in safezone_text.split(".") if "x is" in s.lower()), "").strip()
                logo_safezone["Value"] = value_part

            # Everything else is the requirement
            requirement_part = safezone_text.replace(value_part, "").strip()
            logo_safezone["Requirements"] = requirement_part

            break  # Stop after first match

    doc.close()
    return logo_safezone

def extract_logo_colours(pdf_path):
    doc = fitz.open(stream=BytesIO(pdf_path), filetype="pdf")
    logo_colour = {"Logo colours": []}

    for page in doc:
        text = page.get_text()
        lines = text.splitlines()

        if "primary" in text:
            for line in lines:
                # Just simply check if a line starts with "#" - if it does, we assume it is a colour and we append it. There is a large palette of colours, so we just extract each one, and return them in a dict.
                if line.strip().startswith("#"):
                    logo_colour["Logo colours"].append(line.strip())

    doc.close()
    return logo_colour

def extract_palette_styles(pdf_path):
    doc = fitz.open(stream=BytesIO(pdf_path), filetype="pdf")
    logo_colour_palette = {"Colours": []}

    for page in doc:
        text = page.get_text()
        lines = text.splitlines()

        for line in lines:
            # Just simply check if a line starts with "#" - if it does, we assume it is a colour and we append it. There is a large palette of colours, so we just extract each one, and return them in a dict.
            if line.strip().startswith("#"):
                logo_colour_palette["Colours"].append(line.strip())

    doc.close()
    return logo_colour_palette

# The function that will be used in the API
# Make it more readable what each is? Just return a string along with it?
def extract_brand_compliance(pdf_bytes):
    return {
        "font_styles": extract_font_styles(pdf_bytes),
        "logo_safezone": extract_logo_safezone_styles(pdf_bytes),
        "logo_colour": extract_logo_colours(pdf_bytes),
        "logo_colour_palette": extract_palette_styles(pdf_bytes)
    }
