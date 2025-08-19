def build_compliance_prompt_qwen(brand_data: dict) -> str:
    font_styles = brand_data.get("font_styles", {})
    logo_safezone = brand_data.get("logo_safezone", {})
    logo_colours = brand_data.get("logo_colour", {}).get("Logo colours", [])
    colour_palette = brand_data.get("logo_colour_palette", {}).get("Colours", [])

    prompt = (
        "You are a brand compliance assistant. A user has uploaded a marketing image. "
        "Check the image against the following brand guidelines and decide whether it follows them.\n\n"

        "### Instructions\n"
        "1. For each of the four criteria, assign 1 point if satisfied and 0 if not.\n"
        "2. After evaluating all four, return a total score out of 4.\n"
        "3. For each criterion, explain briefly why it passed (✅) or failed (❌).\n\n"

        "### Brand Guidelines\n"
        f"- **Font Styles**\n"
        f"  - Primary font: {font_styles.get('Primary', 'Unknown')}\n"
        f"  - Secondary font: {font_styles.get('Secondary', 'Unknown')}\n\n"

        f"- **Logo Safe Zone**\n"
        f"  - Size: {logo_safezone.get('Value', 'N/A')}\n"
        f"  - Requirements: {logo_safezone.get('Requirements', 'N/A')}\n\n"

        f"- **Approved Logo Colours**\n"
        f"  {', '.join(logo_colours[:10]) + ('...' if len(logo_colours) > 10 else '')}\n\n"

        f"- **Approved Colour Palette (the image should primarily use these colours)**\n"
        f"  {', '.join(colour_palette[:10]) + ('...' if len(colour_palette) > 10 else '')}\n\n"

        "### Response Format\n"
        "- Font Style: ✅/❌ – explanation\n"
        "- Logo Safe Zone: ✅/❌ – explanation\n"
        "- Logo Colour: ✅/❌ – explanation\n"
        "- Colour Palette: ✅/❌ – explanation\n"
        "**Total Score: X/4**"
    )

    return prompt
