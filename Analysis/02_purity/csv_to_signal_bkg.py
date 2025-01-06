import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from inc.basic_functions import plot_coincidence_histos
from inc.settings import NCC

plot_dir = './Plots'
raw_data_folder_name = '20230722'
csv_file_name = '20230722_CR_5_18_20_BH_32_36_20'

colors = plt.cm.rainbow(np.linspace(0, 1, NCC))

n_entries = 0

result_file_title = f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}.csv"

# Load the CSV data
df_r = pd.read_csv(result_file_title)

n_entries = df_r['evt_nr'].max()

# Initialize empty DataFrames
signal_df_One = pd.DataFrame()
backgr_df_One = pd.DataFrame()

signal_df_Two = pd.DataFrame()
backgr_df_Two = pd.DataFrame()

for c_strip_index, color in zip(range(NCC), colors):
    for source in 'One', 'Two':

        # Find coincidences csv file
        if c_strip_index < 10:
            filename_strip_index = '0' + str(c_strip_index)
        else:
            filename_strip_index = str(c_strip_index)

        file_title = f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_Coincidences_{source}_strip_{filename_strip_index}.csv"

        # Load the CSV data
        df = pd.read_csv(file_title)

        if c_strip_index == 15:
            # if c_strip_index == 15 or c_strip_index == 16:
            if source == 'One':
                signal_df_One = pd.concat([signal_df_One, df['charge_C']], ignore_index=True)
            if source == 'Two':
                signal_df_Two = pd.concat([signal_df_Two, df['charge_C']], ignore_index=True)
        elif 9 < c_strip_index < 22:
            if source == 'One':
                backgr_df_One = pd.concat([backgr_df_One, df['charge_C']], ignore_index=True)
            if source == 'Two':
                backgr_df_Two = pd.concat([backgr_df_Two, df['charge_C']], ignore_index=True)

# Define common plot parameters
bin_size = 20  # You can adjust the bin size as needed
x_range = (0, 1000)  # Set the common x-axis range

# Plot and save signal histogram for the "One" source as PDF
plt.figure(dpi=100)
signal_counts_One, signal_bins_One, _ = plt.hist(signal_df_One, bins=range(x_range[0], x_range[1] + bin_size, bin_size),
                                                 color='darkorange', alpha=0.7,
                                                 edgecolor='darkorange', linewidth=1.2, rwidth=0.85, density=False, label='Signal (One)')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - Signal (One)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Reduce font size of axis tick labels
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.savefig(f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_SIGNAL_histogram_One.pdf")

# Plot and save background histogram for the "One" source as PDF
plt.figure(dpi=100)
background_counts_One, background_bins_One, _ = plt.hist(backgr_df_One, bins=range(x_range[0], x_range[1] + bin_size, bin_size),
                                                         color='dodgerblue', alpha=0.7,
                                                         edgecolor='dodgerblue', linewidth=1.2, rwidth=0.85, density=False, label='Background (One)')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - Background (One)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Reduce font size of axis tick labels
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.savefig(f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_BACKGROUND_histogram_One.pdf")

# Plot and save signal histogram for the "Two" source as PDF
plt.figure(dpi=100)
signal_counts_Two, signal_bins_Two, _ = plt.hist(signal_df_Two, bins=range(x_range[0], x_range[1] + bin_size, bin_size),
                                                 color='darkorange', alpha=0.7,
                                                 edgecolor='darkorange', linewidth=1.2, rwidth=0.85, density=False, label='Signal (Two)')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - Signal (Two)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Reduce font size of axis tick labels
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.savefig(f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_SIGNAL_histogram_Two.pdf")

# Plot and save background histogram for the "Two" source as PDF
plt.figure(dpi=100)
background_counts_Two, background_bins_Two, _ = plt.hist(backgr_df_Two, bins=range(x_range[0], x_range[1] + bin_size, bin_size),
                                                         color='dodgerblue', alpha=0.7,
                                                         edgecolor='dodgerblue', linewidth=1.2, rwidth=0.85, density=False, label='Background (Two)')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - Background (Two)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Reduce font size of axis tick labels
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.savefig(f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_BACKGROUND_histogram_Two.pdf")

# Find peak bins
# signal_peak_bin = signal_bins[np.argmax(signal_counts)]
# background_peak_bin = background_bins[np.argmax(background_counts)]

print("signal_counts_One = ", signal_counts_One)
print("backgr counts_One = ", background_counts_One)
print("signal_counts_Two = ", signal_counts_Two)
print("backgr counts_Two = ", background_counts_Two)

SB_ratio_One = np.divide(signal_counts_One, background_counts_One,
                         out=np.zeros_like(signal_counts_One), where=background_counts_One != 0)

SB_ratio_Two = np.divide(signal_counts_Two, background_counts_Two,
                         out=np.zeros_like(signal_counts_Two), where=background_counts_Two != 0)

print("SB_ratio_One = ", SB_ratio_One)
print("SB_ratio_Two = ", SB_ratio_Two)

av_SB_ratio_One = SB_ratio_One[np.nonzero(SB_ratio_One)].mean()
std_SB_ratio_One = SB_ratio_One[np.nonzero(SB_ratio_One)].std()

av_SB_ratio_Two = SB_ratio_Two[np.nonzero(SB_ratio_Two)].mean()
std_SB_ratio_Two = SB_ratio_Two[np.nonzero(SB_ratio_Two)].std()

scaling_factor_One = 1./av_SB_ratio_One
scaling_factor_Two = 1./av_SB_ratio_Two

print("scaling_factor_One = ", scaling_factor_One)
print("scaling_factor_Two = ", scaling_factor_Two)

# Create and plot the scaled background histogram for the "One" source
# scaled_bkg_counts_One = [a*b for a, b in zip(background_counts_One, SB_ratio_One[np.nonzero(SB_ratio_One)])]
scaled_bkg_counts_One = [x * scaling_factor_One for x in background_counts_One]
print("scaled_bkg_counts_One = ", scaled_bkg_counts_One)

# Create and plot the scaled background histogram for the "Two" source
# scaled_bkg_counts_Two = [a*b for a, b in zip(background_counts_Two, SB_ratio_Two[np.nonzero(SB_ratio_Two)])]
scaled_bkg_counts_Two = [x * scaling_factor_Two for x in background_counts_Two]
print("scaled_bkg_counts_Two = ", scaled_bkg_counts_Two)

# Calculate the SIGNAL_BKG_SUB histogram for the "One" source
signal_bkg_sub_hist_One = np.subtract(signal_counts_One, background_counts_One,
                                      out=np.zeros_like(signal_counts_One), where=background_counts_One != 0)
print("signal_bkg_sub_hist_One = ", signal_bkg_sub_hist_One)

# Calculate the SIGNAL_BKG_SUB histogram for the "Two" source
signal_bkg_sub_hist_Two = np.subtract(signal_counts_Two, background_counts_Two,
                                      out=np.zeros_like(signal_counts_Two), where=background_counts_Two != 0)
print("signal_bkg_sub_hist_Two = ", signal_bkg_sub_hist_Two)

# Plot and save scaled background histogram for the "One" source as PDF
plt.figure(dpi=100)
plt.bar(background_bins_One[:-1], scaled_bkg_counts_One, width=bin_size, color='navy', alpha=0.7,
        edgecolor='navy', linewidth=1.2, label='SCALED_BKG_One')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - SCALED_BKG (One)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Plot and save scaled background histogram for the "Two" source as PDF
plt.figure(dpi=100)
plt.bar(background_bins_Two[:-1], scaled_bkg_counts_Two, width=bin_size, color='navy', alpha=0.7,
        edgecolor='navy', linewidth=1.2, label='SCALED_BKG (Two)')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - SCALED_BKG (Two)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Plot and save the SIGNAL_BKG_SUB histogram for the "One" source as PDF
plt.figure(dpi=100)
plt.bar(signal_bins_One[:-1], signal_bkg_sub_hist_One, width=bin_size, color='limegreen', alpha=0.7,
        edgecolor='limegreen', linewidth=1.2, label='SIGNAL_BKG_SUB (One)')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - SIGNAL_BKG_SUB (One)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Plot and save the SIGNAL_BKG_SUB histogram for the "Two" source as PDF
plt.figure(dpi=100)
plt.bar(signal_bins_Two[:-1], signal_bkg_sub_hist_Two, width=bin_size, color='forestgreen', alpha=0.7,
        edgecolor='forestgreen', linewidth=1.2, label='SIGNAL_BKG_SUB (Two)')
plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - SIGNAL_BKG_SUB (Two)', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# Create a histogram comparison plot with filled contours for the "One" source
plt.figure(dpi=100)
plt.hist(signal_df_One, bins=range(x_range[0], x_range[1] + bin_size, bin_size), color='darkorange', alpha=0.7,
         edgecolor='darkorange', linewidth=1.2, rwidth=0.85, density=False, label='Signal (One)', histtype='step', fill=False)
plt.hist(backgr_df_One, bins=range(x_range[0], x_range[1] + bin_size, bin_size), color='dodgerblue', alpha=0.7,
         edgecolor='dodgerblue', linewidth=1.2, rwidth=0.85, density=False, label='Background (One)', histtype='step', fill=False)
plt.step(background_bins_One[:-1], background_counts_One,
         where='mid', color='navy', alpha=0.7, label='Scaled Background')
plt.legend(fontsize=10)

plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - Histogram Comparison - One', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=8)

# Reduce font size of axis tick labels
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.savefig(f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_HIST_COMPARISON_One.pdf")

# Show plots (optional)
plt.show()

# Create a histogram comparison plot with filled contours for the "Two" source
plt.figure(dpi=100)
plt.hist(signal_df_Two, bins=range(x_range[0], x_range[1] + bin_size, bin_size), color='darkorange', alpha=0.7,
         edgecolor='darkorange', linewidth=1.2, rwidth=0.85, density=False, label='Signal (Two)', histtype='step', fill=False)
plt.hist(backgr_df_Two, bins=range(x_range[0], x_range[1] + bin_size, bin_size), color='darkblue', alpha=0.7,
         edgecolor='dodgerblue', linewidth=1.2, rwidth=0.85, density=False, label='Background (Two)', histtype='step', fill=False)
plt.step(background_bins_Two[:-1], scaled_bkg_counts_Two, where='mid',
         color='navy', alpha=0.7, label='Scaled Background')
plt.legend(fontsize=10)

plt.xlim(x_range)
plt.xlabel('[ADC*µs]', fontsize=12)
plt.ylabel('[#]', fontsize=12)
plt.title(f'{csv_file_name} - Histogram Comparison - Source Two', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(fontsize=8)

# Reduce font size of axis tick labels
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.savefig(f"{plot_dir}/{raw_data_folder_name}/{csv_file_name}_HIST_COMPARISON_Two.pdf")

# Show plots (optional)
plt.show()
