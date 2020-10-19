#! /bin/python3

## python3 experiments.py -p ../experiments.csv -e 0 -m ../ml/clusterlenet.sh -u user -i [google_project_id] --gen

from argparse import ArgumentParser
import csv
import subprocess
import os
import sys
import time
from string import Template


dry_run = False
user = None
project_id = None
path_json_sample = 'conf.json.sample'
run_gen = True

def create_conf_json(cores, nodes, batch_size, master_ip, lbd):
    #1 driver cores
    #2 total executor cores = # of instanes * core per instance
    #3 executor cores
    #7 master ip
    #7 labmda
    total_exec_cores = str(int(nodes) * int(cores))
    content = ''
    with open(path_json_sample) as f:
        raw = f.read()
        tmpl = Template(raw)
        content = tmpl.substitute(driver=cores, total=total_exec_cores, exec=cores, batchSize=batch_size, master_ip=master_ip, lbd=lbd)

    with open('conf.json', 'w') as conf:
        conf.write(content)

    conf_path = os.path.abspath('conf.json')
    print("Will put conf.json in " + conf_path)
    return conf_path

        
        

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



def run_terraform(experiment, tf_command='apply'):
    run_env = os.environ.copy()
    cmd = ['terraform', tf_command, '-auto-approve', '-no-color']
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
    ##run script in master
    run_script_cmd = ["bash", "-x", local_path_ml_script, master_ip, batch, outfile]
    #subprocess.run(copy_cmd)
    ml_dir = os.path.dirname(local_path_ml_script)
    exec_cmd(run_script_cmd, multiplex=outfile,wd=os.path.abspath(ml_dir))

def run_ml_sparkgen(outfile, master_ip, local_path_ml_script, batch, json_conf):
    ##run script in master
    run_script_cmd = ["bash", "-x", local_path_ml_script, master_ip, batch, outfile, json_conf]
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

def run_one(exp, arguments):
    print(f'Will run experiment with setup: {exp}')
    out = run_terraform(exp)
    master_ip = get_master_ip(out)
    now = str(int(time.time()))

    ##Create conf.json
    json_conf = create_conf_json(exp['cores'], exp['nodes'], exp['batch'], master_ip, exp['lambda'])

    outfile = '-'.join([exp['JIT'], exp['nodes'], exp['cores'],exp['batch'], now]) +'.txt'
    if master_ip is None:
        print("Can not find master ip. Execute ml script manually")
        return

    if run_gen:
        print('Running ml code sparkgen')
        run_ml_sparkgen(outfile, master_ip, arguments.ml, exp['batch'], json_conf)
    else:
        print('Running ml code')
        run_ml(outfile, master_ip, arguments.ml, exp['batch'])

    print('Destroying infra')
    out = run_terraform(exp, tf_command='destroy')



if __name__ == '__main__':
    # load csv file
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-p", "--plan", required=True, help="path to the plan of experiments CSV output file")
    argument_parser.add_argument("-j", "--sample", required=False, help="path to json sample file", default='conf.json.sample')
    argument_parser.add_argument("-u", "--user", required=True, help="user")
    argument_parser.add_argument("-i", "--project-id", dest='project', required=True, help="the google project id")
    argument_parser.add_argument("-e", "--experiment", type=int, required=True, help="index of the experiment to run", default=0)
    argument_parser.add_argument("-m", "--ml", required=True, help="path to the ml script")
    argument_parser.add_argument("-d", "--dry-run", dest='dryrun', action='store_true', help="dry-run, print only do not execute")
    argument_parser.add_argument("-g", "--gen", dest='gen', action='store_true', help="Enable spark gen and run normally. This requires a change in the ml script")

    arguments = argument_parser.parse_args()
    dry_run = arguments.dryrun
    user = arguments.user
    project_id = arguments.project
    path_json_sample = arguments.sample
    run_gen = arguments.gen



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
                'lambda': l[5],
                }
        all_exp.append(exp)

    master_ip = None
    if arguments.experiment == -1:
        print('will run all experiments')
        for exp in all_exp:
            run_one(exp, arguments)
    else:
        #run a single experiment
        exp = all_exp[arguments.experiment]
        run_one(exp, arguments)




    
    
