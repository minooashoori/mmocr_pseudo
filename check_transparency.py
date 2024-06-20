import cv2

# # Load the image
# image = cv2.imread('COCO_train2014_000000014446.jpg', cv2.IMREAD_UNCHANGED)

# # Check for transparency
# if image.shape[2] == 4:  # RGBA image
#     # Split channels
#     b, g, r, alpha = cv2.split(image)

#     # Merge RGB channels
#     image_rgb = cv2.merge((b, g, r))

#     # Display the original and RGB image
#     cv2.imshow('Original Image', image)
#     cv2.imshow('RGB Image', image_rgb)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print("The image doesn't contain transparency.")


# Load the image
image = cv2.imread('COCO_train2014_000000014446.jpg', cv2.IMREAD_UNCHANGED)

# Check if the image is loaded successfully
if image is not None:
    # Get dimensions
    height, width = image.shape[:2]
    print("Image dimensions (height, width):", height, "x", width)

    # Get number of channels
    num_channels = image.shape[2] if len(image.shape) == 3 else 1
    print("Number of channels:", num_channels)

else:
    print("Error: Image not loaded.")

