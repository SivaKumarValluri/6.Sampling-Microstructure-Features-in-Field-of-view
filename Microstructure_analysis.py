# -*- coding: utf-8 -*-
"""
Created on Wed May 17 14:14:26 2023

@author: Siva Kumar Valluri

Functions and classes to help process microstructure images and relate them to PMT generated radiance integrals
"""

"""
Microstructure Analysis#################################################################################################################################################
Processes large segmented cross-section SEM images that function as microstructure images 
(several tens of micrometers larger than PMT field of observation)
by superimposing several randomly placed rectangular field of observation 90 x60 micron arrive at statistics of features typically seen by PMT

Requires:
-Folder of segmented microstructure images (cross-section images) where features of interest need to be white
-Scale for each image in the form of 'x' pixels/micron as it will be a user input for each image

Returns:
-Excel workbook, with each sheet documenting number of features and their cumulative area fraction in field of PMT observation
##############################################################################################################################################################
""" 
import math
import random
from shapely.geometry import Polygon, Point
import cv2 
import numpy as np
import pandas as pd

"""
Rectangle generator in space##################################################################################################################################################
Generates randomly orientated rectangle of user provided size 
along with information if generated rectangle is inside or outside user provided X-Y space (rectangular) 

Requires:
- length and breadth of rectangle
- spatial limitations within which rectangle needs to be spawned    

Returns:
- coordinates of generated rectangle corners
- centroid of generated rectangle
- half-diagonal of generated rectangle
- user provided restricted space coordinates (rectangle)
- If generated rectangle is within user privided space in the form of True (inside) or False (outside)


rectangle class repurposed from square class in
https://stackoverflow.com/questions/46081491/how-to-generate-squares-randomly-located-equally-sized-randomly-rotated-that

#Example use case 
import matplotlib.pyplot as plt
r = Rectangle(10,5,0,0,50,50)
(x0, y0), (x1, y1), (x2, y2), (x3, y3) = r.corners
(X0, Y0), (X1, Y1), (X2, Y2), (X3, Y3) = r.frame
plt.plot([x0, x1, x2, x3, x0], [y0, y1, y2, y3, y0]) # randomly generated rectangle
plt.plot([X0, X1, X2, X3, X0], [Y0, Y1, Y2, Y3, Y0]) # Image frame
r.in_or_out()
###############################################################################################################################################################
""" 
class Rectangle():
    """Requires length and breadth of rectangle along with min/max limits of image within which we intend to draw our rectangle"""
    def __init__(self, length, breadth, minx, miny, maxx, maxy, safety_margin=0): #Only integers!
        self.length = length
        self.breadth = breadth
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.safety_margin = safety_margin
        
        """First point of the rectangle"""
        x0 = self.safety_margin + random.random() * (self.maxx - self.minx - 2 * self.safety_margin)
        y0 = self.safety_margin + random.random() * (self.maxy - self.miny - 2 * self.safety_margin)
        
        theta = random.randint(0, 90) * math.pi / 180  # Angle of rotation
        
        self.x1 = x0 + (self.length * math.cos(theta))
        self.x2 = self.x1 + (self.breadth * math.cos((90 * math.pi/180) + theta))
        self.x3 = self.x2 + (self.length * math.cos((180 * math.pi/180) + theta))
        self.y1 = y0 + (self.length * math.sin(theta))
        self.y2 = self.y1 + (self.breadth* math.sin((90 * math.pi/180) + theta))
        self.y3 = self.y2 + (self.length * math.sin((180 * math.pi/180) + theta))
        self.corners = ((x0, y0), (self.x1, self.y1), 
                        (self.x2, self.y2), (self.x3, self.y3))
        self.frame = ((self.minx, self.miny), (self.maxx, self.miny), 
                        (self.maxx, self.maxy), (self.minx, self.maxy))

    @property
    def center(self):
        """(x, y) of the center of the polygon."""
        return Polygon(self.corners).centroid.coords[0]

    @property
    def half_diag(self):
        """The distance of 1/2 the shape's diagonal (center-to-corner)."""
        p0, p1, p2, p3 = self.corners
        return 0.5 * Point(p0).distance(Point(p1))* math.sqrt(2)
    
    def in_or_out(self):
        """To find out if all corners of generated rectangle are within the image frame"""
        coords = [(self.minx, self.miny), (self.maxx,self.miny), (self.maxx,self.maxy), (self.minx,self.maxy)]
        poly = Polygon(coords)
        p0, p1, p2, p3 = self.corners
        p0 = Point(p0)
        p1 = Point(p1)
        p2 = Point(p2)
        p3 = Point(p3)
        if p0.within(poly) and p1.within(poly) and p2.within(poly) and p3.within(poly):
            return True
        else:
            return False


"""
Address importer##################################################################################################################################################
To collect addresses of items in a folder. 
Note: Ensure folder has only the relevant images as it doesnt differentiate between csv files, tif, jpg, etc.

Requires:
- User input for folder address with images. Simple copy paste

Returns:
- List of individual image addresses
###############################################################################################################################################################
""" 
def importer():
    folder_address = input("Enter address of folder with segmented microstructure images: ")
    import os
    image_set_names = []
    tiff_images_addresses = []
    for root, subfolders, filenames in os.walk(folder_address):
        for filename in filenames:
            image_set_names.append(root.rpartition('\\')[2])
            tiff_images_addresses.append(root + "/" + filename)                          
    return tiff_images_addresses, folder_address 
    
"""
Microstructure image analyzer##################################################################################################################################################
Reads imags from provided address

Requires:
- image address
- maximum number of random rectangle generated

Returns:
- Datasheet (pandas dataframe) of number of features and their cumulate area fraction within rectangle for each run
###############################################################################################################################################################
""" 

def image_analyzer(image_address, folder_address, Max_runs = 5):
    image = cv2.imread(image_address,cv2.IMREAD_GRAYSCALE)
    X = image.shape[0]
    Y = image.shape[1]
    sheet_name = image_address.rpartition('\\')[2].rpartition('/')[2].rpartition('.')[0]
    name_list.append(sheet_name)
        
    #Open cv fils X and Y while handing data
    imS = cv2.resize(image, (int(Y/3),int(X/3))) #reducing image size to display image
    cv2.imshow('Imported image', imS)
    cv2.waitKey(0)
        
    while True:
        choice1=input("Want to invert image? (Y/N): ").lower() # So that user input is not case-senitive
        try:
            if choice1.lower() in  ["y","yes","yippee ki yay","alright","alrighty"]:
                print("noted")
            elif choice1.lower() in ["n","no","nope"]:
                print("noted")
            else:
                raise Exception("Invalid input! Answer can only be 'Yes' or 'No'")
        except Exception as e:
            print(e)    
        else:
            break           
    if choice1.lower() in  ["y","yes","yippee ki yay","alright","alrighty"]:        
        image = cv2.bitwise_not(image)
        imS2 = cv2.resize(image, (int(Y/3),int(X/3))) #reducing image size to display image
        cv2.imshow('Imported image', imS2)
        cv2.waitKey(0)
        
    scale = float(input("Enter scale for image (How many pixels/micron): ")) 
    rectx = int(float(scale*90))
    recty = int(float(scale*60))
          
    i = 0     
    summaray_number_of_elements = []
    summary_area_fraction = []
    while i < Max_runs:
        rect = Rectangle(rectx,recty,0,0,Y,X) #flipping X and Y cause of Open cv
        if rect.in_or_out():
            i = i+1
            mask = np.zeros_like(image)
            contours = np.asarray(rect.corners)
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
            cv2.fillPoly(mask, pts = np.int32([contours]), color =(255,255,255))
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            """#Displaying generated mask
            imS = cv2.resize(mask, (int(Y/3),int(X/3))) #reducing image size to display image
            cv2.imshow('Imported image', imS)
            cv2.waitKey(0)"""
            features_in_rectangle_frame = cv2.bitwise_and(image,image, mask = mask)  
            """#Displaying masked portion of microstructure
            imS = cv2.resize(features_in_rectangle_frame, (int(Y/3),int(X/3))) #reducing image size to display image
            cv2.imshow('Imported image', imS)
            cv2.waitKey(0)"""
                
            contours, hierarchy = cv2.findContours(features_in_rectangle_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            contour_new =[]
            cc=list(contours)
            for contournumber in range(0, len(cc),1):
                M = cv2.moments(cc[contournumber])
                if (cc[contournumber].shape[0] > 2 and M['m00'] > 0): 
                    contour_new.append(cc[contournumber])  
                
            contours = tuple(contour_new)                
            Area_total = []
            for contour_number in range(0,len(contours),1):
                cnt = contours[contour_number]
                area = cv2.contourArea(cnt)
                Area_total.append(area)
            
            #Image display to verify region selection
            image_copy = features_in_rectangle_frame.copy()
            image_copy = cv2.cvtColor(image_copy, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=[0,0,250], thickness=2, lineType=cv2.LINE_AA)
            #imS3 = cv2.resize(image_copy, (int(Y/3),int(X/3))) #reducing image size to display image           
            #cv2.imshow('Imported image', imS3)
            #cv2.waitKey(0)
            cv2.imwrite(str(folder_address)+'\\'+'Frame'+ str(i)+ '.tif', image_copy)
                
            summary_area_fraction.append(sum(Area_total)/(rectx*recty))
            summaray_number_of_elements.append(len(contours))
                
    data_in_sheet = np.array(list(zip(summaray_number_of_elements,summary_area_fraction)))
    Data_sheet = pd.DataFrame(data_in_sheet)
    Data_sheet.columns = ['Number', 'Area fraction'] 
    return Data_sheet

"""
Microstructure Analysis#################################################################################################################################################
Processes large microstructure images (several tens of micrometers larger thanPMT field of observation)
by superimposing several randomly placed rectangular field of observation 90 x60 micron arrive at statistics of features typically seen by PMT

Requires:
-Folder of segmented microstructure images (cross-section images) where features of interest need to be white
-Scale for each image in the form of 'x' pixels/micron as it will be a user input for each image

Returns:
-Excel workbook, with each sheet documenting number of features and their cumulative area fraction in field of PMT observation
##############################################################################################################################################################
"""   
Excelwriter = pd.ExcelWriter('Microstructure Analysis.xlsx', engine='xlsxwriter')
Data_list = []
name_list = []
tiff_images_addresses, folder_address = importer()    
for number,image_address in enumerate(tiff_images_addresses):
    Data_sheet = image_analyzer(image_address, folder_address, Max_runs = 100)
    Data_list.append(Data_sheet)
    print("image number" + str(number) +" processed")
    
for i, file in enumerate (Data_list):
    file.to_excel(Excelwriter, sheet_name=str(name_list[i]),index=False)
Excelwriter.save()
Excelwriter.close()


####
import tifffile
tif =  tifffile.TiffFile(r'C:\Users\sivak\OneDrive - University of Illinois - Urbana\Desktop\New folder\500X-BSE_001.tif')
print(tif.fei_metadata['Scan']['PixelWidth'])