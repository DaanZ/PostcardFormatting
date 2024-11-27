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


# Draw Multi-Line Text
def draw_multiline_text(c, text, x, y, font, size, page_height):
    lines = text.split("\n")
    c.setFont(font, size)
    line_height = size * 1.2  # Adjust line height

    # Optionally add a starting margin for the text
    adjusted_y = page_height - y  # Adjust the starting point
    print(x, adjusted_y)
    for line in lines:
        text = line.replace("\\n", "")
        print(text)
        c.drawString(x, adjusted_y, text)
        adjusted_y -= line_height  # Move to the next line


# Generate PDF using ReportLab
def generate_pdf(template, output_pdf, texts):
    elements = parse_pdfml(template, texts)
    print(elements)
    page_width, page_height = landscape(A5)  # Get the page size
    print("page", page_width, page_height)
    c = canvas.Canvas(output_pdf, pagesize=(page_width, page_height))

    line_x = 1050 / MM2PIXEL
    line_start_y = (100 / MM2PIXEL)
    line_end_y = page_height - line_start_y
    c.line(line_x, line_start_y, line_x, line_end_y)  # Draw the vertical line

    for el in elements:
        if el["type"] == "text":
            print(el["content"])
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
    texts = ["""Hello!

Greetings from Middle Earth!
It’s been a fantastic vacation so far
(except for the glowing eye in my host’s backyard),
and I’m really loving the second breakfasts.
Take care,

F.""", """Bob Smith
1234 First Street
Anytown, XX
A COUNTRY"""]
    generate_pdf(template_file, output_pdf_file, texts)
    print(f"PDF generated: {output_pdf_file}")
