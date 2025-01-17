from helper import MM2PIXEL


def character_size(font_size: int = 12):
    return font_size * (1/MM2PIXEL)


def calculate_textbox_size(text: str, font_size: int = 12):
    lines = text.split("\n")
    height = len(lines) * character_size(font_size) * 1.2
    print(font_size, character_size(font_size))
    widths = []
    characters = []
    for line in lines:
        widths.append(len(line) * character_size(font_size))
        characters.append(len(line))

    print(max(characters))
    max_width = max(widths)
    return max_width, height


def find_starting_place(available_width, available_height, width, height):
    if width > available_width:
        return None, None
    if height > available_height:
        return None, None
    margin_top = (available_height - height) / 2
    margin_left = (available_width - width) / 2

    return margin_left, margin_top


def placement(offset_x, offset_y, start_x, start_y):
    return offset_x + start_x, offset_y + start_y


def place_multiline_text(text: str, offset_x: int = 50, offset_y: int = 50, available_width: int = 500, available_height: int = 250, font_size: int = 12):
    max_width, height = calculate_textbox_size(text, font_size)
    print("size", max_width, height)
    left, top = find_starting_place(available_width, available_height, max_width, height)
    if left and top:
        return placement(offset_x, offset_y, left, top)
    else:
        return None, None


def find_maximum_size(text: str, offset_x: int = 50, offset_y: int = 50, available_width: int = 500, available_height: int = 250):
    print(offset_x, offset_y, available_width, available_height)

    for font_size in [96, 48, 36, 32, 28, 24, 20, 16, 14, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]:
        x, y = place_multiline_text(text, offset_x, offset_y, available_width, available_height, font_size)
        if x and y:
            break
    return font_size, x, y


if __name__ == "__main__":
    text = """Hello!

    Greetings from Middle Earth!
    It’s been a fantastic vacation so far
    
    and I’m really loving the second breakfasts.
    Take care,

    F."""
    find_maximum_size(text)

