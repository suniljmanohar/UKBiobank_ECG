# UKBiobank_ECG
Python 3 code to parse and plot data from ECG XML files from the UK Biobank dataset

Author & contact: Dr Sunil Manohar (sunil.manohar@cardiov.ox.ac.uk)

## Summary
This code is extracted from a project for machine learning using ECG data from the UK Biobank and is shared for anyone else wishing to extract data from the XML files.

Summary of data source and type here: https://biobank.ctsu.ox.ac.uk/crystal/field.cgi?id=20205

Specifically, it parses the UK Biobank XML files into a numpy array containing all the lead values, and plots the data into traditional ECG visualisations which can be read by medical practitioners.

**Please note use UKBiobank_ECG_parser.py with resting ECGs (UK Biobank field 20205) and UKBiobank_stress_ECG_parser.py with stress ECGs (field 6025).**

## Usage

Use the import_ecg function in UKBiobank_ECG_parser.py or UKBiobank_stress_ECG_parser.py.

**Function inputs:**
- fname (str): pathname of XML file to import
- save_image_to (str): pathname of output for image file
- lead_order (list): names and order of leads to import
- (for stress ECGs only) indices (list): indices of the median lead data to extract (usually 0-15) corresponding to different points in the stress test

**Function outputs:**
- ecg: numpy array of shape (number_of_leads, lead_length), containing all the extracted ECG trace values for each lead
- median_ecgs: numpy array of shape (number_of_leads, lead_length), containing all the extracted median ECG trace values for each lead, as calculated by the ECG device at the point of acquisition
- (for stress ECGs) median_ecgs: dict of form {idx1: leads1, ...} where idx is the index of the median lead data, and leads is a numpy array of shape (number_of_leads, lead_length), containing all the extracted median ECG trace values for each lead, as calculated by the ECG device at the point of acquisition
- metadata: dict containing information about the ECG, including filename, sample rate, timescale factor, voltage scale factor, and filters (contents differ for rest and stress ECGs)

**Function effects:**
- saves a .svg image to save_image_to showing a full plot of all the lead data in the ECG file
- saves a .svg image to save_image_to + " median.svg" showing a plot of all the median lead data
- (for stress ECGs) saves a .svg image to save_image_to + "_index={idx} median.svg" showing a plot of all the median lead data for index=idx

## Dependencies

Written and tested using Python 3.10 and the following packages:
- numpy 1.26.3
- matplotlib 3.8.0
- xmltodict 0.13.0

## Author
- <b>©2023 Sunil Manohar. All rights reserved</b>
