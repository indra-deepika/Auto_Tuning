# Code Documentation 

## rocksdb_module.cpp
This file creates a Python module using `pybind11` that interfaces with RocksDB to execute database workloads. The main function, `run_workload`, configures and runs a specified workload on a RocksDB instance, allowing for custom database path and tuning parameters. This module enables Python scripts to manage RocksDB operations like benchmarks and performance tuning directly through Python calls.

## settings.py
This file includes the following:
`rocksdb_path` : The location of rocksdb.
`wl_metrics` : A dictionary of workloads and and their coresponding metrics.
`wltype` : Defines the workload type.
`target_metric_name` : Target metric to be optimised.
`target_knob_set` : A collection of configuration parameters.

## setup.py
This `setup.py` script is used for building a Python module that provides bindings for RocksDB functionalities using Pybind11. It defines a Python extension module named rocksdb_module, compiled from the source file rocksdb_module.cpp. The script configures the necessary library and include directories for both RocksDB and Pybind11, ensuring that the Python module links correctly to the RocksDB library installed at the specified path. The setup script also specifies metadata such as the module name, version, and author, and utilizes the build_ext command class from Pybind11 to handle the build process. This enables the Python module to interact with RocksDB through native C++ code.

## botorch_scratch.py
This code employs Gaussian Processes (GP) from the BoTorch library, to model the relationship between configuration settings, referred to as "knobs," and performance metrics. Here’s an overview of the script’s functionalities and workflow:

### Key Functionalities:

1. **Random Data Generation (`gen_random_data` function):**
   - This function generates random configurations for each knob based on its type, such as boolean, integer, or real. This method is particularly useful during the early stages of the tuning process when sufficient historical data is not yet available.

2. **Configuration Recommendation (`configuration_recommendation` function):**
   - This function provides configuration recommendations by utilizing both past and newly acquired data about knob settings and their corresponding performance metrics. It facilitates configuration recommendations during initial stages with fewer than 70 samples by providing random configurations. For later stages, it optimizes configurations using a Gaussian Process model.

### Detailed Workflow:

1. **Data Preparation:**
   - The script combines historical and new knob settings and their corresponding metrics. It applies one-hot encoding to categorical variables and scales all features and target metrics using MinMax scaling to prepare data for modeling.

2. **Model Training:**
   - A Gaussian Process (SingleTaskGP) is used to model the relationship between configurations and a weighted sum of the metrics. The weights and transformations of the metrics are adjusted based on whether higher or lower values are preferable, indicated by the "lessisbetter" attribute.

3. **Optimization:**
   - The script uses the Upper Confidence Bound (UCB) acquisition function to identify knob settings that are expected to optimize the performance metrics. The acquisition function is optimized to recommend new knob settings that could potentially improve system performance.

4. **Post-Processing:**
   - The recommended settings are inverse transformed from their scaled values to their original scale. For categorical variables, the script converts them back from their one-hot encoded form to their original categorical values based on the highest likelihood.

## pipeline.py

The is the main code where the pipeline to automatically tune database configurations to optimize performance metrics starts. It iterates through multiple tuning rounds, adjusting database knobs settings that potentially improve performance, measuring the impact of these settings by running predefined workloads.


### Key Components:
1. **Data Preparation and Initialization**:
   - `GPDataSet`: A custom dataset class that stores configuration settings and their corresponding performance metrics.
   - `metric_list`: Specifies the metrics to be collected and analyzed, derived from predefined workload metrics.
   - `knob_cache`: A cache that stores the current values of the knobs which are being tuned.

2. **Configuration Recommendation**:
   - `configuration_recommendation()`: A function that utilizes Gaussian Processes to predict and recommend knob settings that are likely to optimize the specified target metric. This function is a core component where the GP model integration occurs.

3. **Experimental Execution Loop**:
   - Runs multiple rounds of experiments where each round potentially adjusts the database's configuration based on the recommendations from the GP model.
   - The script dynamically adjusts the number of times a workload is run (`no_times`) based on the progress of the tuning rounds.

4. **Metric Calculation and Data Collection**:
   - `calc_metric()`: Calculates new metrics based on the differences observed before and after applying the recommended settings.
   - Each new configuration's impact is recorded by comparing metrics before and after workload execution.

5. **Workload Execution**:
   - `rocksdb_module.run_workload()`: Executes the workload with the current recommended settings. The workload type and other parameters are specified dynamically.

6. **Data Persistence and Analysis**:
   - Results from each round are serialized and saved as `.pkl` files for persistence and further analysis.
   - The script also prints data to provide a real-time overview of the tuning process.

### Detailed Workflow:
- **Initialization**: Set up the dataset and determine the metrics and knobs to be monitored.
- **Tuning Rounds**: For each round until the specified number of rounds is completed:
  - Get knob recommendations from the GP model.
  - Apply these knobs and run the specified workload multiple times.
  - Collect and calculate performance metrics.
  - Save the results and prepare for the next round.
- **Feedback Loop**: After each round, update the GP model with new data to refine future recommendations.

## datamodel.py
This file contains the class `GPDataSet` which serves as a structured data storage for a Gaussian Process-based tuning system. This class is specifically designed to handle and organize data related to database tuning tasks, including the recording of configuration settings (knobs) and their corresponding performance outcomes (metrics).

## updated_controller.py
This file consists of read metric function that is designed to extract specific performance metrics from a db_bench_output.txt file, which contains database performance data for RocksDB. The function uses regular expressions to parse metrics such as operations per second and microseconds per operation from the file. It also formats and writes these metrics to a custom Prometheus-compatible file, enabling integration with monitoring systems for real-time performance tracking.

# References
- BoTorch : https://botorch.org/docs/introduction
- AutoTiKV : https://github.com/tikv/auto-tikv
