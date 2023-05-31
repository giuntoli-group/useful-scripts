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
    ssh -q -X nayan@mm48.phys.rug.nl "ovito sftp://nvengall@snellius.surf.nl${p}/$1"
}
```

```bash
function send_to_snellius(){
  # send files from local sys to cluster
  # call like: send_to_snellius <file-to-send> <destination>
  # default destination is home directory of the cluster
  
  rsync -rph --progress $1 nvengall@snellius.surf.nl:/home/nvengall/$2
}

```
