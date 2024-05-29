#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <rocksdb/db.h>
#include <rocksdb/slice.h>
#include <rocksdb/options.h>
#include <rocksdb/table.h>
#include <rocksdb/utilities/checkpoint.h>
#include <rocksdb/utilities/db_ttl.h>
#include <rocksdb/statistics.h>

#include <iostream>
#include <string>
// #include <bool>
#include <vector>
#include <sstream>
#include <map>
#include <cstdlib>
#include <regex>
#include <thread>
#include <chrono>

namespace py = pybind11;

const std::string rocksdb_path = "/mnt/c/Users/edeep/Final_Rocksdb/rocksdb";
void run_workload(const std::string &workload_type, int num_operations = 15000000,
                   const std::string &db_path = "/tmp/temp_db_evurid_30",
                //    all recommended knobs
                     std::map <std::string, std::string> recommendations = {},
                   const std::map<std::string, std::string> &other_params = {})
{

    std::cout << "run_workload" << std::endl;
    std::cout << "recommendations" << std::endl;
    // Paths to db_bench and output file
    std::string db_bench_path = rocksdb_path + "/db_bench";
    std::string output_file = "/mnt/c/Users/edeep/Final_Rocksdb/auto-rocksdb/run_botorch/run_botorch_change_all/recent_29_05/db_bench_output.txt";
    
    // Construct the command
    std::ostringstream cmd;

     cmd << db_bench_path << " --benchmarks=" << workload_type << " --num=" << num_operations
         << " --compression_type=none"  << " --key_size=1024 " << "--value_size=10240";
    // Add recommended parameters if provided
    for (auto &rec : recommendations)
    {
        if (rec.first == "write_buffer_size")
        {
            std::string modifiedValue = std::to_string(std::stoul(rec.second) * 1024 * 1024);
            rec.second = modifiedValue;
        }
        else if (rec.first == "block_size")
        {
            std::string modifiedValue = std::to_string(std::stoul(rec.second) );
            rec.second = modifiedValue;
        }
        else
        {
            std::string modifiedValue = std::to_string(std::stoul(rec.second));
            rec.second = modifiedValue;
        }

        
        cmd << " --" << rec.first << "=" << rec.second;
    }

    // Add other parameters if provided
    for (const auto &param : other_params)
    {
        cmd << " --" << param.first << "=" << param.second;
    }

    std::cout << "cmd: " << cmd.str() << std::endl;
    
    // Execute the db_bench command
    std::string full_cmd = cmd.str() + " > " + output_file;
    int result = std::system(full_cmd.c_str());
    std::cout << "full cmd : " <<  full_cmd << std::endl;
    if (result != 0) {
    std::cerr << "Command execution failed with return code: " << result << std::endl;
    }

    return;
}

// Wrapping your functions for Python
PYBIND11_MODULE(rocksdb_module, m)
{
    m.doc() = "pybind11 plugin for RocksDB";

    m.def(
        "run_workload", [](const std::string &workload_type, int num_operations, const std::string &db_path, std::map <std::string, std::string> recommendations , const std::map<std::string, std::string> &other_params)
        { run_workload(workload_type, num_operations, db_path,recommendations,other_params); },
        "Run a workload into RocksDB");
    

}