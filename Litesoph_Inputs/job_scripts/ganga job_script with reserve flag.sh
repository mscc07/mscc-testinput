#! /bin/bash
#SBATCH -N 1
#SBATCH --ntasks-per-node=48
#SBATCH --error=job.%A_%a.err
#SBATCH --output=job.%A_%a.out
#SBATCH --time=01:00:00
#SBATCH --partition=small
#SBATCH --reservation=MSCC_Workshop1

ml MSCC/litesoph
export PYTHONPATH=$PYTHONPATH:/home/apps/MSCC/lite/litesoph/lib/python3.10/site-packages
