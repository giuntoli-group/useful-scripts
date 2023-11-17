import signac
import subprocess
from tools import fetch_squeue, find_dependency_id

def submit(eligible_jobs,squeue_output, operation=None, dependent_on=None):
    
    if dependent_on == None:
        
        for job in eligible_jobs:
            
            subprocess.run(f'python project.py submit -o {operation} -j {job.id}', shell=True)
        
    else:
        
        # submit each job individually with it's dependency 
        for job in eligible_jobs:
            
            dependency_id = find_dependency_id(job.id, dependent_on, squeue_output)
            
            # dependent job is already finished
            if dependency_id == None:
                subprocess.run(f'python project.py submit -o {operation} -j {job.id}', shell=True)
            
            else:
                subprocess.run(f'python project.py submit -o {operation} -j {job.id} -- --dependency={dependency_id}', shell=True)

        

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
