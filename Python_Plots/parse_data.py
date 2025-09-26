# Author: Cameron Liu
# 
# Purpose: This file is dedicated to parsing all the information from the HPC simulation from a file, and putting the only 
# things that I need in the file. If you import this file, you will get all the methods from this file and be able to call it 
# in another file. 

import statistics  
import numpy as np   
from scipy import stats
import os
import tskit
import io
import pandas as pd


debug = False


# If you want to re-create and use these sims, replace home_directory with the directory where the sims are stored. 
home_directory = "/Users/cameronliu/Desktop/Research/Datasets"


# These methods are used for purely editing and gathering information from the file

# This method iterates through the file, and stores the information in a tuple of a tuple, then stores that in a list 
#
# It returns this tuple of tuples stored in a list, as well as the timesteps. This is just the raw data, with no slicing                                                                                                                                                                                                                                                                                                            
def parse(uds, sd, burnin):                                                                                 
    data = []
    timesteps = []
    for ud in uds: 
        if burnin: 
            # sd = 0.01
            filename = home_directory + "/sd-" + str(sd) + "/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_0.010000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"           
        else:
            # sd = 0.0025
            filename = home_directory + "/sd-" + str(sd) + "/datafor_relative_tskitstatus_OFF_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_0.002500/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"


        file_data = []
        with open(filename, "r") as file:
            next(file) # skips the first line
            for line in file: 
                line = line.strip().split(",")
                if len(timesteps) < 20000: # Skips adding after the 0 - 20,000 timesteps
                    timesteps.append(line[0])
                file_data.append(float(line[3]))
            data.append(("sd-" + str(sd), (ud, file_data)))
        print(f"------------------------\nSuccessfully Parsed Data for file SD = {sd}, UD = {ud}\n------------------------\n")
    return data, timesteps


# This parses the exponential data from the data files. 
def parse_exp(uds, sd, tskit): 
    data = []
    timesteps = []
    for ud in uds: 
        if tskit: # Has tskit on
            filename = home_directory + "/sd-" + str(sd) + "-exp-reformatted/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "00/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
        else: # Has tskit of
            filename = home_directory + "/sd-" + str(sd) + "-exp-reformatted/datafor_relative_tskitstatus_OFF_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
        

        file_data = []
        with open(filename, "r") as file:
            next(file) # skips the first line
            for line in file: 
                line = line.strip().split(",")
                if len(timesteps) < 20000: # Skips adding after the 0 - 20,000 timesteps
                    timesteps.append(line[0])
                if not debug:
                    file_data.append(float(line[4]))
            data.append(("sd-" + str(sd), (ud, file_data)))
        print(f"------------------------------------------------\nSuccessfully Parsed Exponential Data for file SD = {sd}, UD = {ud}\n------------------------------------------------\n")
    return data, timesteps

# This function parses the normal data from the Exponentiated Datafiles. 
# This is becuase Ulises and I were testing the Exponentiated Datasets.
def parse_normal_from_exp(uds, sd, tskit): 
    data = []
    timesteps = []
    for ud in uds: 

        filename = get_directory_no_curr(ud, sd, tskit, False)

        file_data = []
        with open(filename, "r") as file:
            next(file) # skips the first line
            for line in file: 
                line = line.strip().split(",")
                if len(timesteps) < 20000: # Skips adding after the 0 - 20,000 timesteps
                    timesteps.append(line[0])
                if not debug:
                    file_data.append(float(line[3]))
            data.append(("sd-" + str(sd), (ud, file_data)))
        print(f"---------------------------------------------------------\nSuccessfully Parsed Normal Data for file SD = {sd}, UD = {ud}\n---------------------------------------------------------\n")
    return data, timesteps


# This function came from a big error in mine: I didn't realize the bash array didn't have commas in it. 
# Useful to have and keep - it just removes the commas from the name of the files - even the subfiles. 
# 
def remove_commas_recursively(root_dir: str):
    message = False
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Rename files
        for filename in filenames:
            if "," in filename:
                message = True
                old_path = os.path.join(dirpath, filename)
                new_filename = filename.replace(",", "")
                new_path = os.path.join(dirpath, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed file: {old_path} -> {new_path}")
        
        # Rename directories
        for dirname in dirnames:
            if "," in dirname:
                old_path = os.path.join(dirpath, dirname)
                new_dirname = dirname.replace(",", "")
                new_path = os.path.join(dirpath, new_dirname)
                os.rename(old_path, new_path)
                print(f"Renamed directory: {old_path} -> {new_path}")
    return message

            

    


# This method slices the data for the given burn-in time
# It slices the both the dataset, but also timesteps as well
# 
# This method returns the sliced data, and the sliced timesteps 
def slice_data(data, timesteps, burnin):
    sliced = []
    sliced_timesteps = list(map(int, timesteps[burnin:]))
    for sd, (ud, dataset) in data:
        dataset = dataset[burnin:]
        sliced.append((sd, (ud, dataset)))
    return sliced, sliced_timesteps


def sort_csv(location, sort_by):
    sorted = []

    filename = location
    with open(filename, "r") as file: 
        next(file)
        for line in file: 
            line = line.strip().split(",")
            data_type = type(line[2])
            if (data_type(line[2]) == data_type(sort_by)):  
                sorted.append((line[0], line[1]))
    sorted.sort()
    return sorted



# Takes the moving average
def moving_average(data, window):
    weights = np.ones(window) / window
    return np.convolve(data, weights, mode='valid')


# Transforms the data, after being given sliced data. 
def transform_data(sliced_data): 
    transformed_datasets = []
    for (sd, (ud, data)) in sliced_data:
        transformed_data, transformed_lambda = stats.boxcox(data) # Returns the transformed data, and the lambda respective to the function
        transformed_mean = statistics.mean(transformed_data)
        transformed_datasets.append((sd, (ud, (transformed_data, transformed_lambda, transformed_mean))))

    return transformed_datasets


# Section to go from Selective Deaths to Ne
def back_transform(transformed_datasets):
    back_transformed_uds = []
    for ((sd, (ud, (transformed_data, transformed_lambda, transformed_mean)))) in transformed_datasets: 
        # Uses equation, and stores it into the value - Find equation on doc if needed more information about back-transforming
        # Sharepoint -> MutationLoad -> Cameron Liu -> Cameron Project Details
        back_transformed_value = ((float(transformed_lambda) * float(transformed_mean) + 1) ** (1 / float(transformed_lambda)))

        back_transformed_uds.append((ud, 1 - (back_transformed_value), sd))
    return back_transformed_uds


# Back transforms the whole dataset, alongside the Upper and Lower Bounds for calculating the Error Bars, and returns the back-transformed error bars
def back_transform_ste(transformed_datasets):
    back_transformed_data = []
    for (sd, (ud, (transformed_data, transformed_lambda, transformed_mean))) in transformed_datasets: 
        back_transformed_value = ((float(transformed_lambda) * float(transformed_mean) + 1) ** (1 / float(transformed_lambda)))

        trans_lower_bound, trans_upper_bound = get_bounds_singular(transformed_data, transformed_mean, 12000)

        back_transformed_lower = ((float(transformed_lambda) * float(trans_lower_bound) + 1) ** (1 / float(transformed_lambda)))
        back_transformed_upper = ((float(transformed_lambda) * float(trans_upper_bound) + 1) ** (1 / float(transformed_lambda)))

        # return sd too
        back_transformed_data.append((ud, 1 - back_transformed_value, sd, (back_transformed_lower, back_transformed_upper)))

    return back_transformed_data


# Generally this should be unused. I am keeping this in here, just so no function editing is needed. 
def back_div_2(transformed_datasets):
    back_transformed_uds = []
    for ((sd, (ud, (transformed_data, transformed_lambda)))) in transformed_datasets: 
        # Gets the Transformed Mean of all of the data
        transformed_mean = statistics.mean(transformed_data)

        # Uses equation, and stores it into the value - Find equation on doc if needed more information about back-transforming
        # Sharepoint -> MutationLoad -> Cameron Liu -> Cameron Project Details
        back_transformed_value = ((float(transformed_lambda) * float(transformed_mean) + 1) ** (1 / float(transformed_lambda)))

        back_transformed_uds.append((ud, 1 - (back_transformed_value / 2), sd))
    return back_transformed_uds


def calculate_variance_after_selection(ud, sd):
    # ud * (-(sd - 1.0)(sd - 2.0)) * 2(sd - 1.0)
    return np.exp(ud) * ((np.exp(-(sd - 1.0) * (sd - 2.0))) - np.exp(2 * (sd - 1.0)))

# This is the final transformation that the dataset goes through. 
def transform_nereproductive_rate(back_transformed_uds):
    transformed_data = []

    for ud, back_transformed_value, sd in back_transformed_uds:
        ne_reproductive_rate = (2.0 / (1.0 + 2 * calculate_variance_after_selection(float(ud), float(sd[3:])) + 1.0))
        #ne_reproductive_rate = (2.0 / (2.0 + calculate_variance_after_selection(float(ud), float(sd[3:]))))

        multiplied_value = back_transformed_value * ne_reproductive_rate

        # Add the value to a list once generated
        transformed_data.append((ud, multiplied_value, sd))

    return transformed_data

# Back-transform the data, then call calculate_variance..(). Then, call transform_nereproductive_rate(), to get the final back-transformed and applied data. 


# This is used to calculate standard error. Not sure where I'm going wrong, but this is for that. Unsure if this works properly 
def transform_nereproductive_rate_ste(back_transformed_uds):
    transformed_data = []

    for ud, back_transformed_value, sd, (bt_lower, bt_upper) in back_transformed_uds:
        ne_reproductive_rate = (
            2.0 / (1.0 + 2 * calculate_variance_after_selection(float(ud), float(sd[3:])) + 1.0)
        )

        multiplied_value = back_transformed_value * ne_reproductive_rate
        multiplied_lower = bt_lower * ne_reproductive_rate
        multiplied_upper = bt_upper * ne_reproductive_rate

        transformed_data.append((ud, multiplied_value, (multiplied_lower, multiplied_upper)))

    return transformed_data







        
# Not used unless you are using Matheson's msprime data. Typically do not need to use. 
def get_matheson_dataset(sd):
    # Uses the sd of the file to detemrine which dataset to use
    matheson_dataset = []
    if sd == 0.01: 
        matheson_dataset = sort_csv("/Users/cameronliu/Desktop/Research/Datasets/matheson_datasets/BGSpaperdataforFigure1A.csv", 2000)
    elif sd == 0.0025: 
        matheson_dataset = sort_csv("/Users/cameronliu/Desktop/Research/Datasets/matheson_datasets/BGSpaperdataforFigure1B.csv", 0.0025)
    else:
        matheson_dataset = sort_csv("/Users/cameronliu/Desktop/Research/Datasets/matheson_datasets/BGSpaperdataforFigure1B.csv", 0.04)

    # Ideally, I should convert to float when I do it above. 
    # Matheson's file has a string value in some of them, like "0.edsrxz" in Figure1B. So I decided to do it here, to prevent any errors when parsing that csv. 
    matheson_dataset = [(float(x), float(y)) for x, y in matheson_dataset]

    return matheson_dataset


# Matheson's calculated ne from the unlinked equation
# If you want the linked equation, pass True - Not put in yet 
# Pass False for unlinked equation
# Pass None for the combined equation - Not put in yet 
def calculate_matheson_data(uds, sd, linked):
    # Params: 
    # 
    # uds: an array of UDs that applies his equation to it. 
    # linked: checks if it's linked, or unlinked, or the combined. 
    #

    matheson_calculated_data = []
    
    if linked: 
        for ud in uds: 
            # This equation is incorrect, but it is obselete in my code - never used. 
            matheson_calculated_data.append((ud, np.exp(-4*ud*sd)))
    elif not linked: 
        for ud in uds: 
            matheson_calculated_data.append((ud, float(np.exp(-8 * float(ud) * float(sd)))))
    else: 
        exit 
    return matheson_calculated_data


# Calculates the BGS line for matheson's data. 
def calculate_bgs(uds, sd):
    # Params: 
    # 
    # uds: an array of UDs that applies his equation to it. 
    # linked: checks if it's linked, or unlinked, or the combined. 
    #

    matheson_calculated_data = []
    for ud in uds: 
        matheson_calculated_data.append(np.exp(-4*ud*sd))
    
    return matheson_calculated_data




def generate_ud_sd(uds, sd):
    # Returns a tuple, where the setup is (a, b)
    # a in the tuple is assigned the sd, and b in the tuple is an array, that stores the ud*sd value 
    # 
    ud_sd_array = []
    for ud in uds: 
        ud_sd_array.append(float(ud) * float(sd))
    return ud_sd_array
        
        


def get_directory(curr_dir, ud, sd, tskit, ne_status):
    if not ne_status: # We don't want to get ne
        if tskit: # Has tskit on
            if (sd == 0.005):
                filename = curr_dir + "/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
                #filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
            else: 
                filename = curr_dir + "/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
                #filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
        else: # Has tskit off
            filename = curr_dir + "-exp-reformatted-tskit/datafor_relative_tskitstatus_OFF_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
            #filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_OFF_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
    else: # We want to get Ne 
        if tskit: # Has tskit on
            if (sd == 0.005):
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "000/" 
            else: 
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/"
        else: # Has tskit off
            filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_OFF_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/"
    return filename


def get_directory_no_curr(ud, sd, tskit, ne_status):
    if not ne_status: # We don't want to get ne
        if tskit: # Has tskit on
            if (sd == 0.005):
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
            else: 
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
        else: # Has tskit off
            filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_OFF_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
    else: # We want to get Ne 
        if tskit: # Has tskit on
            if (sd == 0.005):
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "000/" 
            else: 
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/"
        else: # Has tskit off
            filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-exp-reformatted-tskit/datafor_relative_tskitstatus_OFF_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/"

    return filename 


def get_directory_exponential(ud, sd, tskit, ne_status):
    if not ne_status: # We don't want to get ne
        if tskit: # Has tskit on
            if (sd == 0.005):
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "--n2000-exp/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
            else: 
                test =     "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-0.02-exp-reformatted-tskit/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_0.1_L_200_seed_24_Sd_0.020000"
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-n2000-exp/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
        else: # Has tskit off
            filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-n2000-exp/datafor_relative_tskitstatus_OFF_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/rawdataforNxtimesteps20000popsize2000mutrate" + str(ud) + "chromsize200chromnum23benmutrate0.0000Sb1.0000.txt"
    else: # We want to get Ne 
        if tskit: # Has tskit on
            if (sd == 0.005):
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-n2000-exp/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "000/" 
            else: 
                filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-n2000-exp/datafor_relative_tskitstatus_ON_BURNIN_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/"
        else: # Has tskit off
            filename = "/Users/cameronliu/Desktop/Research/Datasets/Current/sd-" + str(sd) + "-n2000-exp/datafor_relative_tskitstatus_OFF_fixationcalc_OFF_Sb_1.0000_deldist_point_bendist_exponential_mub_0.0000_chromnum_23_N0_2000_mud_" + str(ud) + "_L_200_seed_24_Sd_" + str(sd) + "0000/"

    
    return filename




# Get ne from a singular file
def get_ne(ud, popsize, directory, sd):
    #read tables for tskit
    with open(str(directory) + 'sitetable.txt') as f:
        sites = f.read()

    with open(str(directory) + 'nodetable.txt') as f:
        nodes = f.read()

    with open(str(directory) + 'mutationtable.txt') as f:
        mutations = f.read()

    with open(str(directory) + 'edgetable.txt') as f:
        edges = f.read()

    #load in the tree sequence data
    ts = tskit.load_text(
        nodes = io.StringIO(nodes),
        edges = io.StringIO(edges),
        sites = io.StringIO(sites),
        mutations = io.StringIO(mutations),
        strict = False)

    #ts_2 = TableCollection.tree_sequence("tables.trees")

    num_samples = ts.get_sample_size()
    #print(f"the size of the sample of text-based ts is {num_samples}.")
    #num_samples = ts_2.get_sample_size()

    N = popsize

    #Calculating Average branch length between pair of sample nodes
    print(f"Calculating Coalescent Ne: {(ts.diversity(mode="branch"))/(2*N)} using sd: {sd}, ud: {ud}")
    
    return (ud, float((ts.diversity(mode="branch")/(2*N))))


# Gets all Ne's from all the files
def get_all_nes(root_dir: str, uds, sd, tskit, popsize):
    nes = []
    for ud in uds:
        directory = get_directory(dir, ud, sd, tskit, True)
        ud_val, ne = get_ne(ud, popsize, directory, sd)  # unpack here
        nes.append((sd, ud_val, ne))
    print("Calculated all Ne's for SD = " + str(sd))
    return nes


def write_all_nes(nes):
    file_name = "/Users/cameronliu/Desktop/Research/Datasets/Parsed-Nes/" + "ne_from_sd_" + str(nes[0][0]) + ".txt"
    header = True
    with open(file_name, "w") as f:
        f.write("sd, ud, ne\n")
        for sd, ud, ne in nes:
            f.write(str(float(sd)) + "," + str(float(ud)) + "," + str(float(ne)) + "\n")
        print("Successfully wrote Ne data to file ne_from_" + str(sd) + ".txt, sd = " + str(sd) + " ud = " + str(ud) + "\n")
        return True
    
    
def parse_all_nes(sd, N):
    filename = "/Users/cameronliu/Desktop/Research/Datasets/Parsed-Nes/" + "ne_from_sd_" + str(sd) + ".txt"
    data = []
    with open(filename, "r") as file:
        next(file)
        for line in file: 
            line = line.strip().split(",")
            data.append((float(sd), (float(line[1]), (float(line[2]) / N))))
            # (sd, (ud, ne))
            print(f"******************************************************************\n         Successfully parsed Ne's for SD = {sd}, UD = {float(line[1])}" + "\n******************************************************************\n")
    return data






def calculate_standard_error(dataset, size):
    # size needs to be the size of the dataset?
    standard_deviation = np.std(dataset)
    sterror = standard_deviation / size
    return sterror


# transformed_datasets.append((sd, (ud, (transformed_data, transformed_lambda))))
def calculate_all_stes(datasets, size):
    # size needs to be the size of the dataset?
    stes = []
    for (sd, (ud, (transformed_data, transformed_lambda))) in datasets: 
        # This gets the transformed data per dataset
        standard_deviation = np.std(transformed_data)
        sterror = standard_deviation / size 
        stes.append((sd, (ud, sterror)))
    return stes


def get_bounds(transformed_values, size):
    results = []
    for ((sd, (ud, (transformed_data, transformed_lamba, transformed_mean)))) in transformed_values: 
        ste = calculate_standard_error(transformed_data, size)
        upper_ste = ste + transformed_mean
        lower_ste = transformed_mean - ste
        results.append((sd, ud, transformed_mean, (lower_ste, upper_ste)))
    return results

    

def get_bounds_singular(transformed_data, transformed_mean, size):
    # Iterate through the transformed values
    ste = calculate_standard_error(transformed_data, size)

    upper_ste = ste + transformed_mean
    lower_ste = transformed_mean - ste
    
    return ste, ste
        
        






