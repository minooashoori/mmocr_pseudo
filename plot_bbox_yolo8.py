import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

# #def yolo_to_xyxy(yolo_coords, image_width, image_height):
# def yolo_to_xyxy(yolo_coords, image_width, image_height):
#     x_min, y_min, width, height = yolo_coords
#     xmin = x_min * 0.01  * image_width  # Convert from percentage to normalized value
#     ymin = y_min * 0.01 * image_height  # Convert from percentage to normalized value
#     xmax = (x_min * 0.01  + width * 0.01) * image_width * 0.01  # Convert from percentage to normalized value
#     ymax = (y_min * 0.01 + height * 0.01 )*image_height * 0.01 # Convert from percentage to normalized value
    
#     return xmin, xmax, ymin, ymax
#def yolo_to_xyxy(yolo_coords, image_width, image_height):
# def yolo_to_xyxy(yolo_coords, image_width, image_height):
#     x_min, y_min, width, height = yolo_coords
#     xmin = (x_min - width/2)  * image_width  # Convert from percentage to normalized value
#     ymin = (y_min - height/2)  * image_height  # Convert from percentage to normalized value
#     xmax = (x_min  + width/2 ) * image_width   # Convert from percentage to normalized value
#     ymax = (y_min  + height/2 )*image_height  # Convert from percentage to normalized value
    
#     return xmin, xmax, ymin, ymax
# def yolo_to_xyxy(yolo_coords, image_width, image_height):
#     x_min, y_min, width, height = yolo_coords
#     xmin = (x_min )    # Convert from percentage to normalized value
#     ymin = (y_min )    # Convert from percentage to normalized value
#     xmax = (x_min  + width)  # Convert from percentage to normalized value
#     ymax = (y_min  + height )  # Convert from percentage to normalized value
    
#     return xmin, xmax, ymin, ymax
def yolo_to_xyxy(yolo_coords, image_width, image_height):
    x_min, y_min, width, height = yolo_coords
    xmin = (x_min - width/2)   # Convert from percentage to normalized value
    ymin = (y_min - height/2)   # Convert from percentage to normalized value
    xmax = (x_min  + width/2 )   # Convert from percentage to normalized value
    ymax = (y_min  + height/2 ) # Convert from percentage to normalized value
    
    return xmin, xmax, ymin, ymax
# Load the image
# image = mpimg.imread('/home/ubuntu/val/0_Parade_Parade_0_364.jpg')
# image = mpimg.imread('/home/ubuntu/logo05/yolo/images/test/00000320.jpg')
image = mpimg.imread('/home/ubuntu/train2014/COCO_train2014_000000000036.jpg')
# Bounding box coordinates in YOLOv8 format [x_min, y_min, width, height]
yolov8_bboxes_blue = [[407, 384 ,26 ,7],
[416, 377 ,20 ,6],
[413 ,395 ,22 ,6],
[403, 384 ,15 ,7]



]






# yolov8_bboxes_yellow = [[114.5, 375.5 ,131.0 ,65.0],
# [92.0 ,380.0, 80.0 ,50.0],
# [150.0 ,370.5, 48.0 ,41.0],
# [91.0 ,381.5, 62.0 ,39.0]
    
#     ]
        
# yolov8_bboxes_red = [[92 ,380 ,77, 43]]
   
# Image dimensions
image_width = image.shape[1]
image_height = image.shape[0]

# Plotting
fig, ax = plt.subplots(1)
ax.imshow(image)

# Add blue bounding boxes
for bbox in yolov8_bboxes_blue:
    xmin, xmax, ymin, ymax = yolo_to_xyxy(bbox, image_width, image_height)
    rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='b', facecolor='none')
    ax.add_patch(rect)
    
# for bbox in yolov8_bboxes_yellow:
#     xmin, xmax, ymin, ymax = yolo_to_xyxy(bbox, image_width, image_height)
#     rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='y', facecolor='none')
#     ax.add_patch(rect)

# for bbox in yolov8_bboxes_red:
#     xmin, xmax, ymin, ymax = yolo_to_xyxy(bbox, image_width, image_height)
#     rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='r', facecolor='none')
#     ax.add_patch(rect)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Bounding Boxes')

# Save the image
output_path = "./output_image.jpg"
plt.savefig(output_path)

plt.show()
