
import pydicom 
import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#++++++++++++   INITIAL DEFINITIONS +++++++++++++++++

# Define the center coordinates and radius of the circular area
center = (319, 319)
radius = 17


#define directory path where all DICOM Images are stored
directory_in_str = "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_03_ZM202_FE_10cm/"
directory = os.fsencode(directory_in_str)

path =  "E:/UserData/z004x2zj/Documents/Iron_Code/Iron_DICOM_Files/2024_03_ZM202_FE_10cm/Fe-DTPA10cm_2mg.CT.FeInsertTests(A.5.25.2024.03.26.15.52.13.798.58617420.dcm"



#Create and write in .csv file

csv_file_path = 'E:/UserData/z004x2zj/Documents/Iron_Code/Iron_CSV_Files/ROI_Values.csv'

with  open(csv_file_path, mode='w', newline='') as file:
    file.write("Filename ;Solution   ;Concentration  ;Diameter     ;Mean of ROI   ;Standard deviation   \n")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~









#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#++++++++++++   LOOP ITERATES OVER ALL FILES   +++++++++++++++++


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".dcm") or filename.endswith(".py"): 
        filepath = directory_in_str + filename
        ds = pydicom.dcmread(filepath)
        
        try:
            dicom_hu = ds.pixel_array * ds.RescaleSlope + ds.RescaleIntercept
        except:
            print(filename)
            continue

        # print(os.path.join(directory, filename))
        
   


    ##############################################################################
    #Get necessary information from the header                   -> get list: https://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_6.html

        patientName = str(ds.PatientName)
        list_firstandlastname = patientName.split("^")

        if len(list_firstandlastname[0]) == 6:
            solution = "Fe"
            ph_diameter = list_firstandlastname[0][2:]

        elif len(list_firstandlastname[0]) == 11:
            solution = "Fe-DTPA"
            ph_diameter = list_firstandlastname[0][7:] 

        else:
            print("There is an error in the filename. At least one file isnt named the correct way")
   

        try:
            concentration = list_firstandlastname[1]
        except:
            print("There is at least one file with a missing concentration")
            concentration = "No concentration given" 
            continue
   



        ##############################################################################
        #Get Pixles and calculate mean and stand dev:

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
            string = filename +";"+solution + ";" + concentration + ";" + ph_diameter + ";" + str(round_mean) + ";" + str(round_stddev) + "\n";    #see line 25 : ("Solution   ;Concentration  ;Diameter     ;Mean of ROI   ;Standard deviation   \n")
            file.write(string) 


        # Display the overlaid image
        #plt.show()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~