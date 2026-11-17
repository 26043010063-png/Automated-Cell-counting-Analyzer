# Automated-Cell-counting-Analyzer
Automated Cell Counting and Morphology Analysis using Python
# Automated Cell Counting & Morphology Analyzer

## Overview
This project is a Python-based image processing application that automatically detects and counts cells in microscopy images. It also measures basic morphological properties of detected cells.

## Features
- Supports PNG, JPG, JPEG, TIFF and BMP images.
- Converts images to grayscale.
- Applies Gaussian blur and Otsu thresholding.
- Uses watershed segmentation to separate cells.
- Counts detected cells automatically.
- Measures cell area, perimeter and circularity.
- Generates CSV and PNG analysis reports.

## Technologies Used
- Python 3.12
- OpenCV
- NumPy
- Pandas
- Matplotlib
- Scikit-image (listed dependency)

## Project Structure
```text
Automated-Cell-counting-Analyzer/
│
├── main.py
├── requirements.txt
├── README.md
├── sample_cells.png.jpeg
└── results/
    ├── cell_measurements.csv
    ├── detected_cells.png
    └── cell_area_distribution.png
```

## Installation

Install the required dependencies:

```bash
py -m pip install -r requirements.txt
```

## Usage

Run the analyzer with a sample image:

```bash
py main.py --image "sample_cells.png.jpeg"
```

To specify a minimum cell area:

```bash
py main.py --image "sample_cells.png.jpeg" --min-area 50
```

## Output
The program generates:
- `cell_measurements.csv` – cell measurement data.
- `detected_cells.png` – image with detected cell outlines and labels.
- `cell_area_distribution.png` – cell area distribution histogram.

## Measurements
- Cell count
- Area (pixels)
- Perimeter (pixels)
- Circularity
- Equivalent diameter
- Centroid coordinates

## Note
This project is developed for educational and research purposes. Results depend on image quality and segmentation settings. It is not intended for medical diagnosis.
