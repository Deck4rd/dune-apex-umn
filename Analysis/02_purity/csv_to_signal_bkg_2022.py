import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from inc.basic_functions import plot_coincidence_histos
from inc.settings import NCC

plot_dir = './Plots'
raw_data_folder_name = '20220511'
csv_file_name = '20220511_CR_5_18_10_BH_32_36_20'

colors = plt.cm.rainbow(np.linspace(0, 1, NCC))

n_entries = 0

result_file_title = f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}.csv"

# Load the CSV data
df_r = pd.read_csv(result_file_title)

n_entries = df_r['evt_nr'].max()

# Initialize empty DataFrames
signal_df = pd.DataFrame()
backgr_df = pd.DataFrame()

for c_strip_index, color in zip(range(NCC), colors):

    # Find coincidences csv file
    if c_strip_index < 10:
        filename_strip_index = '0' + str(c_strip_index)
    else:
        filename_strip_index = str(c_strip_index)

    file_title = f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_Coincidences_strip_{filename_strip_index}.csv"

    # Load the CSV data
    df = pd.read_csv(file_title)

    if c_strip_index == 23 or c_strip_index == 24:
        signal_df = pd.concat([signal_df, df['charge_C']], ignore_index=True)
    elif 13 < c_strip_index < 34:
        backgr_df = pd.concat([backgr_df, df['charge_C']], ignore_index=True)

# Define common plot parameters
bin_size = 20  # You can adjust the bin size as needed
x_range = (0, 1000)  # Set the common x-axis range

# Plot and save signal histogram for the source as PDF
plt.figure(dpi=100)
signal_counts, signal_bins, _ = plt.hist(signal_df, bins=range(x_range[0], x_range[1] + bin_size, bin_size),
                                         color='darkorange', alpha=0.7,
                                         edgecolor='darkorange', linewidth=1.2, rwidth=0.85, density=False, label='Signal')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - Signal', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Reduce font size of axis tick labels
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.savefig(f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_SIGNAL_histogram.pdf")

# Plot and save background histogram for the source as PDF
plt.figure(dpi=100)
background_counts, background_bins, _ = plt.hist(backgr_df, bins=range(x_range[0], x_range[1] + bin_size, bin_size),
                                                 color='dodgerblue', alpha=0.7,
                                                 edgecolor='dodgerblue', linewidth=1.2, rwidth=0.85, density=False, label='Background')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - Background', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Reduce font size of axis tick labels
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.savefig(f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_BACKGROUND_histogram.pdf")

# Find peak bins
# signal_peak_bin = signal_bins[np.argmax(signal_counts)]
# background_peak_bin = background_bins[np.argmax(background_counts)]

print("signal_counts = ", signal_counts)
print("backgr counts = ", background_counts)
SB_ratio = np.divide(signal_counts, background_counts,
                     out=np.zeros_like(signal_counts), where=background_counts != 0)

print("SB_ratio = ", SB_ratio)

av_SB_ratio = SB_ratio[np.nonzero(SB_ratio)].mean()
std_SB_ratio = SB_ratio[np.nonzero(SB_ratio)].std()

scaling_factor = 1./av_SB_ratio

print("scaling_factor = ", scaling_factor)

# Create and plot the scaled background histogram for the source
scaled_bkg_counts = np.multiply(background_counts, scaling_factor)
print("scaled_bkg_counts = ", scaled_bkg_counts)

# Calculate the SIGNAL_BKG_SUB histogram for the source
signal_bkg_sub_hist = np.subtract(signal_counts, background_counts,
                                  out=np.zeros_like(signal_counts), where=background_counts != 0)
print("signal_bkg_sub_hist = ", signal_bkg_sub_hist)


# Plot and save scaled background histogram for the source as PDF
plt.figure(dpi=100)
plt.bar(background_bins[:-1], scaled_bkg_counts, width=bin_size, color='navy', alpha=0.7,
        edgecolor='navy', linewidth=1.2, label='SCALED_BKG')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - SCALED_BKG', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Plot and save the SIGNAL_BKG_SUB histogram for the source as PDF
plt.figure(dpi=100)
plt.bar(signal_bins[:-1], signal_bkg_sub_hist, width=bin_size, color='limegreen', alpha=0.7,
        edgecolor='limegreen', linewidth=1.2, label='SIGNAL_BKG_SUB')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - SIGNAL_BKG_SUB', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Create a histogram comparison plot with filled contours for the source
plt.figure(dpi=100)
plt.hist(signal_df, bins=range(x_range[0], x_range[1] + bin_size, bin_size), color='darkorange', alpha=0.7,
         edgecolor='darkorange', linewidth=1.2, rwidth=0.85, density=False, label='Signal', histtype='step', fill=False)
plt.hist(backgr_df, bins=range(x_range[0], x_range[1] + bin_size, bin_size), color='dodgerblue', alpha=0.7,
         edgecolor='dodgerblue', linewidth=1.2, rwidth=0.85, density=False, label='Background', histtype='step', fill=False)
plt.step(background_bins[:-1], background_counts,
         where='mid', color='navy', alpha=0.7, label='Scaled Background')
plt.legend(fontsize=10)

plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - Histogram Comparison', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=8)

# Reduce font size of axis tick labels
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.savefig(f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_HIST_COMPARISON.pdf")

# Show plots (optional)
plt.show()
