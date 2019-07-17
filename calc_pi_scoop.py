from math import hypot
from scoop import futures
from numpy.random import rand, seed
import argh


def run_trial(pts_per_trial):
    # return fraction random pts in the unit square that also fall within
    # the quarter-unit-circle that square encloses
    seed()
    return sum(hypot(rand(), rand()) < 1 for _ in range(pts_per_trial)) / pts_per_trial


def calc_pi1(num_trials, pts_per_trial):
    # using futures.submit
    F = [futures.submit(run_trial, pts_per_trial) for _ in range(num_trials)]
    areas = [f.result() for f in F]
    return 4 * sum(areas) / num_trials


def calc_pi2(num_trials, pts_per_trial):
    # using futures.map
    areas = futures.map(run_trial, [pts_per_trial] * num_trials)
    return 4 * sum(areas) / num_trials


def main(num_trials=10**4, pts_per_trial=10**5):
    print("Using futures.submit:")
    print("pi ~= ", calc_pi1(num_trials, pts_per_trial))
    print()

    print("Using futures.map:")
    print("pi ~= ", calc_pi2(num_trials, pts_per_trial))


if __name__ == "__main__":
    argh.dispatch_command(main)
