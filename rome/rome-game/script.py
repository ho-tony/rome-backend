from PIL import Image, ImageFilter
from rembg import remove
import io

def make_square(img, background_color=(255, 255, 255, 0)):
    """
    Pads the image to make it square by adding a background color.

    :param img: PIL.Image object.
    :param background_color: Tuple specifying the background color. Default is transparent.
    :return: Square PIL.Image object.
    """
    width, height = img.size
    if width == height:
        return img
    max_side = max(width, height)
    new_img = Image.new('RGBA', (max_side, max_side), background_color)
    new_img.paste(img, ((max_side - width) // 2, (max_side - height) // 2))
    print(f"Padded image to square size: {new_img.size}")
    return new_img

def resize_image_then_remove_bg(input_path, output_path, size=(16, 16)):
    """
    Resizes an image to the specified size and then removes its background using high-quality processing to minimize artifacts.

    :param input_path: Path to the input image file.
    :param output_path: Path where the processed image will be saved.
    :param size: A tuple specifying the target size, default is (16, 16).
    """
    try:
        # Open the input image using PIL
        with Image.open(input_path) as img:
            print(f"Original size: {img.size}, mode: {img.mode}")

            # Convert image to RGBA if it's not already in a suitable mode
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")
                print(f"Converted image mode to: {img.mode}")

            # Make the image square to preserve aspect ratio (optional)
            img = make_square(img)

            # Perform high-quality resizing using LANCZOS filter
            resized_img = img.resize(size, Image.LANCZOS)
            print(f"Resized image to: {resized_img.size}")

            # Apply sharpening to enhance details
            resized_img = resized_img.filter(ImageFilter.SHARPEN)
            print("Applied sharpening filter.")

            # Save the resized image to a bytes buffer in PNG format
            img_byte_arr = io.BytesIO()
            resized_img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            print("Resized image saved to bytes buffer.")

        # Remove the background using rembg
        output_image_bytes = remove(img_byte_arr)
        print("Background removal completed.")

        # Convert the byte data back to a PIL Image
        output_image = Image.open(io.BytesIO(output_image_bytes)).convert("RGBA")
        print(f"Image mode after background removal: {output_image.mode}")

        # Save the final image
        output_image.save(output_path, format='PNG', optimize=True)
        print(f"Final image with background removed saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_image_path = "projectile.png"      # Path to your input image
    output_image_path = "converted.png"     # Path where the output image will be saved
    resize_image_then_remove_bg(input_image_path, output_image_path, size=(16, 16))

