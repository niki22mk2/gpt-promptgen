from PIL import Image
from io import BytesIO
import base64

def resize_image(image, max_size=(768, 768)):
    """画像をリサイズし、アスペクト比を維持しながら指定された最大サイズに収める"""
    image.thumbnail(max_size, Image.LANCZOS)
    return image

def image_to_base64(image):
    """PIL Imageオブジェクトをbase64エンコードされた文字列に変換"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def process_reference_image(reference_image, max_size=(768, 768)):
    """参照画像を処理し、リサイズしてbase64エンコードする"""
    if reference_image:
        resized_image = resize_image(reference_image, max_size)
        return image_to_base64(resized_image)
    return None