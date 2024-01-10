# UKBiobank_ECG
Python 3 code to parse and plot data from ECG XML files from the UK Biobank dataset
Dr Sunil Manohar (sunil.manohar@cardiov.ox.ac.uk)

**Summary**
This code is extracted from a project for machine learning using ECG data from the UK Biobank (summary of data source and type here: https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=20205) and is shared for anyone else wishing to extract data from the XML files.
Specifically, it parses the UK Biobank XML files into a numpy array containing all the lead values, and plots the data into traditional ECG visualisations which can be read by medical practitioners.
**Please note this only works with resting ECGs (UK Biobank field 20205) and not stress ECGs (field 6025).**

**Usage**

Use the import_ecg function in UKBiobank_ECG_parser.py.

Function inputs are:
- fname: pathname of XML file to import
- save_image_to: pathname of output for image file
- lead_order: names and order of leads to import

Function outputs are:
- ecg: numpy array of shape (number_of_leads, lead_length), containing all the extracted ECG trace values for each lead
- median_ecg: numpy array of shape (number_of_leads, lead_length), containing all the extracted median ECG trace values for each lead, as calculated by the ECG device at the point of acquisition
- metadata: dict containing information about the ECG, including filename, sample rate, timescale factor, voltage scale factor, and filters

Function effects are:
- saves a .svg image to save_image_to showing a full plot of all the lead data in the ECG file
- saves a .svg image to save_image_to + " median.svg" showing a plot of all the median lead data

**Dependencies**

Written and tested using Python 3.10 and the following packages:
- numpy 1.26.3
- matplotlib 3.8.0
- xmltodict 0.13.0

