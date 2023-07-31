#!/bin/bash

########################################
# Create slurm job submission scripts with different number of cores and submit the jobs
########################################

# run very short simulations using 'c' number of cores
for c in 10 20 30 40 50
do

# replace the variables with their values and 
# write the lines between two FLAGs to the submit_cores_${c}.sh file
cat > submit_cores_${c}.sh <<FLAG
#!/bin/bash
#SBATCH --job-name=CORES_${c}
#SBATCH --time=01:00:00
#SBATCH --partition=parallelshort
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=${c}

cores=${c}
FLAG

# keep the 'variable-looking' words as is and 
# write the lines between two FLAGs to the submit_cores_${c}.sh file
cat >> submit_cores_${c}.sh <<'FLAG'
module load LAMMPS/23Jun2022-foss-2021b-kokkos
srun --ntasks=${cores} --exclusive lmp -l log_${cores} -screen out.txt -in run.in
FLAG

# Make the script executable
chmod +x submit_cores_${c}.sh 

# submit the batch jobs
sbatch submit_cores_${c}.sh
done
