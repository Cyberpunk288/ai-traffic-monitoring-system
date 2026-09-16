# Dataset Inventory

## Project

AI-Based Nepali Vehicle Number Plate Detection and Recognition System

## Purpose

This document records and evaluates datasets considered for the
Nepali vehicle number plate detection and recognition system.

---

## Dataset 1 — Vehicle Number Plate Dataset (Nepal)

### Source

Kaggle

### URL

https://www.kaggle.com/datasets/ishworsubedii/vehicle-number-plate-datasetnepal

### Reported Location

Kathmandu, Bhaktapur, and Lalitpur, Nepal

### Dataset Type

To be verified.

### Number of Images

To be verified.

### Full Vehicle Images

To be verified.

### Number Plate Bounding Boxes

To be verified.

### OCR/Text Labels

To be verified.

### Annotation Format

To be verified.

### License

Apache License 2.0 (reported)

### Intended Use

Potential YOLO number plate detection dataset.

### Initial Decision

Pending dataset inspection.

### Notes

The dataset is specifically related to Nepali vehicle number
plates and will be inspected before inclusion in the final
training dataset.

---

## Dataset Evaluation

| Criteria | Result |
|---|---|
| Nepali vehicle plates | Pending |
| Full vehicle images | Pending |
| Bounding boxes | Pending |
| OCR labels | Pending |
| Image quality | Pending |
| Duplicate images | Pending |
| License suitable for academic use | Pending |
| Suitable for YOLO training | Pending |
| Suitable for OCR | Pending |
| Final decision | Pending |


## Dataset Preparation and Verification

The selected dataset was prepared for YOLO-based vehicle number plate detection.

### Dataset Split

| Split | Images | Labels | Percentage |
|---|---:|---:|---:|
| Train | 5,654 | 5,654 | 70% |
| Validation | 1,615 | 1,615 | 20% |
| Test | 809 | 809 | 10% |
| **Total** | **8,078** | **8,078** | **100%** |

The dataset contains one detection class:

- Class 0: `license_plate`

### Dataset Structure

```text
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
└── labels/
    ├── train/
    ├── val/
    └── test/