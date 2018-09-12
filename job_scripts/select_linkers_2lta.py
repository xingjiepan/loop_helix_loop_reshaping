#!/usr/bin/env python3

import os
import sys
import json

import pyrosetta
from pyrosetta import rosetta

import loop_helix_loop_reshaping as LHLR


def select_and_dump_linkers(input_pdb, input_database, output_database, linker_length, lhl_start, lhl_stop, front_linker):
    pose = rosetta.core.pose.Pose()
    rosetta.core.import_pose.pose_from_file(pose, input_pdb)

    LHLR.select_linkers.prepare_linker_selection(pose, linker_length, lhl_start, lhl_stop, front_linker)

    print('select linkers from', input_database)

    with open(input_database, 'r') as f:
        candidate_linkers = json.load(f)

    if front_linker:
        selected_linkers = LHLR.select_linkers.select_non_clashing_linkers(pose, candidate_linkers, lhl_start)
    else:
        selected_linkers = LHLR.select_linkers.select_non_clashing_linkers(pose, candidate_linkers, lhl_start + 1)
    
    with open(output_database, 'w') as f:
        json.dump(selected_linkers, f)
    
    print('dump selected linkers to', output_database)

def select_linkers_for_2lta(data_path):
    pyrosetta.init()

    input_pdb ='test_inputs/2lta_cleaned.pdb'
    lhl_start = 56
    lhl_stop = 77

    for linker_length in [2, 3, 4, 5]:

        # Select front linkers

        input_database = 'database/linker_database/linker_sheet_helix_{0}_non_redundant.json'.format(linker_length)
        output_database = os.path.join(data_path, 'selected_linkers_{0}_{1}_{2}_front.json'.format(linker_length, lhl_start, lhl_stop))
        select_and_dump_linkers(input_pdb, input_database, output_database, linker_length, lhl_start, lhl_stop, True)
        
        # Select back linkers  

        input_database = 'database/linker_database/linker_helix_sheet_{0}_non_redundant.json'.format(linker_length)
        output_database = os.path.join(data_path, 'selected_linkers_{0}_{1}_{2}_back.json'.format(linker_length, lhl_start, lhl_stop))
        select_and_dump_linkers(input_pdb, input_database, output_database, linker_length, lhl_start, lhl_stop, False)

if __name__ == '__main__':
    data_path = sys.argv[1]
    
    num_jobs = 1
    job_id = 0
    
    if len(sys.argv) > 3:
        num_jobs = int(sys.argv[2])
        job_id = int(sys.argv[3]) - 1
   
    select_linkers_for_2lta(data_path)