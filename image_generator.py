from leonardo import generate_leonardo


class ImageGenerator:

    def __init__(self, provider: str = "leonardo", width: int = 1024, height: int = 1024, high_quality: bool = False):
        self.provider = provider
        self.width = width
        self.height = height
        self.high_quality = high_quality

    def generate(self, query: str, amount: int = 4):
        if self.provider == "leonardo":
            return generate_leonardo(query, amount, self.width, self.height, alchemy=self.high_quality)
        else:
            raise Exception("Unknown image provider:", self.provider)


if __name__ == "__main__":
    generating = "Someone slumping over their desk because there are so many emails on their inbox"
    image_generator = ImageGenerator(high_quality=True)
    images = image_generator.generate(generating, 4)
    for image in images:
        print(image)
