# Research Skills in the Open Science Era – CIVIL\_608 | Assignment 02

This repository contains a Python script to extract and visualize **positive and negative force–drift cycles** from cyclic shear-compression test data of stone masonry walls. The output highlights hysteresis behavior and structural envelope response, essential for evaluating seismic performance.

## Sample Use Case: Figure Reproduction

This script generates **Figure 04** from the associated analysis:

> **Figure 04. Force–Drift relationship highlighting extracted positive and negative cycles from experimental data.**
> The blue curve represents the complete hysteresis loop. Black and red lines represent extracted envelope curves for positive and negative cycles, respectively.

## Reproducibility Checklist

###  1. Clone the Repository

```bash
git clone https://github.com/mati-shah/A2_Civil_608.git
cd A2_Civil_608
```

### 2. Set Up a Virtual Environment (Recommended: Conda)

```bash
conda create -n myfig python=3.10
conda activate myfig
```

### 3. Install Required Packages

```bash
pip install pandas numpy matplotlib scipy
```

## Directory Structure

```
A2_Civil_608/
|
├── Code/                    # Python script(s) for analysis
│   └── Compute_envelope.py  # Main analysis script
|
├── input_data/              # Input CSV files (e.g., Sample_test.csv)
├── output_data/             # Output figures and extracted data
├── README.md                # Project documentation
└── LICENSE                  # License file
```


## Running the Script

1. Place your experimental data (e.g., `Sample_test.csv`) inside the `input_data/` folder.
2. Navigate to the `Code/` folder and run:

```bash
python Compute_envelope.py
```

3. Output:

   * A figure: `envelope_test.png` in `output_data/`
   * A CSV file: `envelope_test.csv` containing combined positive/negative cycles


## Functionality Overview

The script performs the following:

* Reads cyclic test data (`Displacement`, `Force`, `Drift`)
* Identifies local maxima/minima using peak detection (`scipy.signal.find_peaks`)
* Extracts individual positive and negative cycles
* Plots hysteresis loops with envelope curves
* Exports cleaned and ordered data to CSV


## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Contact
For any queries, please contact: mati.shah@epfl.ch
