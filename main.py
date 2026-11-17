import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os


def analyze_cells(image_path, output_dir="results", min_area=50):

    os.makedirs(output_dir, exist_ok=True)

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to load image. Check image path.")

    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Image preprocessing
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Automatic thresholding
    threshold_value, _ = cv2.threshold(
        blurred, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    border = np.concatenate([
        gray[0, :], gray[-1, :],
        gray[:, 0], gray[:, -1]
    ])

    polarity = (
        cv2.THRESH_BINARY_INV
        if np.median(border) > threshold_value
        else cv2.THRESH_BINARY
    )

    _, binary = cv2.threshold(
        blurred, 0, 255, polarity + cv2.THRESH_OTSU
    )

    # Noise removal
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (3, 3)
    )

    binary = cv2.morphologyEx(
        binary, cv2.MORPH_OPEN, kernel
    )

    # Separate touching cells
    distance = cv2.distanceTransform(
        binary, cv2.DIST_L2, 5
    )

    if distance.max() == 0:
        raise ValueError("No objects detected in image.")

    _, foreground = cv2.threshold(
        distance, 0.35 * distance.max(),
        255, cv2.THRESH_BINARY
    )

    foreground = np.uint8(foreground)
    background = cv2.dilate(binary, kernel, iterations=3)
    unknown = cv2.subtract(background, foreground)

    _, markers = cv2.connectedComponents(foreground)

    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(image.copy(), markers)

    output = original.copy()
    measurements = []
    cell_id = 1

    # Cell measurement
    for label in np.unique(markers):

        if label <= 1:
            continue

        mask = np.uint8(markers == label) * 255
        area = cv2.countNonZero(mask)

        if area < min_area:
            continue

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            continue

        contour = max(contours, key=cv2.contourArea)

        perimeter = cv2.arcLength(contour, True)

        if perimeter <= 0:
            continue

        circularity = (
            4 * np.pi * area / (perimeter ** 2)
        )

        circularity = min(circularity, 1.0)

        diameter = np.sqrt(4 * area / np.pi)

        moments = cv2.moments(contour)

        if moments["m00"] == 0:
            continue

        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

        measurements.append({
            "Cell_ID": cell_id,
            "Area_pixels": area,
            "Perimeter_pixels": round(perimeter, 2),
            "Circularity": round(circularity, 4),
            "Equivalent_Diameter_pixels": round(diameter, 2),
            "Centroid_X": cx,
            "Centroid_Y": cy
        })

        cv2.drawContours(
            output, [contour], -1, (0, 255, 0), 2
        )

        cv2.putText(
            output, str(cell_id), (cx, cy),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 1
        )

        cell_id += 1

    # Save results
    df = pd.DataFrame(measurements)

    csv_path = os.path.join(
        output_dir, "cell_measurements.csv"
    )

    image_output = os.path.join(
        output_dir, "detected_cells.png"
    )

    df.to_csv(csv_path, index=False)
    cv2.imwrite(image_output, output)

    # Create area distribution graph
    if not df.empty:

        plt.figure(figsize=(8, 5))

        plt.hist(
            df["Area_pixels"],
            bins=15,
            edgecolor="black"
        )

        plt.title("Cell Area Distribution")
        plt.xlabel("Cell Area (pixels)")
        plt.ylabel("Number of Cells")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                output_dir, "cell_area_distribution.png"
            )
        )

        plt.close()

        average_area = df["Area_pixels"].mean()
        average_circularity = df["Circularity"].mean()

    else:
        average_area = 0
        average_circularity = 0

    print("\n===== CELL ANALYSIS REPORT =====")
    print("Total Cells:", len(df))
    print("Average Area:", round(average_area, 2))
    print("Average Circularity:", round(average_circularity, 4))
    print("CSV:", csv_path)
    print("Annotated Image:", image_output)
    print("================================")

    return df


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Automated Cell Counting and Morphology Analyzer"
    )

    parser.add_argument(
        "--image", required=True,
        help="Path to microscopy image"
    )

    parser.add_argument(
        "--output", default="results"
    )

    parser.add_argument(
        "--min-area", type=int, default=50
    )

    args = parser.parse_args()

    analyze_cells(
        args.image,
        args.output,
        args.min_area
    )
