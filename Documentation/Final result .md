# Final Results 
### Analysis Flow for Fillseq

1. **Data Collection:**
   - Collected 1500 random data samples, including random knob values and their corresponding metric values for the fillseq workload.
   - Parameters:
     - `num_operation` = 100,000
     - `key_size` = 1024
     - `value_size` = 10,240

2. **Random Forest Analysis:**
   - Performed Random Forest to identify the most important features determining the metrics.

3. **ANOVA Verification:**
   - Conducted ANOVA (Analysis of Variance) to verify if the features (knobs) significantly impact the performance metric and selected those that are statistically significant.

4. **Consolidation and Optimization:**
   - Using the most significant features identified by the Random Forest model and those confirmed as statistically important through ANOVA analysis, we consolidated these into a target knob set.
   - This set was then utilized in `pipeline.py`, which executed a Bayesian optimization task focused specifically on these selected knobs.

#### Random Forest Feature Importance:
![Random Forest Feature Importance](data/FillSeq/random_forest.png)

- **Bar Chart**: Feature Importance based on operations per second
- **Most Important Knobs**: `block_size`, `write_buffer_size`, `target_file_size_base`

#### ANOVA Results:
![ANOVA Results](data/FillSeq/Anova.png)
```bash
ANOVA results for max_background_compactions: F-statistic = 0.5731525174969918, p-value = 0.7782126465151836
ANOVA results for max_background_flushes: F-statistic = 0.5154413861166572, p-value = 0.8234408859705862
ANOVA results for write_buffer_size: F-statistic = nan, p-value = nan
ANOVA results for max_write_buffer_number: F-statistic = 2.8620776676592516, p-value = 0.008968696874632177
ANOVA results for min_write_buffer_number_to_merge: F-statistic = 0.9194865901453996, p-value = 0.4516844137673135
ANOVA results for max_bytes_for_level_multiplier: F-statistic = 0.6223234670873851, p-value = 0.8483482972655091
ANOVA results for block_size: F-statistic = 1.2642248433908507, p-value = 0.40513752152271465
ANOVA results for level0_file_num_compaction_trigger: F-statistic = 1.012969018859533, p-value = 0.43714033582124334
ANOVA results for level0_slowdown_writes_trigger: F-statistic = 0.9324543907783813, p-value = 0.5718232352207571
ANOVA results for level0_stop_writes_trigger: F-statistic = 0.6750654586881485, p-value = 0.9081611802239239
ANOVA results for target_file_size_multiplier: F-statistic = 1.3482783205643796, p-value = 0.22375738172421783
ANOVA results for target_file_size_base: F-statistic = nan, p-value = nan
```
- **Bar Chart**: ANOVA p-values for the impact of each configuration parameter on `ops_per_sec`
- **Most Important Knobs**: `max_write_buffer_number` (p < 0.05)

#### Box Plots of Various Knobs:
![Box Plots of Various Knobs](data/FillSeq/Box_plot.png)
- These box plots provide a distribution analysis of `ops_per_sec` across various values of each configuration parameter, such as `max_background_compactions`, `write_buffer_size`, and others.

### Tuning for Fillseq Over Different Target Knob Sets

1. **Target Knob Set:** ['disable_auto_compactions', 'write_buffer_size', 'block_size', 'target_file_size_base', 'max_write_buffer_number']

![1717661401200](data/FillSeq/FillSeq1.png)

2. **Target Knob Set:** ['block_size', 'disable_auto_compaction', 'max_write_buffer_number']
![1717661485691](data/FillSeq/FillSeq2.png)
![1717661628672](data/FillSeq/FillSeq3.png)
3. **Target Knob Set:** ['disable_auto_compactions', 'max_write_buffer_number', 'level0_file_num_compaction_trigger']
![1717661697425](data/FillSeq/FillSeq4.png)

4. **Target Knob Set:** ['block_size', 'disable_auto_compactions', 'max_write_buffer_number', 'level0_file_num_compaction_trigger']
![1717661790685](data/FillSeq/FillSeq5.png)

---

### Analysis Flow for FillRandom

1. **Data Collection:**
   - Collected 1500 random data samples, including random knob values and their corresponding metric values for the fillrandom workload.
   - Parameters:
     - `num_operation` = 100,000
     - `key_size` = 1024
     - `value_size` = 10,240

#### Random Forest Feature Importance Results:

![1717662157800](data/FillRandom/random_forest.png)
- **Bar Chart**: Feature Importance based on operations per second
- **Most Important Knobs**: `target_file_size_base`, `block_size`, `write_buffer_size`

#### ANOVA Results:

![1717662176266](data/FillRandom/Anova.png)
```bash
ANOVA results for max_background_compactions: F-statistic = 2.51391815511479, p-value = 0.014314490900606262
ANOVA results for max_background_flushes: F-statistic = 1.3022109295682394, p-value = 0.24534973241798305
ANOVA results for write_buffer_size: F-statistic = nan, p-value = nan
ANOVA results for max_write_buffer_number: F-statistic = 0.7007886831547335, p-value = 0.6490315737504138
ANOVA results for min_write_buffer_number_to_merge: F-statistic = 0.2354960938842213, p-value = 0.9184126802077021
ANOVA results for max_bytes_for_level_multiplier: F-statistic = 1.4938739069260867, p-value = 0.10548613377840943
ANOVA results for block_size: F-statistic = 1.0380208243548275, p-value = 0.5219002872880009
ANOVA results for level0_file_num_compaction_trigger: F-statistic = 1.0047775370860152, p-value = 0.4454629211307596
ANOVA results for level0_slowdown_writes_trigger: F-statistic = 0.9524827146217583, p-value = 0.5403165078675043
ANOVA results for level0_stop_writes_trigger: F-statistic = 1.9115742501284756, p-value = 0.002213641149434112
ANOVA results for target_file_size_multiplier: F-statistic = 0.8526329567901971, p-value = 0.5436670352041957
ANOVA results for target_file_size_base: F-statistic = nan, p-value = nan
```
- **Bar Chart**: ANOVA p-values for the impact of each configuration parameter on `ops_per_sec`
- **Most Important Knobs**: `level0_stop_writes_trigger` and `max_background_compactions` (p < 0.05)

#### Configuration Recommendation:
- **Target Knob Set:** ['disable_auto_compactions', 'write_buffer_size', 'block_size', 'target_file_size_base', 'level0_stop_writes_trigger', 'max_background_compactions']

![1717662196140](data/FillRandom/Config_rec.png)

---

### Analysis Flow for ReadRandom

1. **Data Collection:**
   - Collected 1500 random data samples, including random knob values and their corresponding metric values for the readrandom workload.
   - Parameters:
     - `num_operation` = 1,000,000
     - `key_size` = 1024
     - `value_size` = 10,240

#### Random Forest Feature Importance:

![1717662287780](data/ReadRandom/random_forest.png)
- **Bar Chart**: Feature Importance based on operations per second
- **Most Important Knobs**: `target_file_size_base`, `block_size`, `write_buffer_size`

#### ANOVA Results:
![1717662348439](data/ReadRandom/Anova.png)
- **Bar Chart**: ANOVA p-values for each feature's impact on `ops_per_sec`

#### Box Plots of Various Knobs:

![1717662371265](data/ReadRandom/Box_plot.png)
- These box plots provide a distribution analysis of `ops_per_sec` across different values of each configuration parameter, such as `max_write

_buffer_number` and `block_size`.

#### Performance Trend Scatter Plot:
![1717662390252](data/ReadRandom/Performance.png)
- This scatter plot tracks the performance metric `ops_per_sec` across different rounds of configuration testing, showing a noticeable increase in performance metrics after round 70.

---

### Analysis Flow for ReadSequential

1. **Data Collection:**
   - Collected 1500 random data samples, including random knob values and their corresponding metric values for the readseq workload.
   - Parameters:
     - `num_operation` = 1,000,000
     - `key_size` = 1024
     - `value_size` = 10,240

#### Random Forest Feature Importance:

![1717662404325](data/ReadSeq/random_forest.png)
- **Bar Chart**: Feature Importance based on operations per second
- **Most Important Knobs**: `write_buffer_size`, `target_file_size_base`

#### ANOVA Results:
![1717662417199](data/ReadSeq/Anova.png)
- **Bar Chart**: ANOVA p-values for each configuration parameter's impact on `ops_per_sec`
- **Most Important Knobs**: `block_size` and `target_file_size_multiplier`

#### Configuration Recommendation:
   ![1717662430545](data/ReadSeq/Confi_rec.png)
- **Scatter Plot**: Tracks the performance metric `ops_per_sec` across different rounds of configuration testing, showing a noticeable increase in performance metrics after round 70.
