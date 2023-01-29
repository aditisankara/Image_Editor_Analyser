import numpy as np
from PIL import Image
from scipy import ndimage

def crop_image(to_crop):

    img_fp = to_crop[0]
    crop_coord = to_crop[1]

    # Open the image file
    im = Image.open(img_fp)

    # Convert the image to a numpy array
    im_array = np.array(im)

    # Define the coordinates of the area you want to crop
    x1, y1, x2, y2 = crop_coord

    # Crop the image using numpy array slicing
    cropped_im_array = im_array[y1:y2, x1:x2]

    # Convert the cropped numpy array back to an image and save it
    cropped_im = Image.fromarray(cropped_im_array)
    new_fp = new_fp_name(img_fp)
    cropped_im.save(new_fp)
    return new_fp


def resize_image(to_resize):
    img_fp = to_resize[0]
    desired_pixels = to_resize[1]
    print('desired = ', desired_pixels)
    # open the image
    im = Image.open(img_fp)
    width, height = im.size

    # calculate new width and height
    scale = np.sqrt(int(desired_pixels) / (width * height))
    new_width = int(scale * width)
    new_height = int(scale * height)

    resized_im = np.array(im.resize((new_width, new_height)))

    new_fp = new_fp_name(img_fp)
    Image.fromarray(resized_im).save(new_fp)
    return new_fp

def rotate_image(to_rotate):
    img_fp = to_rotate
    im = Image.open(to_rotate)
    im_np = np.array(im)
    rotated_im = np.rot90(im_np, 1)
    
    new_fp = new_fp_name(img_fp)
    Image.fromarray(rotated_im).save(new_fp)
    return new_fp

def change_brightness(to_change_brightness):
    img_fp = to_change_brightness[0]
    brightness = to_change_brightness[1]

    im = Image.open(img_fp)
    im_np = np.array(im)

    # adjust the brightness
    im_np_bright = (im_np) * (1+np.float32(brightness))

    # clip the values to 0-255
    im_np_bright = np.clip(im_np_bright, 0, 255)

    # convert to image
    im_bright = Image.fromarray(im_np_bright.astype(np.uint8))

    new_fp = new_fp_name(img_fp)
    im_bright.save(new_fp)
    return new_fp


def median_noise_remove(to_noise_rm):
    img_fp = to_noise_rm 
    # Open the image
    im = Image.open(img_fp)
    im_np = np.array(im)

    filtered_im = ndimage.median_filter(im_np, 3)
    filtered_im = Image.fromarray(filtered_im)
    
    new_fp = new_fp_name(img_fp)
    filtered_im.save(new_fp)
    return new_fp

# def gauss_noise_remove(to_noise_rm):
#     img_fp = to_noise_rm

#     im = Image.open(img_fp)
#     im_np = np.array(im)

#     filtered_im = ndimage.gaussian_filter(im, sigma=1)
#     filtered_im = Image.fromarray(filtered_im)
    
#     new_fp = new_fp_name(img_fp)
#     filtered_im.save(new_fp)
#     print('applied gauss fil')
#     return new_fp



def new_fp_name(old_fp):
    if('_edited' in old_fp):
        return old_fp
    else:
        new_fp = old_fp[:-4] + '_edited.jpg'
        return new_fp

