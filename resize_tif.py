from PIL import Image
import gdal
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def resize_raw(file):
    output = file[:-4] + '_tn.tif'
    im = Image.open(file)
    im = im.convert("RGBX")
    im.thumbnail((500, 500))
    im.save(output)
    return output


def colormap():
    return mpl.colors.LinearSegmentedColormap.from_list('cmap', ['#FFFFFF','#bde5ef','#c2c7c8','#287ab9','#08306b'])

def resize_tif_result(file):
    output = file[:-4] + '_tn.tif'
    src_ds = gdal.Open(file, gdal.GA_ReadOnly)
    classified_image_data = src_ds.ReadAsArray()
    plt.figure(figsize=(8, 8))
    plt.axis('off')
    # imgplot = plt.imshow(classified_image_data, colormap())
    plt.imsave(output, classified_image_data, cmap = colormap())
    return output


path = 'C:/Users/dsha/Documents/workspace/arcci_image/arcci-backend/arcciNew/static/media/uploads/'
tif_file = path + 'DMS_1842638_01372_20180406_15080202.tif'
result_file = path + 'classified/DMS_1842638_01372_20180406_15080202_classified.tif'
print(resize_raw(tif_file))