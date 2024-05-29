# workloads and their related performance metrics
rocksdb_path="/mnt/c/Users/edeep/Final_Rocksdb/rocksdb"
wl_metrics={
    # "writeheavy":["ops_per_sec"]
    "fillseq":["ops_per_sec","micros_per_op" ],
    "fillrandom":["ops_per_sec","micros_per_op" ],  
    "readseq":["ops_per_sec","micros_per_op"  ],
    "readrandom":["ops_per_sec","micros_per_op" ]
}


# workload to be run
# wltype = "fillseq"
# wltype = "fillrandom"
# wltype = "readrandom"
wltype = "readseq"


# only 1 target metric to be optimized
# target metric to be optimized
target_metric_name="ops_per_sec"
# target_metric_name="micros_per_op"

# several knobs to be tuned

# target_knob_set=['disable_auto_compactions', 'target_file_size_base', 'block_size', 'write_buffer_size' , 'max_write_buffer_number'] # fillseq
target_knob_set=['disable_auto_compactions', 'target_file_size_base', 'block_size', 'write_buffer_size' , 'level0_stop_writes_trigger' , 'max_background_compactions'] # fillrandom
# target_knob_set=['disable_auto_compactions', 'target_file_size_base', 'block_size', 'write_buffer_size'] # readrandom
# target_knob_set=['disable_auto_compactions', 'target_file_size_base', 'block_size', 'write_buffer_size'] # readseq

