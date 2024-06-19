# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 17:46:50 2021
Edited on July 2022

Make Verification in the same way as excel file

@author: iviejo, ajuan
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# %% FUNCTIONS
def data_analysis(Y_pred, Y_true, execution_folder):
    report = {}

    # (y-mediay)^2
    SStot = np.sum((Y_pred - np.mean(Y_pred)) ** 2)

    # Linear regression 1
    # fy1=1*x
    # (y-fy1)^2
    SSres_lr1 = np.sum((Y_pred - Y_true) ** 2)

    # linear regression 2
    # fy2=m*x+n
    # (y-fy2)^2
    linfit = np.polyfit(Y_true, Y_pred, 1)
    SSres_lr2 = np.sum((Y_pred - (linfit[0] * Y_true + linfit[1])) ** 2)
    # report['Coeff_corr_linear_regression']=1-(SSres_lr2/SStot)

    # Analysis based on absolute error
    error_abs = np.abs(Y_pred - Y_true)
    error_sorted = np.sort(error_abs)
    MeanAbsError = np.mean(error_abs)
    PerceMeanAbsError = np.mean(error_abs) / np.mean(abs(Y_true)) * 100
    Mean10peraxErrors = np.mean(error_sorted[-int(len(error_sorted) / 10):])
    PerceMean10peraxErrors = Mean10peraxErrors / np.mean(abs(Y_true)) * 100
    MaxAbsError = np.max(error_abs)
    PerceMaxAbsError = MaxAbsError / np.mean(abs(Y_true)) * 100
    report['Coeff_corr_linear_regression'] = 1 - (SSres_lr1 / SStot)
    report['Mean_absolute_error'] = MeanAbsError
    report['%(MeanabsError)'] = PerceMeanAbsError
    report['Mean10%ofMax_absolute_error'] = Mean10peraxErrors
    report['%(Mean10%ofMax_absolute_errors)'] = PerceMean10peraxErrors
    report['Maximum_absolute_error'] = MaxAbsError
    report['%(Maximum_absolute_error)'] = PerceMaxAbsError
    report['StdDesv_absolute_error'] = np.std(error_abs)
    report['MeanDesv_absolute_error'] = np.mean(np.abs(error_abs - np.mean(error_abs)))
    print(f"report: {report}")
    # Other analysis
    # report['Coeff_correlation']=np.sum((data[:,0]-np.mean(data[:,0]))*(data[:,1]-np.mean(data[:,1])))/(np.sum((data[:,0]-np.mean(data[:,0]))**2)*np.sum((data[:,1]-np.mean(data[:,1]))**2))**0.5

    if report is not None:
        report_df = pd.DataFrame([report])
        report_path = os.path.join(execution_folder, 'Report.csv')
        report_df.to_csv(report_path, index=False)
        print(f"REPORT PATH: {report_path}")
        print(f"report {report}")
    return report
