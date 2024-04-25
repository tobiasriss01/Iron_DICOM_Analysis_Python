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
liver_y = 1.155

#Liver Iron line
liver_iron_x = 1
liver_iron_y = 2.02



#filepath_ME = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_03_28_ZM202_FE_sol/Fe-DTPA20cm_10m.CT.FeInsertTests(A.2.15.2024.03.28.15.09.16.931.72748928.dcm"
filepath_HIGH = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_04_23_ZM202_IronLiver_etc/IronLiver_multiple_LH/SPP_CntHighEnergyVolume/IronLiver_all_1.CT.FeInsertTests(A.2.1.2024.04.23.09.51.28.404.65539006.dcm"
filepath_LOW = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_04_23_ZM202_IronLiver_etc/IronLiver_multiple_LH/SPP_CntLowEnergyVolume/IronLiver_all_1.CT.FeInsertTests(A.2.1.2024.04.23.09.51.28.404.65539006.dcm"

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
if False:

    # Convert to float
    img_2d = no_iron_array_ME.astype(float)




    # Rescale the values
    min_value = -40
    max_value = 200
    img_2d_scaled = np.clip((img_2d - min_value) / (max_value - min_value) * 250, 0, 250)
    px_array_ME_scaled = np.clip((px_array_ME - min_value) / (max_value - min_value) * 250, 0, 250)

    #Create a mask of zero values in the original image
    zero_mask = px_array_ME_scaled == 0
    # Convert the mask to uint8 with value 0 where zeros are present
    zero_mask = zero_mask.astype(np.uint8) * 255


    #replace air of img_2d_scaled with water for further processing
    img_2d_scaled[img_2d_scaled == 0] = 40

    
    # Convert to uint8
    blur = np.uint8(img_2d_scaled)


    # Apply blur filter
    blur = cv2.medianBlur(blur,5)
    for i in range(2):
      blur = cv2.medianBlur(blur,5)

    # Overlay the zero values of the original image onto the filtered image
    final_image = cv2.bitwise_or(blur, zero_mask)

    final_image[final_image == 255] = 0

    


    # Display images using matplotlib with color
    plt.subplot(131), plt.imshow(px_array_ME_scaled, cmap='viridis'), plt.title('Original ME')
    plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(blur, cmap='viridis'), plt.title('Iron removed')
    plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(final_image, cmap='viridis'), plt.title('Final Image')
    plt.xticks([]), plt.yticks([])
    plt.colorbar()
    plt.show()
  
   


#Create only iron image
if True:
   
    # Convert to float
    img_2d = only_iron_array_ME.astype(float)
    

    # Rescale the values
    min_value = -40
    max_value = 150
    img_2d_scaled = np.clip((img_2d - min_value) / (max_value - min_value) * 250, 0, 250)
    px_array_ME_scaled = np.clip((px_array_ME - min_value) / (max_value - min_value) * 250, 0, 250)
    img_2d_scaled[´ö == 250] = 0

    #Create a mask of zero values in the original image
    zero_mask = px_array_ME_scaled == 0
    # Convert the mask to uint8 with value 0 where zeros are present
    zero_mask = zero_mask.astype(np.uint8) * 255


    
    # Convert to uint8
    blur = np.uint8(img_2d_scaled)


    # Apply blur filter
    blur = cv2.medianBlur(blur,5)
    for i in range(2):
      blur = cv2.medianBlur(blur,5)

  

    # Overlay the zero values of the original image onto the filtered image
    final_image = cv2.bitwise_or(blur, zero_mask)

    final_image[final_image == 255] = 0

    

    # Rescale the values
    min_value = -40
    max_value = 150
    final_image = np.clip((final_image - min_value) / (max_value - min_value) * 250, 0, 250)


    # Display images using matplotlib with color
    plt.subplot(131), plt.imshow(px_array_ME_scaled, cmap='viridis'), plt.title('Original ME')
    plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(blur, cmap='viridis'), plt.title('Iron removed')
    plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(final_image, cmap='viridis'), plt.title('Final Image')
    plt.xticks([]), plt.yticks([])
    plt.colorbar()
    plt.show()
  

   



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
