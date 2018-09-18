# loop_helix_loop_reshaping
Reshape a part of the protein into a loop-helix-loop unit

## Installation
I recommand to create a python virtual environment before installing the package.
```
virtualenv -p /usr/bin/python3 --system-site-packages venv
```
Activate the virtual environment and install the package by
```
pip install -e .
```

## Running An Example
This is an example that remodels two loop-helix-loop units in the `test_inputs/2lv8_cleaned.pdb` structure. The insertion points for the LHL units are defined in the file `test_inputs/2lv8_insertion_points.json`. 

### Select linker loops
The first step is selecting linker loops that do not clash with the scaffold.
```
./run_jobs.py test_select_linkers job_scripts/select_linkers_example.py
```
This command will create the directory `data/test_select_linkers` and dump 16 json libraries for selected linker loops at different positions.

### Screen loop helix loop units
The second step is screening LHL units that at each insertion points individually. At each insertion point, pairs of linker loops will be inserted and a helix will be introduced to bridge the gap. The built LHL unit will be filtered by the quality of the gap closure, the helix-scaffold contact and the number of buried unsatisfied H-bonds.
```
./run_jobs.py test_screen_single_insertion_loop_helix_loop_units job_scripts/screen_single_insertion_loop_helix_loop_units_example.py
```
The command will create the directory `data/test_screen_single_insertion_loop_helix_loop_units` and dump 2 json libraries for LHL units at the two insertion points.

### Screen compatible loop helix loop units
The last step is to get combinations of LHL units that don't clash against each other.
```
./run_jobs.py test_screen_compatible_loop_helix_loop_units job_scripts/screen_compatible_loop_helix_loop_units_example.py
```
The command will create the directory `data/test_screen_compatible_loop_helix_loop_units` and dump the selected models. For each model, a pdb file of its structure and a json file of its insertion points will be made.

## Production Run
Now that you know how to run the example, let's see how to do a production run for a real problem, which often produce tens of thousands of structures. First you need to prepare a pdb file for the scaffold and a json file for the insertion points. I recommand to create a directory under the `data` directory to store your inputs. Then you need to customize the job scripts. Copy the example scripts to the `job_scripts/user` directory and edit them for inputs and options. Run a job script by
```
./run_jobs.py my_output_data_set job_scripts/user/my_script.py
```
The two LHL screening steps are usually too computationaly expensive to ran on a single computer. You'd better use a cluster. To submit a job to the UCSF QB3 cluster. Just do
```
./run_jobs.py my_output_data_set job_scripts/user/my_script.py -d SGE -n 100
```
This command will use 100 CPUs to run the job.
