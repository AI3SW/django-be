from PIL import Image  # to read images


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