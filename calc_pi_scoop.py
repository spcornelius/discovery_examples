from common import run_trial
from scoop import futures
import argh
import numpy as np


def calc_pi1(num_trials, pts_per_trial):
    F = [futures.submit(run_trial, pts_per_trial) for _ in range(num_trials)]
    areas = [f.result() for f in F]
    return 4 * np.mean(areas)


def calc_pi2(num_trials, pts_per_trial):
    areas = futures.map(run_trial, [pts_per_trial] * num_trials)
    return 4 * np.mean(areas)


def main(num_trials=10**4, pts_per_trial=10**6):
    print("Using futures.submit:")
    print("pi ~= ", calc_pi1(num_trials, pts_per_trial))
    print()

    print("Using futures.map:")
    print("pi ~= ", calc_pi2(num_trials, pts_per_trial))


if __name__ == "__main__":
    argh.dispatch_command(main)
