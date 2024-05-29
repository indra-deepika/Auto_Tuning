import re
from settings import rocksdb_path


def read_metric(req_metric_name, file_path = './db_bench_output.txt'):
    metrics = {}
    micros_op_pattern = re.compile(r"(\d+\.\d+) micros/op (\d+) ops/sec")
    write_read_rate_pattern = re.compile(r"Write rate: (\d+) bytes/second\nRead rate: (\d+) ops/second")
    with open(file_path, 'r') as file:
        file_content = file.read()
        
        micros_op_match = micros_op_pattern.search(file_content)
        if micros_op_match:
            metrics['micros_per_op'] = float(micros_op_match.group(1))
            metrics['ops_per_sec'] = int(micros_op_match.group(2))
            

        write_read_rate_match = write_read_rate_pattern.search(file_content)
        if write_read_rate_match:
            metrics['write_rate'] = int(write_read_rate_match.group(1))
            metrics['read_rate'] = int(write_read_rate_match.group(2))


    
    file_path = rocksdb_path + "/node_exporter-1.7.0.linux-amd64/custom_metrics.prom"
    try:
        with open(file_path, "w") as outfile:
            # Write to the file
            outfile.write("# Custom metric for ops_per_sec\n")
            outfile.write("rocksdb_ops_per_sec " + str(metrics['ops_per_sec']) + "\n")
            outfile.write("# Custom metric for write_rate\n")
            outfile.write("rocksdb_write_rate " + str(metrics['write_rate']) + "\n")
            outfile.write("# Custom metric for read_rate\n")
            outfile.write("rocksdb_read_rate " + str(metrics['read_rate']) + "\n")
            outfile.write("# Custom metric for micros_per_op\n")
            outfile.write("rocksdb_micros_per_op " + str(metrics['micros_per_op']) + "\n")
    except IOError:
        print("Error opening or writing to the file")
    return metrics[req_metric_name]
def read_ops_per_sec():
    return read_metric("ops_per_sec")

def read_micros_per_op():
    return read_metric("micros_per_op")

metric_set=\
    {
        "ops_per_sec":
        {
         "read_func": read_ops_per_sec,        #function to read the metric
         "lessisbetter": 0,                   # whether less value of this metric is better(1: yes)
         "calc": "ins",                       #incremental
        },

        "micros_per_op":
        {
         "read_func": read_micros_per_op,        #function to read the metric
         "lessisbetter": 1,                   # whether less value of this metric is better(1: yes)
         "calc": "ins",                       #incremental
        },
        
    }

knob_set = {

    "write_buffer_size": {
        "changebyyml": True,
        "set_func": None,
        "minval": 64,
        "maxval": 1024,
        "enumval": [],
        "type": "int",
        "default": 64
    },
    "max_bytes_for_level_base":
        {
            "changebyyml": True,
            "set_func": None,
            "minval": 512,                          # if type==int, indicate min possible value
            "maxval": 4096,                         # if type==int, indicate max possible value
            "enumval": [],                          # if type==enum, list all valid values
            "type": "int",                          # int / enum
            "default": 512                            # default value
        },

    "block_size" :{
        "changebyyml": True,
        "set_func": None,
        "minval": 4,                            # if type==int, indicate min possible value
        "maxval": 64,                            # if type==int, indicate max possible value
        "enumval": [4*1024, 8*1024, 16*1024, 32*1024, 64*1024 , 128*1024],          # if type==enum, list all valid values
        "type": "enum",                         # int / enum
        "default": 0                            # default value
    },
    "disable_auto_compactions" :{

        "changebyyml": True,
        "set_func": None,
        "minval": 0,                            # if type==int, indicate min possible value
        "maxval": 1,                            # if type==int, indicate max possible value
        "enumval": [1 , 0],  #true , false        # if type==enum, list all valid values
        "type": "bool",                         # int / enum
        "default": 0                            # default value
    },
    "max_write_buffer_number" :{
        "changebyyml": True,
        "set_func": None,
        "minval": 0,                            # if type==int, indicate min possible value
        "maxval": 1,                            # if type==int, indicate max possible value
        "enumval": [2 , 3 ,4 , 5 ,6 ,7 ,8 ],  #true , false        # if type==enum, list all valid values
        "type": "enum",                         # int / enum
        "default": 0                            # default value

    },
    "level0_file_num_compaction_trigger" :{
        "changebyyml": True,
        "set_func": None,
        "minval": 0,                            # if type==int, indicate min possible value
        "maxval": 1,                            # if type==int, indicate max possible value
        "enumval": [2 , 3 ,4 , 5 ,6 ,7 ,8 , 9 ,10 ,11 ,12 ,13 ,14 ,15 , 16 ],  #true , false        # if type==enum, list all valid values
        "type": "enum",                         # int / enum
        "default": 0                            # default value

    },
    "target_file_size_base" : {
        "changebyyml": True,
        "set_func": None,
        "minval": 33554432,
        "maxval": 134217728,
        "enumval": [],
        "type": "int",
        "default": 33554432

    },
    "max_bytes_for_level_multiplier" :{
            "changebyyml": True,
            "set_func": None,
            "minval": 0,                            # if type==int, indicate min possible value
            "maxval": 0,                            # if type==int, indicate max possible value
            "enumval":  [2 , 3 ,4 , 5 ,6 ,7 ,8 , 9 ,10 ,11 ,12 ,13 ,14 ,15 , 16 ],                # if type==enum, list all valid values
            "type": "enum",                         # int / enum
            "default": 0                            # default value
    },
    'level0_stop_writes_trigger': {
        "changebyyml": True,
        "set_func": None,
        "minval": 1,                            # if type==int, indicate min possible value
        "maxval": 2**10,                            # if type==int, indicate max possible value
        "enumval":  [],                # if type==enum, list all valid values
        "type": "int",                  # int / enum
        "default": 0  

    },
        'max_background_compactions': {
        "changebyyml": True,
        "set_func": None,
        "minval": 1,                            # if type==int, indicate min possible value
        "maxval": 2**8,                            # if type==int, indicate max possible value
        "enumval":  [],                # if type==enum, list all valid values
        "type": "int",                  # int / enum
        "default": 0  

    },
    "bloom_filter_bits_per_key" :{
            "changebyyml": True,
            "set_func": None,
            "minval": 0,                            # if type==int, indicate min possible value
            "maxval": 0,                            # if type==int, indicate max possible value
            "enumval": [5,10,15,20],                # if type==enum, list all valid values
            "type": "enum",                         # int / enum
            "default": 0                            # default value
    },
}