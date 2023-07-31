#!/bin/bash

############################
# get the performance data from lammps log file
# Must make sure all the jobs are finished before running this
############################


echo "mpi_tasks   timesteps/s" >> performance.txt
for c in 10 20 30 40 50
do
  timesteps=$(cat log_${c} | grep -oE ' [0-9.]+ timesteps/s' | grep -oE '[0-9.]+')
  mpi_tasks=$(cat log_${c} | grep -oE ' [0-9.]+ MPI tasks' | grep -oE '[0-9.]+')
  echo "${mpi_tasks}    ${timesteps}" >> performance.txt
done
