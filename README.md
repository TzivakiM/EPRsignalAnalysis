# EPRsignalAnalysis
Sample files used for analysis of spectra produced by the BRuker EPR software.
Input: ".asc" spectra files: B-field/Intensity measurement

Order of execution:
1. SignalHeights.py: Normalizes the x axis based on the B-field value of the standard and the x-axis based on the height of the standard intensity for each file in the containing folder
2. Output: csv file with signal heights (normalized as well as raw data)
3. dataAnalysis_outfiles.py: Takes the designated "background" dataset and subtracts it from all the irradiated sets on a sample basis. Calculates density normalization and the associated error. Can plot the data if uncommenting the relevant parts.

