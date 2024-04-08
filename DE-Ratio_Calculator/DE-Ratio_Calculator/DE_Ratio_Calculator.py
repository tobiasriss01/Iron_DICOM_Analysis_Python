import numpy as np
import csv
import pandas as pd 


# File path to your CSV file
filepath_low = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_CSV_Files/ROI_Values_Low.csv"
filepath_high = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_CSV_Files/ROI_Values_High.csv"

filepath_mean_low = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_CSV_Files/Calculated_Means_Low.csv"
filepath_mean_high = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_CSV_Files/Calculated_Means_High.csv"



# Load the data from the CSV file
# You may need to adjust additional parameters such as delimiter, encoding, etc., based on your CSV file.
pd_table_low = pd.read_csv(filepath_low, sep=';', engine='python')
mean_values_low = pd_table_low.groupby(['Solution', 'Concentration', 'Diameter', 'Mode'])['Mean of ROI'].mean()

mean_values_low.to_csv(filepath_mean_low, sep=';')

pd_table_high = pd.read_csv(filepath_high, sep=';', engine='python')
mean_values_high = pd_table_high.groupby(['Solution', 'Concentration', 'Diameter', 'Mode'])['Mean of ROI'].mean()

mean_values_high.to_csv(filepath_mean_high, sep=';')

# Load the data from the CSV file
# You may need to adjust additional parameters such as delimiter, encoding, etc., based on your CSV file.
l_table = pd.read_csv(filepath_mean_low, sep=';', engine='python')
h_table = pd.read_csv(filepath_mean_high, sep=';', engine='python')

# Merge the two tables on 'concentration' and 'solution' columns
#mean_values_low['High Energy iron value'] = mean_values_high['Mean of ROI'].copy()

l_table['Mode'] = l_table['Mode'].replace('Abdomen 120kVp 2.00 Qr40 Q3  LOW', 'Abdomen 120kVp 2.00 Qr40 Q3')
l_table['Mode'] = l_table['Mode'].replace('Abdomen140kVp 2.00 Qr40 Q3  LOW', 'Abdomen140kVp 2.00 Qr40 Q3')
l_table['Mode'] = l_table['Mode'].replace('Spine 70/Sn150 2.00 Qr40 Q3  LOW', 'Spine 70/Sn150 2.00 Qr40 Q3')
l_table['Mode'] = l_table['Mode'].replace('Spine 90/Sn150 2.00 Qr40 Q3  LOW', 'Spine 90/Sn150 2.00 Qr40 Q3')
h_table['Mode'] = h_table['Mode'].replace('Abdomen 120kVp 2.00 Qr40 Q3  HIGH', 'Abdomen 120kVp 2.00 Qr40 Q3')
h_table['Mode'] = h_table['Mode'].replace('Abdomen140kVp 2.00 Qr40 Q3  HIGH', 'Abdomen140kVp 2.00 Qr40 Q3')
h_table['Mode'] = h_table['Mode'].replace('Spine 70/Sn150 2.00 Qr40 Q3  HIGH', 'Spine 70/Sn150 2.00 Qr40 Q3')
h_table['Mode'] = h_table['Mode'].replace('Spine 90/Sn150 2.00 Qr40 Q3  HIGH', 'Spine 90/Sn150 2.00 Qr40 Q3')


merged_table = pd.merge(l_table, h_table[['Solution', 'Concentration', 'Diameter', 'Mode', 'Mean of ROI']], on=['Solution', 'Concentration', 'Diameter', 'Mode'], how='outer')
merged_table.rename(columns={'Mean of ROI_x': 'Low Energy Values'}, inplace=True)
merged_table.rename(columns={'Mean of ROI_y': 'High Energy Values'}, inplace=True)
#merged_table.drop(columns=['Energy'], inplace=True)

#sorted_table = merged_table.sort_values(by=['Solution', 'Diameter','Mode'])


merged_table.to_csv("E:/UserData/z004x2zj/Documents/Iron_Code/Iron_CSV_Files/Merged_Table.csv", sep=';', index=False)

