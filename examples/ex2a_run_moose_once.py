"""
==============================================================================
EXAMPLE 2a: Run MOOSE using mooseherder once

Author: Lloyd Fletcher
==============================================================================
"""
import time
import os
from pathlib import Path
from mooseherder import MooseRunner

def main():
    path_parts = Path(os.getcwd()).parts
    user_dir = os.path.join(path_parts[0],path_parts[1],path_parts[2])

    print('------------------------------------------')
    print('EXAMPLE 2a: Run MOOSE once')
    print('------------------------------------------')
    # Create the moose runner with correct paths to moose and apps
    moose_dir = os.path.join(user_dir,'moose')
    moose_app_dir = os.path.join(user_dir,'moose-workdir/proteus')
    moose_app_name = 'proteus-opt'
    moose_runner = MooseRunner(moose_dir,moose_app_dir,moose_app_name)

    print('MOOSE directory:' + moose_dir)
    print('MOOSE app directory: ' + moose_app_dir)
    print('MOOSE app name: ' + moose_app_name)
    print()

    # Set input and parallelisation options
    moose_runner.set_opts(n_tasks=2,n_threads=4,redirect=False)
    input_file = 'scripts/moose/moose-mech-simple.i'
    moose_runner.set_input_file(input_file)

    # Run the MOOSE!
    print('Running moose with:')
    print(moose_runner.get_run_str())

    start_time = time.perf_counter()
    moose_runner.run()
    end_time = time.perf_counter()

    print()
    print('MOOSE run time = '+'{:.3f}'.format(end_time-start_time)+' seconds')
    print('------------------------------------------')
    print()

if __name__ == '__main__':
    main()

