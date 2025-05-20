
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import os

# Define paths
input_folder = "..\Input_data"
output_folder = "..\A2\Output_data"
input_file_name = "Sample_test.csv"
input_file_path = os.path.join(input_folder, input_file_name)

# Extract file ID for naming
file_id = input_file_name.split("_", 1)[-1].split(".")[0]

thre = 0.00

# Read the first 4 lines as metadata (optional)
with open(input_file_path, "r", encoding="ISO-8859-1") as f:
    header_lines = [next(f).strip() for _ in range(4)]

# Read CSV and define column names
df = pd.read_csv(input_file_path, skiprows=4, header=None, encoding="ISO-8859-1")
df.columns = ["Displacement", "Force", "Drift"]
df_clean = df.dropna().reset_index(drop=True)

# Detect local peaks
local_maxima, _ = find_peaks(df_clean["Drift"], prominence=0.05, distance=5)
filtered_maxima = []
prev_value = -np.inf
for peak in local_maxima:
    current_value = df_clean["Drift"].iloc[peak]
    if current_value > prev_value:
        filtered_maxima.append(peak)
        prev_value = current_value
local_maxima = np.array(filtered_maxima)

local_minima, _ = find_peaks(-df_clean["Drift"], prominence=0.1, distance=10)
filtered_minima = []
prev_value = np.inf
for peak in local_minima:
    current_value = df_clean["Drift"].iloc[peak]
    if current_value < prev_value:
        filtered_minima.append(peak)
        prev_value = current_value
local_minima = np.array(filtered_minima)

# Extract peak data
disp_max = df_clean["Displacement"].iloc[local_maxima].values
force_max = df_clean["Force"].iloc[local_maxima].values
drift_max = df_clean["Drift"].iloc[local_maxima].values
disp_min = df_clean["Displacement"].iloc[local_minima].values
force_min = df_clean["Force"].iloc[local_minima].values
drift_min = df_clean["Drift"].iloc[local_minima].values
index_max = df_clean.index[local_maxima]
index_min = df_clean.index[local_minima]

# Cycle extraction
pos_drift, pos_force, pos_disp = [0], [0], [0]
neg_drift, neg_force, neg_disp = [0], [0], [0]

# Positive cycles
if len(local_maxima) >= 2:
    first_pos_peak_index = local_maxima[0]
    first_pos_peak_drift = df_clean["Drift"].iloc[first_pos_peak_index]
    start_pos_index = df_clean.index[(df_clean.index < first_pos_peak_index) & 
                                     (df_clean["Drift"] <= 0)].max()
    if start_pos_index is not None:
        first_pos_cycle = df_clean.loc[start_pos_index:first_pos_peak_index]
        pos_drift.extend(first_pos_cycle["Drift"])
        pos_force.extend(first_pos_cycle["Force"])
        pos_disp.extend(first_pos_cycle["Displacement"])
    ref_pos_index = first_pos_peak_index
    ref_pos_drift = first_pos_peak_drift
    for i in range(1, len(local_maxima)):
        curr_peak_index = local_maxima[i]
        curr_peak_drift = df_clean["Drift"].iloc[curr_peak_index]
        if abs(curr_peak_drift - ref_pos_drift) >= thre:
            condition = df_clean["Drift"] > ref_pos_drift
            extracted_data = df_clean[condition].loc[ref_pos_index:curr_peak_index]
            pos_drift.extend(extracted_data["Drift"])
            pos_force.extend(extracted_data["Force"])
            pos_disp.extend(extracted_data["Displacement"])
            ref_pos_index = curr_peak_index
            ref_pos_drift = curr_peak_drift

# Negative cycles
if len(local_minima) >= 2:
    first_neg_peak_index = local_minima[0]
    first_neg_peak_drift = df_clean["Drift"].iloc[first_neg_peak_index]
    start_neg_index = df_clean.index[(df_clean.index < first_neg_peak_index) & 
                                     (df_clean["Drift"] >= 0)].max()
    if start_neg_index is not None:
        first_neg_cycle = df_clean.loc[start_neg_index:first_neg_peak_index]
        neg_drift.extend(first_neg_cycle["Drift"])
        neg_force.extend(first_neg_cycle["Force"])
        neg_disp.extend(first_neg_cycle["Displacement"])
    ref_neg_index = first_neg_peak_index
    ref_neg_drift = first_neg_peak_drift
    for i in range(1, len(local_minima)):
        curr_peak_index = local_minima[i]
        curr_peak_drift = df_clean["Drift"].iloc[curr_peak_index]
        if abs(curr_peak_drift - ref_neg_drift) >= thre:
            condition = df_clean["Drift"] < ref_neg_drift
            extracted_data = df_clean[condition].loc[ref_neg_index:curr_peak_index]
            neg_drift.extend(extracted_data["Drift"])
            neg_force.extend(extracted_data["Force"])
            neg_disp.extend(extracted_data["Displacement"])
            ref_neg_index = curr_peak_index
            ref_neg_drift = curr_peak_drift

# Remaining data
remaining_data = df_clean.iloc[max(index_max[-1] if len(index_max) > 0 else 0, 
                                   index_min[-1] if len(index_min) > 0 else 0) + 1:]
if not remaining_data.empty:
    max_remaining_drift = remaining_data["Drift"].max()
    min_remaining_drift = remaining_data["Drift"].min()
    if max_remaining_drift > max(pos_drift):  
        max_row = remaining_data.loc[remaining_data["Drift"].idxmax()]
        pos_drift.append(max_row["Drift"])
        pos_force.append(max_row["Force"])
        pos_disp.append(max_row["Displacement"])
    if min_remaining_drift < min(neg_drift):  
        min_row = remaining_data.loc[remaining_data["Drift"].idxmin()]
        neg_drift.append(min_row["Drift"])
        neg_force.append(min_row["Force"])
        neg_disp.append(min_row["Displacement"])

# Plot and save
plt.figure(figsize=(10, 6))
plt.plot(df_clean["Drift"], df_clean["Force"], color="blue", linestyle="-", label="Force vs Drift")
plt.plot(pos_drift, pos_force, color="black", linestyle="-", label="Extracted Positive Cycles")
plt.plot(neg_drift, neg_force, color="red", linestyle="-", label="Extracted Negative Cycles")
plt.xlabel("Drift [%]")
plt.ylabel("Force [kN]")
plt.title("Cyclic shear response")
plt.legend()
plt.grid(False)
plt.savefig(os.path.join(output_folder, f"envelope_{file_id}.png"), dpi=300, bbox_inches="tight")
plt.show()


# Save to CSV
output_csv_path = os.path.join(output_folder, f"envelope_{file_id}.csv")
neg_drift_reversed = neg_drift[::-1]  
neg_force_reversed = neg_force[::-1]  
neg_displacement_reversed = neg_disp[::-1]  
displacement_combined = np.concatenate((neg_displacement_reversed, pos_disp))
force_combined = np.concatenate((neg_force_reversed, pos_force))
drift_combined = np.concatenate((neg_drift_reversed, pos_drift))

with open(output_csv_path, "w", encoding="ISO-8859-1") as f:
    f.write("\n".join(header_lines[:4]) + "\n")  
    np.savetxt(f, np.column_stack((displacement_combined, force_combined, drift_combined)), 
               delimiter=",", fmt="%.6f", header="Displacement,Force,Drift", comments="")

print(f"Envelope data saved to {output_csv_path} in correct order.")
