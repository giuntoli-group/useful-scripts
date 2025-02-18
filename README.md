## Build a Slurm pipeline

Split a long simulation into smaller parts and run them one after the other in Slurm.

```bash
#!/bin/bash

# submit the first job without any dependency
id=$( sbatch submit.sh)

# submit 10 successive jobs each starting after the previous one ends/timeouts.
for i in {1..10}
do
  id=$( sbatch --dependency=afterany:${id##* } submit.sh )
done
```


## .bashrc functions and aliases
```bash
# show currect queue
alias q='squeue --format="%.18i %.20E %.9P %.25j %.8u %.2t %.9M %.6D  %R"  -u <username>'

# show details of a job
alias job='scontrol show jobid -dd '

# show a continuously updating queue
alias w='watch -n1 -x squeue --format="%.18i %.9P %.25j %.2t %.9M  %.18R %.20e %.70Z" -u <username>'
```
```bash
convert_restart(){
  # convert restart file to data file
  # call like: convert_restart <restart-file> <data-file>
  
  lmp -restart2data $1 $2
}
```

```bash
view(){
  # view data file from cluster without explicit download
  # call like: view <data-file>
    p=${PWD}
    ssh -q -X <username>@mm48.phys.rug.nl "ovito sftp://<username>@snellius.surf.nl${p}/$1"
}
```

```bash
function send_to_snellius(){
  # send files from local sys to cluster
  # call like: send_to_snellius <file-to-send> <destination>
  # default destination is home directory of the cluster
  
  rsync -rph --progress $1 nvengall@snellius.surf.nl:/home/<username>/$2
}
```
## High resolution rendering using Ovito

There are three rendering engines in Ovito. Only the basic one is available in the free version.
However, you can access the other two renderers using an old version of Ovito. Steps to do that are
as follows:

* Download Ovito-2.9.0 version named _ovito-2.9.0-x86_64.tar.xz_ from the [Ovito downloads page](https://www.ovito.org/download-other/) or from [this](https://www.ericnhahn.com/tutorials/ovito) alternate link.
* Extract the tar file using `tar -xvf ovito-2.9.0-x86_64.tar.xz`
* Load a file to Ovito and switch renderer to either Tachyon renderer or POV-Ray renderer
* Increasing the height and width of the render will increase the quality as well!

## Chain Signac operations

Run another signac operation once the current one is finished. This can be useful to
automate postprocessing operations after the simulation is complete. This is done using
[hooks](https://docs.signac.io/en/latest/hooks.html) from Signac

```python
import subprocess

def submit_next_operation(operation_name, job):
  command = ['python', 'project.py', 'submit', '-o', 'run2', '-j', f'{job.id}']
  subprocess.check_call(command)

@Project.operation
@Project.operation_hooks.on_success(submit_next_operation)
def run1(job):
  pass

@Project.operation
def run2(job):
  pass
```
