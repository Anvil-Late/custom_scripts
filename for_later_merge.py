#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:53:40 2022

@author: antoinevillatte
"""
import numpy as np
import pandas as pd

def get_modality_proportions(sample):
    unique_values, value_counts = np.unique(sample, return_counts=True)
    sample_report = {
        value: value_count for value, value_count in zip(
            np.unique(sample, return_counts=True)[0], 
            np.unique(sample, return_counts=True)[1] / sample.shape[0]
        )
    }
    return sample_report

def generate_random_sample_reports(loops, goldensource, indicator, sample_size=2000):
    initial_report={modality : [] for modality in goldensource[indicator].unique()}
    i=0
    while i < loops:
        # Select random sample
        random_sample = np.random.choice(goldensource[indicator], size=sample_size, replace=False)
        sample_report = get_modality_proportions(random_sample)
        for key in sample_report.keys():
            initial_report[key].append(sample_report[key])
        i+=1
        
    return initial_report

def generate_statistical_report(random_sample_reports):
    statistical_report = {}
    for modality, modality_proportions in random_sample_reports.items():
        statistical_report[modality] = {
            "mean" : np.mean(modality_proportions),
            "std" : np.std(modality_proportions)
        }
    
    return statistical_report

def get_population_groups(goldensource, low_cutoff=0.4, high_cutoff=0.6):
    gs_no_outliers = goldensource[~goldensource["OUTLIER"]]
    loyals = gs_no_outliers[
        (gs_no_outliers["LIFETIME"].ge(gs_no_outliers["LIFETIME"].quantile(high_cutoff)))
        & (gs_no_outliers["BC_CLI"].ge(gs_no_outliers["BC_CLI"].quantile(high_cutoff)))
    ]
    aliens = gs_no_outliers[
        (gs_no_outliers["LIFETIME"].le(gs_no_outliers["LIFETIME"].quantile(low_cutoff)))
        & (gs_no_outliers["BC_CLI"].le(gs_no_outliers["BC_CLI"].quantile(low_cutoff)))
    ]
    butterflies = gs_no_outliers[
        (gs_no_outliers["LIFETIME"].le(gs_no_outliers["LIFETIME"].quantile(low_cutoff)))
        & (gs_no_outliers["BC_CLI"].ge(gs_no_outliers["BC_CLI"].quantile(high_cutoff)))
    ]
    crustaceans = gs_no_outliers[
        (gs_no_outliers["LIFETIME"].ge(gs_no_outliers["LIFETIME"].quantile(high_cutoff)))
        & (gs_no_outliers["BC_CLI"].le(gs_no_outliers["BC_CLI"].quantile(low_cutoff)))
    ]
    
    population_groups = {
        "loyals": loyals,
        "aliens": aliens,
        "butterflies": butterflies,
        "crustaceans": crustaceans
    }
    
    return population_groups

def get_population_group_reports(population_groups, statistical_report, indicator):
    general_modality_conformity = {}
    for group_name, group in population_groups.items():
        group_modality_sample = group[indicator]
        modality_conformity = {}
        for modality, modality_proportion in get_modality_proportions(group_modality_sample).items():
            lower_bound = statistical_report[modality]["mean"] - 3*statistical_report[modality]["std"]
            upper_bound = statistical_report[modality]["mean"] + 3*statistical_report[modality]["std"]
            modality_conformity[modality] = False \
            if lower_bound <= modality_proportion <= upper_bound else True
        
        general_modality_conformity[group_name] = modality_conformity
    
    general_modality_conformity_df = pd.DataFrame.from_dict(
        general_modality_conformity, 
        orient="index"
    )
    general_modality_conformity_df.columns = [
        "ABNORMAL_" + modality + "_DISTRIB" for modality in general_modality_conformity_df.columns
    ]
    return general_modality_conformity_df

def analyze_subgroups(
    goldensource,
    indicator,  
    random_loops=1000,
    random_sample_size=2000
):
    
    modality_report = generate_random_sample_reports(
        loops=random_loops,
        goldensource=goldensource,
        indicator=indicator,
        sample_size=random_sample_size
    )
    statistical_report = generate_statistical_report(
        modality_report
    )
    population_groups = get_population_groups(
        goldensource=goldensource
    )
    subgroup_analysis_report = get_population_group_reports(
        population_groups=population_groups,
        statistical_report = statistical_report,
        indicator=indicator
    )

    return subgroup_analysis_report