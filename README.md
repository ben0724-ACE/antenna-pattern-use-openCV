# Antenna Pattern Analysis using OpenCV

This project provides tools for analyzing and visualizing antenna radiation patterns using computer vision techniques. It includes both Python (OpenCV) and MATLAB implementations for processing antenna measurement data and generating polar plots.

## Features

- Image processing of antenna measurement data using OpenCV
- Generation of polar radiation pattern plots
- Support for both vertical and horizontal polarization measurements
- Data export to CSV format
- Visualization using both Python (Matplotlib) and MATLAB

## Requirements

### Python Dependencies
- OpenCV (cv2)
- NumPy
- Matplotlib
- Pandas

### MATLAB Dependencies
- MATLAB R2019b or later
- Signal Processing Toolbox

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ben0724-ACE/antenna-pattern-use-openCV.git
cd antenna-pattern-use-openCV
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Python Implementation
```bash
python src/antennaPattern.py
```

### MATLAB Implementation
1. Open MATLAB
2. Navigate to the project directory
3. Run:
```matlab
plotAntennaPattern
```

## Project Structure
```
antenna-pattern-use-openCV/
├── src/
│   ├── antennaPattern.py
│   └── plotAntennaPattern.m
├── data/
│   ├── cylindrical_monopole_V.jpg
│   ├── cylindrical_monopole_H.jpg
│   └── antenna_data.csv
├── results/
│   ├── antenna_pattern_matlab.png
│   └── antenna_pattern2.png
├── requirements.txt
└── README.md
```

## Results

The program generates two types of visualization:
1. Python-generated polar plot (antenna_pattern2.png)
2. MATLAB-generated polar plot (antenna_pattern_matlab.png)

Both plots show the radiation pattern in dBm across 360 degrees for both vertical and horizontal polarizations.

## License

MIT License

## Author

- GitHub: [@ben0724-ACE](https://github.com/ben0724-ACE) 