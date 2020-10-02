#! /bin/python3

from argparse import ArgumentParser
import csv
import subprocess

def run_terraform(experiment):
    print(f'Will run experiment with setup: {experiment}')
    cmd = ['terraform', 'apply']
    nodes = experiment['nodes']
    cmd.append(f'-var="num_nodes={nodes}"')
    if 'Graal' in experiment['JIT']:
        cmd.append(f'-var="jdk_version=/usr/local/bin/graalvm-ce-java8-20.2.0/"')
    else:
        cmd.append(f'-var="jdk_version=/usr/lib/jvm/java-8-openjdk-amd64/')

    cores = experiment['cores']
    machine_type = f'e2-highmem-{cores}'
    cmd.append(f'-var="machine_type={machine_type}"')
    batch = experiment['batch']
    cmd.append(f'-var="batch_size={batch}"')

    print(f'Will run command: {cmd}')


if __name__ == '__main__':
    # load csv file
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-p", "--plan", required=True, help="path to the plan of experiments CSV output file")
    argument_parser.add_argument("-e", "--experiment", type=int, required=True, help="experiment number 1-indexed", default=0)

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
    if arguments.experiment == 0:
        # run all one-by-one
        print('will run all experiments')
        pass
    else:
        run_terraform(all_exp[arguments.experiment - 1])
        #run a single experiment



    
    
