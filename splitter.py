import re


def split_into_sentences(text):
    # Preprocess to temporarily protect abbreviations
    abbreviations = ["Dr.", "Mr.", "Mrs.", "Ms.", "Jr.", "Sr.", "etc.", "vs.", "St."]
    for abbr in abbreviations:
        text = text.replace(abbr, abbr.replace(".", "<DOT>"))

    # Pattern to match sentence-ending punctuation (., ?, !) followed by whitespace
    pattern = re.compile(r'(?<=[.!?])\s+')

    # Split text into sentences
    sentences = pattern.split(text)

    # Postprocess to restore abbreviations
    sentences = [sentence.replace("<DOT>", ".") for sentence in sentences]

    return sentences


# Example text
text = """
Hey Jamie! 😊

Hope this postcard finds you well in Seattle! 🍃 I'm reaching out because I've come across a fantastic investment opportunity in Texas - a charming house that's full of potential!

If you're interested or know someone who might be, drop me a line. We could catch up and discuss more over a call or email! 

Excited to hear from you!

Warm regards,
[Your Name]
"""

# Split the text into sentences
split_sentences = split_into_sentences(text)

# Print each sentence on a new line
for sentence in split_sentences:
    print(sentence.strip())
