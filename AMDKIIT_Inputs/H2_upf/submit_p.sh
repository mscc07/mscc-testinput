#!/bin/bash -l
#SBATCH --job-name=amdkiit_h2o
#SBATCH -e ./%x.%j.err
#SBATCH -o ./%x.%j_log.o
#SBATCH --partition=hm
#SBATCH --nodes=1
#SBATCH --tasks-per-node=48
#SBATCH --time=00:15:00
#SBATCH --reservation=mscc_workshop
module load cdac/MSCC/amdkiit

INPUT=input.yaml
OUTPUT=amdkiit.out
MYNP=48
mpirun -n ${MYNP} amdkiit.x $INPUT > $OUTPUT
