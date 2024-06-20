import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Path to your image file
image_path = '/home/ubuntu/train2014/COCO_train2014_000000262145.jpg'


# List of bounding box coordinates [(xmin, ymin, width, height), ...]
bounding_boxes = [[371.0561688026685 ,271.3129176879197 ,25.168539325842758 ,19.191011235955056]]
image = Image.open(image_path)

# Create figure and axes
fig, ax = plt.subplots()

# Display the image
ax.imshow(image)

# Plot each bounding box
for bbox in bounding_boxes:
    # Create a Rectangle patch
    bbox_patch = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=2, edgecolor='b', facecolor='none')
    # Add the bounding box to the plot
    ax.add_patch(bbox_patch)

# Set axis limits to match the image dimensions
ax.set_xlim(0, image.width)
ax.set_ylim(image.height, 0)  # Invert y-axis to match image coordinates

# Save the plot to a file
plt.savefig('output_image_with_bboxes.jpg')

# Show the plot
plt.show()
