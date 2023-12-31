'''
==============================================================================
EXAMPLE 6a: Run MOOSE in sequential then parallel mode then read sweep results

Author: Lloyd Fletcher, Rory Spencer
==============================================================================
'''
import os
from pathlib import Path
from pprint import pprint
from mooseherder import MooseHerd
from mooseherder import MooseRunner
from mooseherder import InputModifier

def main():
    print('-----------------------------------------------------------')
    print('EXAMPLE 6a: Parallel Herd Setup & Run')
    print('-----------------------------------------------------------')

    path_parts = Path(os.getcwd()).parts
    user_dir = os.path.join(path_parts[0],path_parts[1],path_parts[2])

    moose_dir = os.path.join(user_dir,'moose')
    moose_app_dir = os.path.join(user_dir,'moose-workdir/proteus')
    moose_app_name = 'proteus-opt'
    moose_input = 'scripts/moose/moose-mech-simple.i'

    moose_modifier = InputModifier(moose_input,'#','')
    moose_runner = MooseRunner(moose_dir,moose_app_dir,moose_app_name)
    
    # Start the herd and create working directories
    herd = MooseHerd(moose_runner,moose_modifier)

    # Set the parallelisation options, we have 8 combinations of variables and
    # 4 MOOSE intances running, so 2 runs will be saved in each working directory
    herd.para_opts(n_moose=4,tasks_per_moose=1,threads_per_moose=2,redirect_out=True)

     # Send all the output to the examples directory and clear out old output
    herd.set_base_dir('examples/')
    herd.clear_dirs()
    herd.create_dirs()

    # Create variables to sweep in a list of dictionaries, 8 combinations possible.
    n_elem_y = [25,50]
    e_mod = [1e9,2e9]
    p_rat = [0.3,0.35]
    moose_vars = list()
    for nn in n_elem_y:
        for ee in e_mod:
            for pp in p_rat:
                moose_vars.append({'n_elem_y':nn,'e_modulus':ee,'p_ratio':pp})
        
    print('Herd sweep variables:')
    pprint(moose_vars)

    print()
    print('Running MOOSE in parallel.')
    herd.run_para(moose_vars)

    print('Run time (parallel) = '+'{:.3f}'.format(herd.get_sweep_time())+' seconds')
    print('-----------------------------------------------------------')
    print()

    print('-----------------------------------------------------------')
    print('EXAMPLE 6a: Read Herd Output')
    print('-----------------------------------------------------------')
    output_files = herd.get_output_files()
    print('Herd output files (from output_keys.json):')
    pprint(output_files)
    print()

    vars_to_read = ['disp_x','disp_y','disp_z','strain_xx']
    elem_blocks = [0,0,0,1]

    print('Variable keys to read as list:')
    pprint(vars_to_read)
    print()

    print('Element blocks associated with variable keys as list:')
    pprint(elem_blocks)
    print()

    print('-----------------------------------------------------------')
    print('Reading the first output file, no element blocks specified.')
    print('Variables returned as dict.')
    read_vars = herd.read_results_once(output_files[0],vars_to_read)
    print()

    print('Variables read from file, time and coords are always read:')
    pprint(list(read_vars.keys()))
    print()

    print('Variable = Time (t): ', end='')
    print(type(read_vars['time']))
    print(read_vars['time'].shape)
    print()

    print('Variable = Coords, num nodes by (x,y,z): ', end='')
    print(type(read_vars['coords']))
    print(read_vars['coords'].shape)
    print()

    print('Variable = disp_x, num nodes by t: ', end='')
    print(type(read_vars['disp_x']))
    print(read_vars['disp_x'].shape)
    print()

    print('Variable = disp_z: ', end='')
    print(type(read_vars['disp_z']))
    print('NOTE: disp_z does not exist in the simulation so returns None')
    print()

    print('Variable = strain_xx: ', end='')
    print(type(read_vars['strain_xx']))
    print('NOTE: no elem block provided so strain_xx = None.')
    print()

    print('-----------------------------------------------------------')
    print('Reading the first output file, element blocks specified.')
    read_vars = herd.read_results_once(output_files[0],vars_to_read,elem_blocks)

    print('Variable = strain_xx, : ', end='')
    print(type(read_vars['strain_xx']))
    print(read_vars['strain_xx'].shape)
    print()

    print('-----------------------------------------------------------')
    print('Reading all output files sequentially as a list(dict).')
    print()
    read_all = herd.read_results_sequential(vars_to_read,None,elem_blocks)
    
    print('Number of simulations outputs: {:d}'.format(len(read_all)))
    print('Variable keys for simulation output:')
    print(list(read_all[0].keys()))
    print()

    print('-----------------------------------------------------------')
    print('Reading all output files in parallel as list(dict).')
    print()
    read_all = herd.read_results_para(vars_to_read,None,elem_blocks)

    print('Number of simulations outputs: {:d}'.format(len(read_all)))
    print('Variable keys for simulation output:')
    print(list(read_all[0].keys()))
    print()

    print('-----------------------------------------------------------')

if __name__ == '__main__':
    main()
