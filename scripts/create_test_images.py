"""
Create test images for script generator.

This script creates test images for testing the script generator functionality.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def create_test_image(
    width=800, height=600, text="DemoMaker", color=(100, 100, 255), output_path=None
):
    """Create a simple test image with text."""
    # Create a new image
    img = Image.new("RGB", (width, height), color=color)
    draw = ImageDraw.Draw(img)

    # Try to get a font
    font_size = 60
    try:
        font = ImageFont.truetype("Arial", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("DejaVuSans", font_size)
        except IOError:
            font = ImageFont.load_default()

    # Calculate text position to center it
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Draw text
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)

    # Draw a rectangle
    rect_size = 100
    rect_x = width // 2 - rect_size // 2
    rect_y = height // 2 + text_height
    draw.rectangle(
        [rect_x, rect_y, rect_x + rect_size, rect_y + rect_size],
        outline=(255, 255, 255),
        width=3,
    )

    # Save the image
    if output_path:
        img.save(output_path)

    return img


def main():
    """Create test images for script generator testing."""
    # Define output directory
    output_dir = Path(__file__).parent.parent / "data" / "test_images"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Clear existing test images
    for f in output_dir.glob("test*.png"):
        f.unlink()

    # Create test images
    print(f"Creating test images in {output_dir}")

    # Test image 1
    img1_path = output_dir / "test1.png"
    create_test_image(
        width=800,
        height=600,
        text="DemoMaker",
        color=(100, 100, 255),
        output_path=img1_path,
    )
    print(f"Created {img1_path}")

    # Test image 2
    img2_path = output_dir / "test2.png"
    create_test_image(
        width=800,
        height=600,
        text="Script Generator",
        color=(100, 150, 200),
        output_path=img2_path,
    )
    print(f"Created {img2_path}")

    # Test image 3
    img3_path = output_dir / "test3.png"
    create_test_image(
        width=800,
        height=600,
        text="AI Integration",
        color=(150, 100, 200),
        output_path=img3_path,
    )
    print(f"Created {img3_path}")

    print("Done creating test images")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
