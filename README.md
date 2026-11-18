
# Automated Cell Counting & Morphology Analyzer
Automated Cell Counting and Morphology Analysis using Python

## 1. Introduction

The Automated Cell Counting & Morphology Analyzer is a Python-based image processing project designed to automatically detect, count, and analyze cells from microscopy images.

The system processes microscopy images using image preprocessing, thresholding, and watershed segmentation techniques. It identifies individual cells and calculates their morphological properties.

This project is developed for educational purposes to demonstrate the application of digital image processing in biological image analysis.

## 2. Objectives

- To automate cell detection and counting.
- To reduce manual effort in cell counting.
- To identify individual cells in microscopy images.
- To measure morphological characteristics of detected cells.
- To generate visual and numerical analysis reports.

## 3. Features

- Supports PNG, JPG, JPEG, TIFF, and BMP image formats.
- Converts input images into grayscale.
- Applies Gaussian Blur for noise reduction.
- Uses Otsu's thresholding for image segmentation.
- Uses morphological operations for image processing.
- Applies Watershed Algorithm for separating touching cells.
- Automatically counts detected cells.
- Calculates cell area, perimeter, and circularity.
- Calculates equivalent diameter and centroid coordinates.
- Generates annotated output images.
- Exports cell measurements into CSV format.
- Generates a cell area distribution histogram.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Main programming language |
| OpenCV | Image processing and segmentation |
| NumPy | Numerical operations |
| Pandas | Measurement data and CSV export |
| Matplotlib | Graph and histogram generation |
| Scikit-image | Listed image-processing dependency |

## 5. System Workflow

1. Input microscopy image.
2. Convert image into grayscale.
3. Apply Gaussian Blur.
4. Perform Otsu thresholding.
5. Apply morphological opening.
6. Calculate distance transform.
7. Identify foreground and background regions.
8. Apply Watershed segmentation.
9. Detect and count individual cells.
10. Calculate morphological measurements.
11. Generate CSV and image reports.

## 6. Morphological Measurements

The system calculates the following properties:

### Cell Area
The number of pixels occupied by an individual detected cell.

### Cell Perimeter
The length of the detected cell boundary in pixels.

### Circularity
Measures how closely the detected cell resembles a circle.

Formula:

Circularity = 4 × π × Area / Perimeter²

### Equivalent Diameter
The diameter of a circle having the same area as the detected cell.

### Centroid
The approximate center coordinates (X, Y) of a detected cell.

## 7. Project Structure

```text
Automated-Cell-counting-Analyzer/
│
├── main.py
├── requirements.txt
├── README.md
├── sample_cells.png.jpeg
│
└── results/
    ├── cell_measurements.csv
    ├── detected_cells.png
    └── cell_area_distribution.png
```

## 8. Installation Requirements

Python 3.12 or later compatible environment is required.

Install the required libraries:

```bash
py -m pip install -r requirements.txt
```

## 9. How to Run the Project

Run the program using the following command:

```bash
py main.py --image "sample_cells.png.jpeg"
```

To specify a minimum cell area:

```bash
py main.py --image "sample_cells.png.jpeg" --min-area 50
```

## 10. Output Files

The program generates the following outputs inside the results folder:

- **cell_measurements.csv:** Contains measurements of detected cells.
- **detected_cells.png:** Displays detected cells with outlines and labels.
- **cell_area_distribution.png:** Shows the distribution of detected cell areas.

## 11. Sample Execution Result

The program was tested using the provided sample microscopy image.

```text
===== CELL ANALYSIS REPORT =====
Total Cells: 243
Average Area: 378.63
Average Circularity: 0.3393
================================
```

Note: These values represent the output from the tested sample image and may vary depending on the input image.

## 12. Limitations

- Detection accuracy depends on image quality and contrast.
- Overlapping or touching cells may affect segmentation.
- Thresholding parameters may need adjustment for different images.
- Measurements are pixel-based and do not represent physical dimensions without image calibration.

## 13. Conclusion

The Automated Cell Counting & Morphology Analyzer demonstrates how image processing techniques can be used to automate cell counting and basic morphological analysis.

The project successfully generates cell detection images, numerical measurements, and graphical reports from microscopy images.

This application is intended for educational and experimental purposes only and is not designed for medical diagnosis.
main.py – Complete Python code

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from pathlib import Path


def load_image(image_path):
    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError("Image could not be loaded.")

    return image


def preprocess_image(image):
    # Convert image into grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove noise using Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    return blurred


def segment_cells(image):
    # Apply Otsu thresholding
    _, binary = cv2.threshold(
        image, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Morphological operations
    kernel = np.ones((3, 3), np.uint8)

    opening = cv2.morphologyEx(
        binary, cv2.MORPH_OPEN, kernel, iterations=2
    )

    sure_background = cv2.dilate(
        opening, kernel, iterations=3
    )

    # Distance transformation
    distance = cv2.distanceTransform(
        opening, cv2.DIST_L2, 5
    )

    _, sure_foreground = cv2.threshold(
        distance,
        0.35 * distance.max(),
        255,
        cv2.THRESH_BINARY
    )

    sure_foreground = np.uint8(sure_foreground)

    unknown = cv2.subtract(
        sure_background, sure_foreground
    )

    # Connected components
    _, markers = cv2.connectedComponents(
        sure_foreground
    )

    markers = markers + 1
    markers[unknown == 255] = 0

    # Watershed algorithm
    markers = cv2.watershed(
        cv2.cvtColor(image, cv2.COLOR_GRAY2BGR),
        markers
    )

    return markers


def measure_cells(markers, min_area=50):

    measurements = []

    for label in np.unique(markers):

        if label <= 1:
            continue

        mask = np.uint8(markers == label)

        area = cv2.countNonZero(mask)

        if area < min_area:
            continue

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            continue

        contour = max(contours, key=cv2.contourArea)

        perimeter = cv2.arcLength(contour, True)

        moments = cv2.moments(mask)

        if moments["m00"] == 0:
            continue

        cx = moments["m10"] / moments["m00"]
        cy = moments["m01"] / moments["m00"]

        # Calculate circularity
        circularity = (
            4 * np.pi * area / (perimeter ** 2)
            if perimeter > 0 else 0
        )

        # Equivalent diameter
        diameter = np.sqrt(4 * area / np.pi)

        measurements.append({
            "Cell ID": len(measurements) + 1,
            "Area": area,
            "Perimeter": round(perimeter, 2),
            "Circularity": round(circularity, 4),
            "Equivalent Diameter": round(diameter, 2),
            "Centroid X": round(cx, 2),
            "Centroid Y": round(cy, 2)
        })

    return pd.DataFrame(measurements)


def save_detected_image(image, markers, df, output_folder):

    output_image = image.copy()

    for label in np.unique(markers):

        if label <= 1:
            continue

        mask = np.uint8(markers == label)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        cv2.drawContours(
            output_image,
            contours,
            -1,
            (0, 255, 0),
            2
        )

    for row in df.itertuples():

        x = int(row._6)
        y = int(row._7)

        cv2.circle(
            output_image, (x, y), 3, (0, 0, 255), -1
        )

    cv2.imwrite(
        str(output_folder / "detected_cells.png"),
        output_image
    )


def save_histogram(df, output_folder):

    plt.figure(figsize=(8, 5))

    if not df.empty:
        plt.hist(
            df["Area"],
            bins=20,
            edgecolor="black"
        )

    plt.title("Cell Area Distribution")
    plt.xlabel("Cell Area (Pixels)")
    plt.ylabel("Number of Cells")

    plt.tight_layout()

    plt.savefig(
        output_folder / "cell_area_distribution.png"
    )

    plt.close()


def main():

    parser = argparse.ArgumentParser(
        description="Automated Cell Counting Analyzer"
    )

    parser.add_argument(
        "--image",
        required=True,
        help="Input microscopy image"
    )

    parser.add_argument(
        "--min-area",
        type=int,
        default=50
    )

    args = parser.parse_args()

    output_folder = Path("results")
    output_folder.mkdir(exist_ok=True)

    # Load image
    image = load_image(args.image)

    # Preprocessing
    gray = preprocess_image(image)

    # Cell segmentation
    markers = segment_cells(gray)

    # Morphological measurements
    df = measure_cells(markers, args.min_area)

    # Save CSV file
    df.to_csv(
        output_folder / "cell_measurements.csv",
        index=False
    )

    # Save detected image
    save_detected_image(
        image, markers, df, output_folder
    )

    # Save histogram
    save_histogram(df, output_folder)

    # Display report
    print("\n===== CELL ANALYSIS REPORT =====")

    print("Total Cells:", len(df))

    if not df.empty:

        print(
            "Average Area:",
            round(df["Area"].mean(), 2)
        )

        print(
            "Average Circularity:",
            round(df["Circularity"].mean(), 4)
        )

    print("\nAnalysis Completed Successfully!")


if __name__ == "__main__":
    main()
