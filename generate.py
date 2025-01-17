from xml.etree import ElementTree as ET
from reportlab.lib.pagesizes import landscape, A5
from reportlab.pdfgen import canvas

from helper import MM2PIXEL
from postcard import find_maximum_size


# Parse PDFML XML Template
def parse_pdfml(file, texts):
    tree = ET.parse(file)
    root = tree.getroot()
    elements = []
    index = 0
    for block in root.findall(".//block"):
        for text in block.findall("text"):
            print(index, texts[index])
            elements.append({
                "type": "text",
                "font": text.attrib.get("font", "Helvetica"),
                "x": float(text.attrib.get("x", 0).replace("mm", "")) / MM2PIXEL,
                "y": float(text.attrib.get("y", 0).replace("mm", "")) / MM2PIXEL,
                "width": float(text.attrib.get("width", 0).replace("mm", "")) / MM2PIXEL,
                "height": float(text.attrib.get("height", 0).replace("mm", "")) / MM2PIXEL,
                "content": texts[index],
            })
            index += 1
        for rect in block.findall("rectangle"):
            elements.append({
                "type": "rectangle",
                "x": float(rect.attrib.get("x", 0).replace("mm", "")) / MM2PIXEL,
                "y": float(rect.attrib.get("y", 0).replace("mm", "")) / MM2PIXEL,
                "width": float(rect.attrib.get("width", 0).replace("mm", "")) / MM2PIXEL,
                "height": float(rect.attrib.get("height", 0).replace("mm", "")) / MM2PIXEL,
                "border": rect.attrib.get("border", "1pt solid #000000"),
            })
    return elements


def find_closest_space(line, start_index):
    """
    Finds the closest space character to the given start index in a string.

    Args:
        line (str): The string to search in.
        start_index (int): The starting index to search around.

    Returns:
        int: The index of the closest space, or -1 if no space is found.
    """
    if not line or start_index < 0 or start_index >= len(line):
        return -1

    left_index = start_index
    right_index = start_index

    while left_index >= 0 or right_index < len(line):
        if left_index >= 0 and line[left_index] == " ":
            return left_index
        if right_index < len(line) and line[right_index] == " ":
            return right_index

        left_index -= 1
        right_index += 1

    return -1  # No space found



# Draw Multi-Line Text
def draw_multiline_text(c, text, x, y, font, size, page_height):
    lines = text.split("\n")
    c.setFont(font, size)
    line_height = size * 1.2  # Adjust line height

    # Optionally add a starting margin for the text
    adjusted_y = page_height - y  # Adjust the starting point
    print(x, adjusted_y)

    maxed_lines = []
    for line in lines:
        while len(line) > 75:
            first_closest_space = find_closest_space(line, 75)
            if first_closest_space > 0:
                maxed_lines.append(line[:first_closest_space])
                line = line[first_closest_space:]
        maxed_lines.append(line)

    for line in maxed_lines:
        text = line.replace("\\n", "")
        print(text)
        c.drawString(x, adjusted_y, text)
        adjusted_y -= line_height  # Move to the next line


# Generate PDF using ReportLab
def generate_pdf(template, output_pdf, texts):
    elements = parse_pdfml(template, texts)
    page_width, page_height = landscape(A5)  # Get the page size
    c = canvas.Canvas(output_pdf, pagesize=(page_width, page_height))

    line_x = 950 / MM2PIXEL
    line_start_y = (100 / MM2PIXEL)
    line_end_y = page_height - line_start_y
    c.line(line_x, line_start_y, line_x, line_end_y)  # Draw the vertical line

    for el in elements:
        if el["type"] == "text":
            size, x, y = find_maximum_size(el["content"], el["x"], el["y"], el["width"], el["height"])
            print(size, x, y)
            draw_multiline_text(c, el["content"], x, y, el["font"], size, page_height)
        elif el["type"] == "rectangle":
            adjusted_y = page_height - el["y"] - el["height"]  # Adjust y to match top-left origin
            c.rect(el["x"], adjusted_y, el["width"], el["height"], stroke=1, fill=0)

    c.save()


# Run the script
if __name__ == "__main__":
    template_file = "template.pdfml"
    output_pdf_file = "postcard.pdf"
    texts = ["""Hello, dear friend!

The house in Washington offers a serene retreat,
Nestled among lush trees and a quiet street.
From cozy fireplaces to spacious rooms,
Every corner exudes warmth and charm, it's your dream come true!
Don't miss the backyard, it's a true gem,
For BBQs, garden parties, and starlit evenings.

Embrace this home, make it your own,
For memories to cherish and stories yet to unfold.

Looking forward to welcoming you to your new abode!""", """Bob Smith
1234 First Street
Anytown, XX
A COUNTRY"""]
    generate_pdf(template_file, output_pdf_file, texts)
    print(f"PDF generated: {output_pdf_file}")
