#!/bin/bash -l
#SBATCH --job-name=amdkiit_h2o
#SBATCH -o ./%x.%j.out
#SBATCH -e ./%x.%j.err
#SBATCH --output=log.o%j
#SBATCH --partition=hm
#SBATCH --nodes=1
#SBATCH --tasks-per-node=48
#SBATCH --time=00:15:00
#SBATCH --exclusive=user
#SBATCH --reservation=mscc_workshop

module load cdac/MSCC/amdkiit

INPUT=input.yaml
OUTPUT=amdkiit.out
MYNP=48
mpirun -n ${MYNP} amdkiit.x $INPUT > $OUTPUT
