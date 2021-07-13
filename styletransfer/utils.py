from PIL import Image  # to read images
import base64

from PIL import Image
from io import BytesIO
import re

from django.conf import settings
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile

def cropImageTargetCoordinate(root_img, box):

   # get dimensions of input image

    width, height = root_img.size
    bbox = bounding_box(width, height, box)

    # im.crop((left, top, right, bottom))
    result_img = root_img.crop(bbox)

    return result_img

def bounding_box(original_width, original_height, box):

    # Left coordinate = BoundingBox.Left * image width
    # Top coordinate = BoundingBox.Top * image height
    # Face width = BoundingBox.Width * image width
    # Face height = BoundingBox.Height * image height

    left = original_width * box['Left']
    top = original_height * box['Top']
    right = left + original_width * box['Width']
    bottom = top + original_height * box['Height']

    # (left, top, right, bottom)
    return (left, top, right, bottom)


def image_to_base64(img):
    with Image.open(img) as image_file:
        buffered = BytesIO()
        image_file.save(buffered, format="JPEG")
        image_bytes = base64.b64encode(buffered.getvalue())
        return image_bytes.decode("utf-8")

def base64_to_image(base64_str, image_path=None):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    if image_path:
        img.save(image_path)
    return img


def storeImageIntoDB(selectedModel, raw_img, img_format = 'JPEG'):
                        
    new_img = selectedModel()
    pil_img = base64_to_image(raw_img)
    img_io = BytesIO()
    pil_img.save(img_io, format = img_format)

    cur_time = str(timezone.now()).split('.')[0]
    new_img.file_path = InMemoryUploadedFile(img_io, field_name=None, name = cur_time + '.jpg', 
        content_type='image/jpeg', size=img_io.tell, charset=None)

    new_img.create_date = timezone.now()
    new_img.save()