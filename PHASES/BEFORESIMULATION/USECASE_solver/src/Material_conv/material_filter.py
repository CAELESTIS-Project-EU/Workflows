# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 12:16:44 2024

@author: Said Abdelmonsef (said.abdelmonsef@udg.edu)
"""
import os

os.environ["OMP_NUM_THREADS"] = "4"

from pathlib import Path
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

import sklearn

sklearn.set_config(assume_finite=True)


def group_vf_vv(Element_IDs, Vf, Vv, n_f, params_micro):
    """
    Group a dataset based on the values of Vf and Vv using K-Means clustering.

    Parameters:
    Vf (array-like): Array of values for Vf 
    Vv (array-like): Array of values for Vv 
    n_f (int): Number of groups to create (clusters)

    Returns:
    np.ndarray: Dataset with Vf, Vv, and the assigned group number.
    """

    # Combine Vf and Vv into pairs
    data = np.column_stack((Vf, Vv))

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=n_f, n_init=10, random_state=0).fit(data)

    # Get cluster labels (group numbers)
    group_numbers = kmeans.labels_

    # Assign group numbers to the dataset
    grouped_data = np.column_stack((data, group_numbers))

    # Store groups in a dictionary
    groups_dict = {i: [] for i in range(n_f)}
    for i, group in enumerate(group_numbers):
        groups_dict[group].append({'Vf': data[i][0], 'Vv': data[i][1]})

    fiber_material  = params_micro['Fiber']
    matrix_material = params_micro['Matrix']
    
    # calculate means
    group_mean_prop = {}
    for group, values in groups_dict.items():
        Vf_values = [v['Vf'] for v in values]
        Vv_values = [v['Vv'] for v in values]
        mean_vf = np.mean(Vf_values)
        mean_vv = np.mean(Vv_values)
        properties = Mori_Tanaka_multiple_cons(mean_vf, mean_vv, fiber_material, matrix_material)
        group_mean_prop[group] = {
            'mean_Vf': mean_vf,
            'mean_Vv': mean_vv,
            'title': properties[0],
            'E11_MT': properties[1],
            'NU12_MT': properties[2],
            'E22_MT': properties[3],
            'G12_MT': properties[4],
            'G23_MT': properties[5],
            'NU23_MT': properties[6]
        }

    # outputs
    material_output = {'Element_ID': Element_IDs, 'Vf': Vf, 'Vv': Vv, 'material_ID': grouped_data[:, 2],
                       'material_no': n_f, 'material_groups': group_mean_prop}

    return material_output


def Mori_Tanaka_multiple_cons(V_fiber, V_void, fiber_material, matrix_material):
    '''
    The Python function calculates the analytical results following Mori-Tanaka strategy
    From: Melro

    Author
    -----
         Oriol Vallmajo Martin
         oriol.vallmajo@udg.edu
         AMADE research group, University of Girona (UdG), Girona, Catalonia

    Args
    -----
    V_fiber : float
            Fiber volume fraction
    V_void : float
            Void volume fraction
    fiber_material : str
            Name of the fiber material
    matrix_material : str
            Name of the matrix material
    void_material : str
            Name of the void material
    Kwargs
    -----
        none

    Return
    --------
    dict_anal : dict
             Dictionary with all the results

    Examples
    -----
        none

    Raises
    -----
        none

    Note
    -----
        none

    Program called by
    -----
        none

    Program calls
    -----
        none
    '''
    Vf = V_fiber
    Vv = V_void
    Vm = (1 - Vf - Vv)
    # Get the fibers material properties
    Ef1  = float(fiber_material['Ef1'])
    Ef2  = float(fiber_material['Ef2'])
    Gf12 = float(fiber_material['Gf12']) 
    Gf23 = float(fiber_material['Gf23']) 
    vf12 = float(fiber_material['vf12'])
    # Get the matrix material properties
    Em   = float(matrix_material['Em'])
    Gm   = float(matrix_material['Gm'])
    vm   = float(matrix_material['vm'])
    # Get the voids material properties
    dummy_material = 0.001
    #
    #CALCULATE THE ELASTIC PROPERTIES
    #One constituent:
    if V_void == 0.:
        title = 'Mori Tanaka - One constituent'
        #
        mm = Gm
        mf = Gf23
        pf = Gf12
        pm = Gm
        kmh = -1 / (1 / Gm - 4 / Em + 4 * vm * vm / Em)
        kfh = -1 / (1 / Gf23 - 4 / Ef2 + 4 * vf12 * vf12 / Ef1)
        k_star = (kfh * kmh + mm * (Vf * kfh + Vm * kmh)) / (Vf * kmh + Vm * kfh + mm)
        #
        lf = 2 * kfh * vf12
        lm = 2 * kmh * vm
        l_star = (Vf * lf * (kmh + mm) + Vm * lm * (kfh + mm)) / (Vf * (kmh + mm) + Vm * (kfh + mm))
        #
        nf = Ef1 + 4 * kfh * vf12 * vf12
        nm = Em + 4 * kmh * vm * vm
        n_star = Vf * nf + Vm * nm + (l_star - Vf * lf - Vm * lm) * (lf - lm) / (kfh - kmh)
        #
        G23_MT = round((mm * mf * (kmh + 2 * mm) + kmh * mm * (Vf * mf + Vm * mm)) / (
                    kmh * mm + (kmh + 2 * mm) * (Vf * mm + Vm * mf)), 2)
        G12_MT = round((2 * Vf * pf * pm + Vm * (pf * pm + pm * pm)) / (2 * Vf * pm + Vm * (pf + pm)), 2)
        E1_MT = round(n_star - l_star * l_star / k_star, 2)
        v12_MT = round(l_star / k_star / 2, 2)
        E2_MT = round(4. / (1. / k_star + 1. / G23_MT + 4 * v12_MT * v12_MT / E1_MT), 2)
        v23_MT = round(E2_MT / G23_MT / 2 - 1, 2)
    #
    #Multiple inclusions
    #Source: Chen1992MoriTanaka
    else:
        title = 'Mori Tanaka - Multiple constituents'
        #
        mm = Gm
        mf = Gf23
        mv = dummy_material
        pf = Gf12
        pm = Gm
        pv = dummy_material
        kmh = -1 / (1 / Gm - 4 / Em + 4 * vm * vm / Em)
        kfh = -1 / (1 / Gf23 - 4 / Ef2 + 4 * vf12 * vf12 / Ef1)
        kvh = -1 / (1 / dummy_material - 4 / dummy_material + 4 * dummy_material * dummy_material / dummy_material)
        lf = 2 * kfh * vf12
        lm = 2 * kmh * vm
        lv = 2 * kvh * dummy_material
        nf = Ef1 + 4 * kfh * vf12 * vf12
        nm = Em + 4 * kmh * vm * vm
        nv = dummy_material + 4 * kmh * dummy_material * dummy_material
        #
        p = ((Vm * pm / (pm + pm)) + (Vf * pf / (pm + pf)) + (Vv * pv / (pm + pv))) / (
                    (Vm / (pm + pm)) + (Vf / (pm + pf)) + (Vv / (pm + pv)))
        gamma_m = (1 / mm + 2 / kmh) ** (-1)
        m = ((Vm * mm / (mm + gamma_m)) + (Vf * mf / (mf + gamma_m)) + (Vv * mv / (mv + gamma_m))) / (
                    (Vm / (mm + gamma_m)) + (Vf / (mf + gamma_m)) + (Vv / (mv + gamma_m)))
        k = ((Vm * kmh / (kmh + mm)) + (Vf * kfh / (kfh + mm)) + (Vv * kvh / (kvh + mm))) / (
                    (Vm / (kmh + mm)) + (Vf / (kfh + mm)) + (Vv / (kvh + mm)))
        l = ((Vm * lm / (kmh + mm)) + (Vf * lf / (kfh + mm)) + (Vv * lv / (kvh + mm))) / (
                    (Vm / (kmh + mm)) + (Vf / (kfh + mm)) + (Vv / (kvh + mm)))
        n = (Vm * nm + Vf * nf + Vv * nv) - Vm * (lm - lm) ** 2 / (kmh + mm) - Vf * (lf - lm) ** 2 / (kfh + mm) - Vv * (
                    lv - lm) ** 2 / (kvh + mm) + \
            (((Vm * (lm - lm) / (kmh + mm) + Vf * (lf - lm) / (kfh + mm) + Vv * (lv - lm) / (kvh + mm)) ** 2) / (
                        (Vm / (kmh + mm)) + (Vf / (kfh + mm)) + (Vv / (kvh + mm))))
        #
        G23_MT = round(m, 2)
        G12_MT = round(p, 2)
        E1_MT = round(n - l * l / k, 2)
        v12_MT = round(l / k / 2, 2)
        E2_MT = round(4. / (1. / k + 1. / G23_MT + 4 * v12_MT * v12_MT / E1_MT), 2)
        v23_MT = round(E2_MT / G23_MT / 2 - 1, 2)

    return title, E1_MT, v12_MT, E2_MT, G12_MT, G23_MT, v23_MT


def material_output_debug(lperm_path_file, voids_path_file):
    file_voids = True
    # Example usage:
    num_samples = 1000
    if file_voids:
        Vv = np.loadtxt(voids_path_file) / 100
        num_samples = len(Vv)
    else:
        # Generate Vv values between 0 and 0.02
        Vv = np.random.uniform(0, 0.02, num_samples)

    # Generate Vf values between 0.4 and 0.6
    lperm_file_ = True

    if lperm_file_:
        # Define the file path
        file_path = Path(lperm_path_file)

        # Define the column names
        column_names = [
            'Element_ID', 'Thickness', 'Fiber_Content', 'K1', 'K2', 'K3',
            'Perm_Vec1_x', 'Perm_Vec1_y', 'Perm_Vec1_z',
            'Perm_Vec2_x', 'Perm_Vec2_y', 'Perm_Vec2_z'
        ]

        # Read the file into a DataFrame with specified column names
        data = pd.read_csv(file_path, delim_whitespace=True, header=None, names=column_names, skiprows=1)

        Element_IDs = data['Element_ID']
        Vf = data['Fiber_Content']
        # Vv should have the same length (this an issue in the files we received)
        Vv = Vv[:len(Vf)]
    else:
        Vf = np.random.uniform(0.49, 0.54, num_samples)

    n_f = 10  # Number of groups to create (clusters)
    material_output = group_vf_vv(Vf, Vv, n_f)

    return material_output




