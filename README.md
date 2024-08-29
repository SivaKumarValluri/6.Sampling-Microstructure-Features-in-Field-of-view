# Quantifying-Heterogenous-Material-Microstructure
## Overview ##
This software package processes segmented cross-sectional scanning electron microscopy (SEM) images to estimate features observed by a photomultiplier tube (PMT). The primary goal is to analyze large microstructure images by superimposing randomly placed rectangular fields of observation and computing statistics on the features within these fields.

## Features ##
1.Microstructure Analysis: Processes SEM images to provide statistics on features observed by PMT.

2.Rectangle Generator: Generates randomly oriented rectangles within specified spatial constraints.

3.Address Importer: Collects image file paths from a specified folder.

4.Image Analyzer: Analyzes each image by applying randomly placed rectangles and calculates feature statistics.

5.Output: Generates an Excel workbook with detailed analysis results.

## Requirements ##
-Images: Folder containing segmented microstructure images (cross-section images) where features of interest are highlighted in white.

-Scale: Scale information for each image in pixels per micron.

-Libraries: Requires math, random, shapely, cv2, numpy, pandas, and tifffile Python libraries.

## Function and Class Details ##
1. Rectangle Class
   
    -Purpose:Generates randomly oriented rectangles within a specified rectangular space.
     
    -Constructor:
   
        -length: Length of the rectangle.
   
        -breadth: Breadth of the rectangle.
   
        -minx, miny: Minimum x and y coordinates of the space.
   
        -maxx, maxy: Maximum x and y coordinates of the space.
   
        -safety_margin: Margin to avoid edge issues.
        
    -Methods:
   
        -center: Returns the centroid of the rectangle.
   
        -half_diag: Returns half of the diagonal length of the rectangle.
   
        -in_or_out: Checks if the rectangle is entirely within the specified space.
      
2. importer Function
   
    -Purpose:Collects addresses of images in a specified folder.
    
    -Returns:
   
        -List of image file addresses.
   
        -Folder address.
      
3. image_analyzer Function
   
    -Purpose:Analyzes an image by superimposing randomly placed rectangles and computes feature statistics.
    
    -Parameters:
   
        -image_address: Path to the image file.
   
        -folder_address: Path to the folder containing the image.
   
        -Max_runs: Maximum number of random rectangles to generate.
   
    -Returns: A Pandas DataFrame with:
   
        -Number of features within the rectangle.
   
        -Cumulative area fraction of the features.
   
4. Main Script Execution
   
    -Purpose: Processes all images in the specified folder, analyzes them, and saves results to an Excel workbook.
   
    -Steps:
   
        -Import image addresses using importer.
   
        -Analyze each image using image_analyzer.
   
        -Save results to an Excel workbook named 'Microstructure Analysis.xlsx'.

## Notes ##
-Ensure images are segmented correctly, with features of interest in white.

-Verify that the scale information for each image is accurate.

-The software will prompt for user input during execution, including whether to invert images and the scale of the image.

## Troubleshooting ##

-Invalid Input: The software expects specific responses (e.g., 'Y' or 'N'). Ensure inputs are case-insensitive.

=Library Issues: Ensure all required libraries are installed.

This manual provides a comprehensive overview of the software's capabilities and usage. For further assistance, refer to the source code comments or contact the author.

Feel free to adjust any section based on your specific needs or use cases!
