#!/bin/bash -l
#SBATCH --job-name=amdkiit_h2o
#SBATCH -o ./%x.%j.out
#SBATCH -e ./%x.%j.err
#SBATCH --output=log.o%j
#SBATCH --partition=standard
#SBATCH --nodes=2
#SBATCH --tasks-per-node=48
#SBATCH --time=00:15:00
#SBATCH --exclusive=user
#SBATCH --reservation=mscc_workshop

export OMPI_MCA_mtl=psm2
module load cdac/MSCC/amdkiit

INPUT=input.yaml
OUTPUT=amdkiit13.out
MYNP=48

echo " 2 nodes"

time mpirun -n 96 --npernode 48 amdkiit.x $INPUT > $OUTPUT
