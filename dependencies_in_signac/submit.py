import signac
import subprocess
from tools import fetch_squeue, construct_dependency_string

def submit(eligible_jobs,squeue_output, operation=None, dependent_on=None):
    
    operation_string = f'python project.py submit -o {operation}'
    
    # swap template if postprocessing; must define a template first
    template_string = ' --template postprocess.sh' if operation == 'postprocess' else ''

    # submit each job individually with it's dependency
    for job in eligible_jobs:
        
        job_string = f' -j {job.id}'
        dependency_string = construct_dependency_string(job, dependent_on, squeue_output)
        total_string = operation_string + job_string + template_string + dependency_string
       
        subprocess.run(total_string, shell=True)

project = signac.get_project()
eligible_jobs = project.find_jobs()

serial_operations_list = ['operation1','operation2','operation3']

for i in range(len(serial_operations_list)):

    # get currently running jobs from slurm
    squeue_output = fetch_squeue(user='<user-name>')

    # 1st operation in the serial_operations_list don't have any dependencies
    if i == 0:
        submit(eligible_jobs,
                squeue_output,
                operation = serial_operations_list[i],
                dependent_on = None)
    
    # each operation is dependent on the previous one
    else:
        submit(eligible_jobs,
                squeue_output,
                operation = serial_operations_list[i],
                dependent_on = serial_operations_list[i-1])
