# Task: Cartoon Edge Filter

## Objective

You will build a **cartoon-style edge filter** in Python using OpenCV. Given any image of your choice, your program should detect the outlines/edges of subjects in the image and overlay them on the original — making it look like a hand-drawn cartoon or comic strip.

---

## Background

Many photo filters (like those in Snapchat or Instagram) use simple CV pipelines under the hood. A cartoon filter works by:

1. Smoothing the image to reduce noise
2. Detecting strong edges (outlines of objects/characters)
3. Overlaying those edges onto the original image

You have already learned all the tools you need — blurring, kernels, edge detection, and thresholding. Now it's time to put them together.

---

## What You Need to Do

Complete the three functions in `cartoon_filter.py`:

### `smooth_image(image)`
- Apply a blur to reduce noise before edge detection
- Think about which type of blur preserves edges better than others
- Return the smoothed image

### `get_edges(image)`
- Convert the image to grayscale
- Apply a suitable blur (a smaller one works here)
- Use edge detection to find outlines
- Apply thresholding to get a clean black-and-white edge mask
- Return the edge mask

### `apply_cartoon_effect(original, edges)`
- The edges are currently white lines on black — you need to **invert** them so you get black lines on a white mask
- Use `cv2.bitwise_and` to overlay the edge mask onto the original image
- Return the final cartoon image

---

## Expected Output

Your output should look like the original image but with dark outlines tracing the shapes and subjects — like a cartoon or comic book illustration.

Save and display your result using the provided `show_result()` function.

---

## Tips

- `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` converts to grayscale
- `cv2.bitwise_not(mask)` inverts a binary image
- For `cv2.bitwise_and`, think about what happens when you AND a colour image with a binary mask
- Kernel size must always be **odd** (e.g. 5, 7, 9)
- Try different images — portraits, cartoon characters, and objects with clear outlines work best

---

## Submission

Submit your completed `cartoon_filter.py` along with:
- The original image you used
- A screenshot of your output

---

## Bonus (Optional)

- Try applying a **bilateral filter** for smoothing instead of Gaussian blur — notice any difference?
- Experiment with the Canny thresholds and observe how the edge density changes
- Apply a colour quantisation step to make the image look even more "cartoon-like"
