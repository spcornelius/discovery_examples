#!/bin/sh
#SBATCH -n 16
#SBATCH -t 00:15:00
#SBATCH --job-name=scoop_worker
#SBATCH --mem-per-cpu=4GB
#SBATCH -p netsi_standard
#SBATCH -o output.log
#SBATCH -e error.log

hosts=$(srun bash -c hostname)
python -m scoop --host $hosts -v calc_pi_scoop.py
