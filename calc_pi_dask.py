from math import hypot
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
from numpy.random import rand, seed
import argh


def run_trial(pts_per_trial):
    # return fraction random pts in the unit square that also fall within
    # the quarter-unit-circle that square encloses
    seed()
    return sum(hypot(rand(), rand()) < 1 for _ in range(pts_per_trial)) / pts_per_trial


def calc_pi1(num_trials, pts_per_trial, num_workers):
    # using futures.submit
    with SLURMCluster(queue='netsi_standard', processes=1, cores=1,
                      walltime='00:15:00', memory='4GB') as cluster:
        cluster.scale(num_workers)
        with Client(cluster) as client:
            F = [client.submit(run_trial, pts_per_trial) for _ in range(num_trials)]
            areas = [f.result() for f in F]
            return 4 * sum(areas) / num_trials


def calc_pi2(num_trials, pts_per_trial, num_workers):
    # using futures.map
    with SLURMCluster(queue='netsi_standard', processes=1, cores=1,
                      walltime='00:15:00', memory='4GB') as cluster:
        cluster.scale(num_workers)
        with Client(cluster) as client:
            F = client.map(run_trial, [pts_per_trial] * num_trials)
            areas = client.gather(F)
            return 4 * sum(areas) / num_trials


def main(num_trials=10**4, pts_per_trial=10**5, num_workers=16):
    print("Using client.submit:")
    print("pi ~= ", calc_pi1(num_trials, pts_per_trial, num_workers))
    print()

    print("Using client.map:")
    print("pi ~= ", calc_pi2(num_trials, pts_per_trial, num_workers))


if __name__ == "__main__":
    argh.dispatch_command(main)
