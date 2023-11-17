import subprocess

def fetch_squeue(user=None):

    if user is None:
        print('No such user')
        exit

    cmd = ["squeue", "-u", user, "-h", "--format=%2t%100j%i"]

    try:
        result = subprocess.check_output(cmd).decode("utf-8", errors="backslashreplace")
    except subprocess.CalledProcessError:
        raise

    lines = result.split("\n")
    jobs = []
    for line in lines:
        if line:
            status = line[:2]
            name = line[2:-7].rstrip()
            jobid = line[-7:]
            jobs.append((name, jobid))
            # print(name, jobid)
    
    return jobs

def find_dependency_id(job_name, dependent_on, squeue_output):  
    '''
    get the first half of "{{ id }}"
    the job name is dependent on project.min_len_unique_id() function and may be more than 12
    ''' 
    dependent_job_name = f'Project/{job_name}/{dependent_on[:12]}'
    
    # loop through squeue_output;find dependent_job_name;get it's slurmid
    for running_job_name, running_job_slurmid in squeue_output:
        
        if dependent_job_name in running_job_name:
            
            return running_job_slurmid
