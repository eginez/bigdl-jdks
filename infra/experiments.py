#! /bin/python3

from argparse import ArgumentParser
import csv
import subprocess
import os

def run_terraform(experiment):
    print(f'Will run experiment with setup: {experiment}')
    run_env = os.environ.copy()
    cmd = ['terraform', 'apply', '-auto-approve']

    nodes = experiment['nodes']
    run_env['TF_VAR_num_nodes'] = nodes

    run_env['TF_VAR_jdk_version'] = '/usr/lib/jvm/java-8-openjdk-amd64/'
    if 'Graal' in experiment['JIT']:
        run_env['TF_VAR_jdk_version'] = "/usr/local/bin/graalvm-ce-java8-20.2.0/"

    cores = experiment['cores']
    ## minimum number or cores is 2
    if cores == 1:
        cores = 2

    machine_type = f'e2-highmem-{cores}'
    run_env['TF_VAR_machine_type'] = machine_type

    batch = experiment['batch']
    run_env['TF_VAR_batch_size'] = batch

    cmd_str = ' '.join(cmd)
    print(f'Will run command: {cmd_str} with env {run_env}')
    subprocess.run(cmd, env=run_env)


if __name__ == '__main__':
    # load csv file
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-p", "--plan", required=True, help="path to the plan of experiments CSV output file")
    argument_parser.add_argument("-e", "--experiment", type=int, required=True, help="index of the experiment to run", default=0)

    arguments = argument_parser.parse_args()
    csv_file = csv.reader(open(arguments.plan))
    headers = next(csv_file, None)
    all_exp = []
    for l in csv_file:
        exp = {
                'JIT': l[1],
                'nodes': l[2],
                'cores': l[3],
                'batch': l[4]
                }
        all_exp.append(exp)
    if arguments.experiment == -1:
        # run all one-by-one
        print('will run all experiments')
        pass
    else:
        #run a single experiment
        run_terraform(all_exp[arguments.experiment])



    
    
