import pydicom 
import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt 
import time 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#++++++++++++   INITIAL DEFINITIONS +++++++++++++++++

# Define the center coordinates and radius of the circular area
radius = 23


#define directory path where all DICOM Images are stored 
directory_in_str = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_04_08_LiverSample_LOW_HIGH/SPP_CntLowEnergyVolume/"
directory = os.fsencode(directory_in_str)

path =  "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/LowHigh_images/SPP_PrimaryRepresentation/Fe10cm_0mg_ml.CT.CaInsertTests_V.2.11.2024.03.28.15.09.16.931.72719327.dcm"


#Create and write in .csv file


csv_file_path = 'E:/UserData/z004x2zj/Documents/Iron_Code/Iron_CSV_Files/ROI_Liver_Values_Low.csv'

with  open(csv_file_path, mode='w', newline='') as file:
    file.write("Filename;Mode;Energy;Solution;Concentration;Diameter;Mean of ROI;Standard deviation\n")



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#++++++++++++   LOOP ITERATES OVER ALL FILES   +++++++++++++++++


for file in os.listdir(directory):
    filename = os.fsdecode(file)

    
    if filename.endswith(".dcm") or filename.endswith(".py"): 
        filepath = directory_in_str + filename
        ds = pydicom.dcmread(filepath)
        
        dicom_hu = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept
        try:
            dicom_hu = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept
        except:
            print("Error")
            continue

     
        
   


        ##############################################################################
        #Get necessary information from the header                   -> get list: https://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_6.html

        patientName = str(ds.PatientName)
        
        solution = "LiverSample"
        energy = str(ds.ImageComments)
        mode = str(ds.SeriesDescription)
        nameList = patientName.split("^")

        if patientName[10] == "1":
            ph_diameter = "small"
            concentration = nameList[1][0:2]

        elif patientName[10] == "2":
            ph_diameter = "large"
            concentration = nameList[1][0:2] 

        else:
            print("There is an error in the filename. At least one file isnt named the correct way")
   
        concentration = concentration.strip("m")
        if ph_diameter == "small":
            radius = 23
            center = (257, 265)
        elif  ph_diameter == "large":
            radius = 13
            center = (277, 186)


        # Create a meshgrid to get the coordinates of all pixels
        x, y = np.meshgrid(np.arange(dicom_hu.shape[0]), np.arange(dicom_hu.shape[1]))

        # Calculate the distance of each pixel from the center
        distance = np.sqrt((x - center[0])**2 + (y - center[1])**2)

        # Extract pixel information for pixels within the circular area
        pixels_in_circle = dicom_hu[distance <= radius]

        # Convert the pixel information to a list
        pixels_list = pixels_in_circle.tolist()

        length_list = len(pixels_list)

        #Calculate mean:
        sum_list = 0
        for i in pixels_list:
            sum_list = i + sum_list

        if length_list == 0:
            mean = 0
            print("There are no values in the list: " + filename)
        else:
            mean = sum_list / length_list
        round_mean = round(mean , 3)

        #Calculate standard deviation:
        sd_sum = 0 
        for i in pixels_list:
            sd_sum = sd_sum + (i - mean)**2
        stddev = math.sqrt(sd_sum/(length_list - 1))
        round_stddev = round(stddev , 3)



        ##############################################################################
        #Create and display mask to see if circle is in the correct place

        # Create a mask for the circular area
        circle_mask = np.zeros_like(dicom_hu)
        circle_mask[distance <= radius] = 1

        # Create a red overlay by setting the RGB channels to (1, 0, 0) for the circular area
        overlay = np.stack([dicom_hu, dicom_hu * (1 - circle_mask), dicom_hu * (1 - circle_mask)], axis=-1)

        plt.imshow(overlay)

        #############################################################################
        #Create and write in .csv file

        with  open(csv_file_path, mode='a', newline='') as file:
            string = filename +";"+ mode + ";" + energy + ";" + solution + ";" + concentration + ";" + ph_diameter + ";" + str(round_mean) + ";" + str(round_stddev) + "\n";    #see line 25 : ("Solution   ;Concentration  ;Diameter     ;Mean of ROI   ;Standard deviation   \n")
            file.write(string) 


        #Display the overlaid image
        # Show the plot
       # if ph_diameter == "large":
        #    plt.show()

        # Pause for 2 seconds
        #plt.pause(0.5)

        # Close the plot window
        #plt.close()
       


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

