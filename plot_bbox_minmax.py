import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Path to your image file
image_path = '/home/ubuntu/train2014/COCO_train2014_000000003941.jpg'

# List of bounding box coordinates [(xmin, ymin, xmax, ymax), ...]
bounding_boxes = [[212.5, 98.0, 9.3, 13.1]]
# Load the image
image = Image.open(image_path)

# Create figure and axes
fig, ax = plt.subplots()

# Display the image
ax.imshow(image)

# Plot each bounding box
for bbox in bounding_boxes:
    # Extract coordinates
    xmin, ymin, xmax, ymax = bbox
    # Calculate width and height
    width = xmax - xmin
    height = ymax - ymin
    # Create a Rectangle patch
    bbox_patch = patches.Rectangle((xmin, ymin), width, height, linewidth=2, edgecolor='b', facecolor='none')
    # Add the bounding box to the plot
    ax.add_patch(bbox_patch)

# Set axis limits to match the image dimensions
ax.set_xlim(0, image.width)
ax.set_ylim(image.height, 0)  # Invert y-axis to match image coordinates

# Save the plot to a file
plt.savefig('output_image_with_bboxes.jpg')

# Show the plot
plt.show()
