from controller import metric_set , knob_set , read_metric
from botorch_scratch import configuration_recommendation
from datamodel import GPDataSet
from settings import  target_knob_set, target_metric_name, wl_metrics, wltype
import numpy as np
import time
import re
import subprocess
import pickle
import inspect
import random
import rocksdb_module
import os


def calc_metric(metric_after, metric_before, metric_list):
    num_metrics = len(metric_list)
    new_metric = np.zeros([1, num_metrics])
    for i, x in enumerate(metric_list):
        if(metric_set[x]["calc"]=="inc"):
            new_metric[0][i]=metric_after[0][i]-metric_before[0][i]
        elif(metric_set[x]["calc"]=="ins"):
            new_metric[0][i]=metric_after[0][i]
    return(new_metric)


def read_knob(knob_name, knob_cache):
    return knob_cache[knob_name]

if __name__ == '__main__':

    ds = GPDataSet()
    Round = 350
    
    metric_list = wl_metrics[wltype]
    ds.initdataset(metric_list)
    num_knobs = len(target_knob_set)
    num_metrics = len(metric_list)

    KEY = str(time.time())
    while Round > 0:

        print("################## start a new Round ##################")
        
        rec = configuration_recommendation(ds)
        print("Recommendation: ", rec)

        rec_temp = {key: str(value) for key, value in rec.items()}
        knob_cache = {x: rec[x] for x in rec.keys()}
        
        print("Round: ", Round)
        db_path = "/tmp/temp_evurid_22"


        if Round > 180 : 
            no_times = 3
        else :
            no_times = 2

        for iterations in range(no_times):
            new_knob_set = np.zeros([1, num_knobs])
            new_metric_before = np.zeros([1, num_metrics])
            new_metric_after = np.zeros([1, num_metrics])

            for i, metric in enumerate(metric_list):
                # if db_bench_output exist or db_bench_outut.txt is empty then skip
                if not os.path.exists("./db_bench_output.txt") or os.stat("./db_bench_output.txt").st_size == 0:
                    print("db_bench_output.txt does not exist or is empty")
                    break
                new_metric_before[0][i] = read_metric(metric)

            for i, knob in enumerate(target_knob_set):
                new_knob_set[0][i] = read_knob(knob, knob_cache)
            # Assuming run_workload returns a result or raises an exception
            try:
                num_operations = 100000
                other_params = {}
                print("rec_temp: ", rec_temp)
                rocksdb_module.run_workload(wltype, num_operations, db_path, rec_temp,other_params)

            except Exception as e:
                print("run workload error:", e)
                break
            for i, metric in enumerate(metric_list):
                new_metric_after[0][i] = read_metric(metric)

            new_metric = calc_metric(new_metric_after, new_metric_before, metric_list)
            ds.add_new_data(new_knob_set, new_metric)

            print("new_knob_set: ", new_knob_set)
            print("new_metric: ", new_metric)

            fp = f"pkl_data/ds_{KEY}_{Round}_.pkl"
            with open(fp, "wb") as f:
                pickle.dump(ds, f)

            ds.printdata()
            ds.merge_new_data()

            Round -= 1
    
