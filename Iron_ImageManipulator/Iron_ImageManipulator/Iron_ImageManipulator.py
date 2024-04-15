import pandas as pd
import pydicom 
import numpy as np
import os
import csv

#Calibration Parameters:
#x represents "high energy" and y "low energy" values
#Liver Water Line:
liver_x = 
liver_y = 





filepath_ME = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_03_28_ZM202_FE_sol/Fe-DTPA20cm_10m.CT.FeInsertTests(A.2.15.2024.03.28.15.09.16.931.72748928.dcm"
filepath_HIGH = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/CntHighEnergyVolume/SPP_CntHighEnergyVolume/Fe-DTPA20cm_10m.CT.FeInsertTests(A.2.15.2024.03.28.15.09.16.931.72748928.dcm"
filepath_LOW = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/CntLowEnergyVolume/SPP_CntLowEnergyVolume/Fe-DTPA20cm_10m.CT.FeInsertTests(A.2.15.2024.03.28.15.09.16.931.72748928.dcm"

dicom_ME = pydicom.dcmread(filepath_ME)
dicom_HIGH = pydicom.dcmread(filepath_HIGH)
dicom_LOW = pydicom.dcmread(filepath_LOW)

px_array_HIGH = dicom_HIGH.pixel_array * dicom_HIGH.RescaleSlope + dicom_HIGH.RescaleIntercept
px_array_LOW = dicom_LOW.pixel_array * dicom_LOW.RescaleSlope + dicom_LOW.RescaleIntercept


print (dicom_hu)