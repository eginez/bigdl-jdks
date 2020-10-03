#! /bin/python3

from argparse import ArgumentParser
import csv
import subprocess
import os
import sys
import time


dry_run = False
user = None
project_id = None

def exec_cmd(cmd, env=os.environ.copy(), multiplex=None, wd=os.path.abspath('.')):
    cmd_str = ' '.join(cmd)
    output = []
    outf = None
    if multiplex is not None:
        print(f"Will save output to  {multiplex}")
        outf = open(multiplex, 'w')

    if dry_run:
        print(f'Will run command: {cmd_str} with env {env}')
        return None
    else:
        #print(f'Executing command: {cmd_str} with env {env}')
        print(f'Executing command: {cmd_str}')
        process = subprocess.Popen(cmd, env=env,stdout=subprocess.PIPE,universal_newlines=True, cwd=wd)
        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(line)
            output.append(line)
            if outf is not None:
                outf.write(line)

    if outf is not None:
        outf.close()
    return output



def run_terraform(experiment):
    print(f'Will run experiment with setup: {experiment}')
    run_env = os.environ.copy()
    cmd = ['terraform', 'apply', '-auto-approve', '-no-color']
    run_env['TF_VAR_user'] = user
    run_env['TF_VAR_project_id'] = project_id

    nodes = experiment['nodes']
    run_env['TF_VAR_num_nodes'] = nodes

    run_env['TF_VAR_jdk_version'] = '/usr/lib/jvm/java-8-openjdk-amd64/'
    if 'Graal' in experiment['JIT']:
        run_env['TF_VAR_jdk_version'] = "/usr/local/bin/graalvm-ce-java8-20.2.0/"

    cores = experiment['cores']
    ## minimum number or cores is 2
    if int(cores) == 1:
        print("WARNING resetting cores to 2, cores can not be 1")
        cores = "2"

    machine_type = f'e2-highmem-{cores}'
    run_env['TF_VAR_machine_type'] = machine_type

    batch = experiment['batch']
    run_env['TF_VAR_batch_size'] = batch

    return exec_cmd(cmd, run_env)

def run_ml(outfile, master_ip, local_path_ml_script, batch):
    #remote_ml_dir = '/tmp/ml_scripts'
    ##create a dir in well know location in master
    #cmd_create_dir = ['ssh', master_ip, 'mkdir', '-p', remote_ml_dir]

    #exec_cmd(cmd_create_dir)
    ##subprocess.run(cmd_create_dir)

    ##copy ml_script to to 
    #copy_cmd = ['scp',local_path_ml_script, f"{master_ip}:{remote_ml_dir}"]
    ##subprocess.run(copy_cmd)
    #exec_cmd(copy_cmd)

    #script_name=os.path.basename(local_path_ml_script)
    ##run script in master
    run_script_cmd = ["bash", "-x", local_path_ml_script, master_ip, batch]
    #subprocess.run(copy_cmd)
    ml_dir = os.path.dirname(local_path_ml_script)
    exec_cmd(run_script_cmd, multiplex=outfile,wd=os.path.abspath(ml_dir))

def get_master_ip(out):
    for line in out:
        sys.stdout.write(line)
        if 'ip_master_internal' in line:
            parts = line.split('=')
            print(f"Found {parts[1]}")
            return parts[1].strip()
    return None



if __name__ == '__main__':
    # load csv file
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-p", "--plan", required=True, help="path to the plan of experiments CSV output file")
    argument_parser.add_argument("-u", "--user", required=True, help="user")
    argument_parser.add_argument("-i", "--project-id", dest='project', required=True, help="the google project id")
    argument_parser.add_argument("-e", "--experiment", type=int, required=True, help="index of the experiment to run", default=0)
    argument_parser.add_argument("-m", "--ml", required=True, help="path to the ml script")
    argument_parser.add_argument("-d", "--dry-run", dest='dryrun', action='store_true', help="dry-run, print only do not execute")

    arguments = argument_parser.parse_args()
    dry_run = arguments.dryrun
    user = arguments.user
    project_id = arguments.project

    #p = exec_cmd(['ls' , '-larth'], multiplex='out.txt')
    #get_master_ip(p)
    #exit(0)

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

    master_ip = None
    if arguments.experiment == -1:
        # run all one-by-one
        print('will run all experiments')
        pass
    else:
        #run a single experiment
        exp = all_exp[arguments.experiment]
        out = run_terraform(exp)
        master_ip = get_master_ip(out)
        now = str(int(time.time()))
        outfile = '-'.join([exp['JIT'], exp['nodes'], exp['cores'],exp['batch'], now]) +'.txt'
        if master_ip is None:
            print("Can not find master ip. Execute ml script manually")
            exit(0)
        run_ml(outfile, master_ip, arguments.ml, exp['batch'])




    
    
