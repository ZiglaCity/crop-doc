from PIL import Image
import io

def read_imagefile(file) -> Image.Image:
    image = Image.open(io.BytesIO(file)).convert('RGB')
    return image
