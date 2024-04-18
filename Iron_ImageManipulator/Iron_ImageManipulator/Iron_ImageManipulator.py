import pandas as pd
import pydicom 
import numpy as np
import os
import cv2
import csv
import matplotlib.pyplot as plt
from PIL import Image
from pydicom.dataset import Dataset


#Calibration Parameters:
#x represents "high energy" and y "low energy" values
#For 140 kVp photon counting mode with small phantom diameter for iron liver samples

#Liver Water Line:
liver_x = 1
liver_y = 1.195

#Liver Iron line
liver_iron_x = 1
liver_iron_y = 2.178



#filepath_ME = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_03_28_ZM202_FE_sol/Fe-DTPA20cm_10m.CT.FeInsertTests(A.2.15.2024.03.28.15.09.16.931.72748928.dcm"
filepath_HIGH = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_04_08_LiverSample_LOW_HIGH/SPP_CntHighEnergyVolume/IronLiver_1_25m.CT.CaInsertTests(A.5.55.2024.04.08.14.15.52.409.39375416.dcm"
filepath_LOW = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_04_08_LiverSample_LOW_HIGH/SPP_CntLowEnergyVolume/IronLiver_1_25m.CT.CaInsertTests(A.5.55.2024.04.08.14.15.52.409.39375416.dcm"

#Extracts Array in greyscale values
#dicom_ME = pydicom.dcmread(filepath_ME)
dicom_HIGH = pydicom.dcmread(filepath_HIGH)
dicom_LOW = pydicom.dcmread(filepath_LOW)


no_iron_array_ME = dicom_HIGH
only_iron_array_high = dicom_HIGH


#Get DICOM information
patientName = str(dicom_HIGH.PatientName)
list_firstandlastname = patientName.split("^")
energy = str(dicom_HIGH.ImageComments)
mode = str(dicom_HIGH.SeriesDescription)



#create Array with HU values
firstarray = dicom_HIGH.pixel_array 
px_array_HIGH = dicom_HIGH.pixel_array * dicom_HIGH.RescaleSlope + dicom_HIGH.RescaleIntercept
px_array_LOW = dicom_LOW.pixel_array * dicom_LOW.RescaleSlope + dicom_LOW.RescaleIntercept
px_array_ME = px_array_HIGH * 0.5 + px_array_LOW * 0.5


#creates slope and intercept for LOW and HIGH files
intercept_HIGH = dicom_HIGH.RescaleIntercept
slope_HIGH  = dicom_HIGH.RescaleSlope
intercept_LOW = dicom_LOW.RescaleIntercept
slope_LOW = dicom_LOW.RescaleSlope

#Calculates Values of High Energy image without iron HU
no_iron_array_high = 2.178 * px_array_HIGH - (1.02 * px_array_LOW)
no_iron_array_low = no_iron_array_high * liver_y

#Calculates Values of high energy image only containing the iron content HU
only_iron_array_high = -(1.22 * px_array_HIGH - 1.02 * px_array_LOW)
only_iron_array_low = only_iron_array_high * liver_iron_y



#create ME image array with HU values


if mode == "Abdomen 120kVp 2.00 Qr40 Q3  HIGH":
    no_iron_array_ME = no_iron_array_high * 0.56 + no_iron_array_low * 0.44 
    only_iron_array_ME = only_iron_array_high * 0.56 + only_iron_array_low * 0.44 
    
elif mode == "Abdomen140kVp 2.00 Qr40 Q3  HIGH":
    no_iron_array_ME = no_iron_array_high * 0.46 + no_iron_array_low * 0.54
    only_iron_array_ME = only_iron_array_high * 0.46 + only_iron_array_low * 0.54
  
elif mode == "Spine 90/Sn150 2.00 Qr40 Q3  HIGH":
    no_iron_array_ME = no_iron_array_high * 0.63 + no_iron_array_low * 0.37
    only_iron_array_ME = only_iron_array_high * 0.63 + only_iron_array_low * 0.37
elif mode == "Spine 70/Sn150 2.00 Qr40 Q3  HIGH":
    no_iron_array_ME = no_iron_array_high * 0.46 + no_iron_array_low * 0.54
    only_iron_array_ME = only_iron_array_high * 0.46 + only_iron_array_low * 0.54



#create removed iron image
if True:

    # Convert to float
    img_2d = px_array_ME.astype(float)

    # Rescale the values
    min_value = -500
    max_value = 400
    img_2d_scaled = np.clip((img_2d - min_value) / (max_value - min_value) * 250, 0, 250)

    # Convert to uint8
    img_2d_scaled = np.uint8(img_2d_scaled)

    
    # Create a mask of zero values in the original image
    zero_mask = img_2d_scaled == 0

    # Convert the mask to uint8 with value 0 where zeros are present
    zero_mask = zero_mask.astype(np.uint8) * 255


    # Apply blur filter
    blur = cv2.medianBlur(img_2d_scaled,5)
    for i in range(100):
        blur = cv2.medianBlur(blur,5)


    # Rescale the values
    min_value = 0
    max_value = 500
    blur = np.clip((blur - min_value) / (max_value - min_value) * 250, 0, 250)



    # Overlay the zero values of the original image onto the filtered image
    blur = np.uint8(blur)
    final_image = cv2.bitwise_or(blur, zero_mask)

    final_image[final_image == 255] = 0

    final_image =  cv2.blur(final_image, (3, 3))

    # Display images using matplotlib with color
    plt.subplot(131), plt.imshow(img_2d_scaled, cmap='viridis'), plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(blur, cmap='viridis'), plt.title('Averaging')
    plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(final_image, cmap='viridis'), plt.title('Final Image')
    plt.xticks([]), plt.yticks([])
    plt.colorbar()
    plt.show()
  
   

#var2[var2 < 0] = 0
#greyscale_px_array_ME = (var2 - dicom_HIGH.RescaleIntercept)/dicom_HIGH.RescaleSlope

#Create only iron image
if False:
    var2[var2 < 0] = 0
  # Calculate iron content differences
    px_array_iron_content_HIGH = px_array_HIGH - px_array_HIGH_no_iron
    px_array_iron_content_LOW = px_array_LOW - px_array_LOW_no_iron

    # Rescale the values
    min_value = 0
    max_value = 300
    # Scale the iron content differences for visualization
    scaled_high = np.clip((var2 - min_value) / (max_value - min_value) * 255, 0, 255)
    scaled_low = np.clip((var2 - min_value) / (max_value - min_value) * 255, 0, 255)

    # Create empty RGB image
    height, width = var2.shape
    rgb_image = np.zeros((height, width, 3), dtype=np.uint64)

    # Assign iron content differences to respective channels
 
    rgb_image[:,:,0] = var2
  

   



#create new DICOM File
if False:
    
    # Create a new DICOM dataset
    ds = Dataset()

    # Set required DICOM attributes
    ds.PatientName = "Anonymous"
    ds.PatientID = "123456"

    # Set pixel array
    
    if greyscale_px_array_ME.dtype != np.uint16:
        pixel_array = greyscale_px_array_ME.astype(np.uint16)
    else:
        pixel_array = greyscale_px_array_ME  

    ds.PixelData = pixel_array.tobytes()

    # Set other DICOM attributes as needed
    ds.Rows = pixel_array.shape[0]
    ds.Columns = pixel_array.shape[1]
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.RescaleSlope = dicom_HIGH.RescaleSlope
    ds.RescaleIntercept = dicom_HIGH.RescaleIntercept
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 0  # Unsigned integer

    # Set study, series, and instance UIDs
    ds.StudyInstanceUID = "1.2.3.4.5"
    ds.SeriesInstanceUID = "1.2.3.4.5.1"
    ds.SOPInstanceUID = "1.2.3.4.5.1.1"

    # Set transfer syntax and VR
    ds.is_little_endian = True
    ds.is_implicit_VR = False 

    # Save the dataset to a DICOM file
    ds.save_as("E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_04_16_Created_DICOMs/new_dicom_file.dcm")

#greyscale_HIGH = (px_array_iron_content_HIGH - dicom_HIGH.RescaleIntercept)/dicom_HIGH.RescaleSlope


#print(px_array_iron_content_HIGH)
