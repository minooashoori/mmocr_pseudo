from mmocr.apis import MMOCRInferencer
from mmocr.utils.polygon_utils import poly2bbox
import numpy as np


image_filename = '/home/ubuntu/dev/data/whole/images/val/A_A_A_A_000000528.jpg'
output_directory = '/home/ubuntu/mmocr/test_output'
ocr = MMOCRInferencer(det='DBNetpp', device='cuda:0')
ocr(image_filename, out_dir=output_directory, save_pred=True, save_vis=True)
