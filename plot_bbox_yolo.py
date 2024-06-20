import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

# Convert YOLO format coordinates to xmin, xmax, ymin, ymax format
def yolo_to_xyxy(yolo_coords, image_width, image_height):
    x1, y1, x2, y2 = yolo_coords
    xmin = x1 * image_width
    ymin = y1 * image_height
    xmax = x2 * image_width
    ymax = y2 * image_height
    return xmin, xmax, ymin, ymax

# Load the image
image = mpimg.imread('/home/ubuntu/dev/data/whole/images/train/A_A_B_000101589.jpg')

# Bounding box coordinates in YOLO format [x1, y1, x2, y2]
yolo_bboxes = [[0.0000, 0.2455, 0.9856, 0.3234]]


# Image dimensions
image_width = image.shape[1]
image_height = image.shape[0]

# Plotting
fig, ax = plt.subplots(1)
ax.imshow(image)

# Add bounding boxes
for bbox in yolo_bboxes:
    xmin, xmax, ymin, ymax = yolo_to_xyxy(bbox, image_width, image_height)
    rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Bounding Boxes')

# Save the image
output_path = "./output_image.jpg"
plt.savefig(output_path)

plt.show()
