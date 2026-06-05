import cv2
import numpy as np
import sys


def load_image(path):
    """Loads an image from the given file path."""
    image = cv2.imread(path)
    if image is None:
        print(f"Error: Could not load image from '{path}'.")
        sys.exit(1)
    return image


def show_result(original, cartoon):
    """Displays the original and cartoon images side by side and saves the output."""
    h = 500
    scale = h / original.shape[0]
    w = int(original.shape[1] * scale)

    orig_resized = cv2.resize(original, (w, h))
    cart_resized = cv2.resize(cartoon, (w, h))

    combined = np.hstack([orig_resized, cart_resized])

    cv2.putText(combined, "Original", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(combined, "Cartoon", (w + 10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Cartoon Filter", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite("cartoon_output.jpg", cart_resized)
    print("Saved output to cartoon_output.jpg")


def smooth_image(image):
    """
    Apply a Gaussian blur to the image to reduce noise.
    Use a kernel size of (9, 9).

    Returns the blurred image.
    """
    pass


def get_edges(image):
    """
    Detect edges in the image and return a clean binary edge mask.

    Steps:
        1. Convert the image to grayscale.
        2. Apply a small Gaussian blur with kernel size (5, 5).
        3. Run Canny edge detection with thresholds 50 and 150.
        4. Threshold the result: any pixel > 0 should become 255.
           Use cv2.THRESH_BINARY for this.

    Returns a single-channel binary image (white edges on black background).
    """
    pass


def apply_cartoon_effect(original, edges):
    """
    Overlay the edge mask onto the original image to produce a cartoon effect.

    Steps:
        1. Invert the edge mask using cv2.bitwise_not so edges become black
           lines on a white background.
        2. Convert the single-channel mask to 3 channels (BGR) using
           cv2.cvtColor with cv2.COLOR_GRAY2BGR, so it matches the
           shape of the original image.
        3. Use cv2.bitwise_and on the original image and the mask to
           burn the black edge lines into the colour image.

    Returns the final cartoon image.
    """
    pass


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cartoon_filter.py <path_to_image>")
        sys.exit(1)

    original = load_image(sys.argv[1])

    smoothed = smooth_image(original)
    edges = get_edges(smoothed)
    cartoon = apply_cartoon_effect(original, edges)

    show_result(original, cartoon)
