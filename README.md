# Automated-Cell-counting-Analyzer
Automated Cell Counting and Morphology Analysis using Python

# Automated Cell Counting & Morphology Analyzer

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
