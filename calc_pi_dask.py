from common import run_trial
from dask_jobqueue import SLURMCluster
from dask.distributed import Client
import argh
import numpy as np


def calc_pi1(client, num_trials, pts_per_trial):
    # NOTE: CRITICAL to use pure=False for any stochastic task; dask is
    # lazy by default, and will not redo an execution of the same function
    # on the same arguments (it caches the result)
    F = [client.submit(run_trial, pts_per_trial, pure=False) for _ in range(num_trials)]
    areas = client.gather(F)
    return 4 * np.mean(areas)


def calc_pi2(client, num_trials, pts_per_trial):
    # see above about pure=False
    F = client.map(run_trial, [pts_per_trial] * num_trials, pure=False)
    areas = client.gather(F)
    return 4 * np.mean(areas)


def main(num_trials=10**4, pts_per_trial=10**6, num_cores=32):
    # context mgrs, so resources are released even if things go awry
    with SLURMCluster(processes=4, cores=4,
                      walltime="00:05:00", queue="netsi_standard",
                      memory='4GB') as cluster:
        # not sure if this try block is necessary, but the finally
        # seems to resolve some weird race conditions that create either
        # "zombie" jobs or prematurely closed tcp connections between
        # scheduler/workers
        try:
            with Client(cluster) as client:
                # request num_cores total cores from SLURM
                cluster.scale(num_cores)
                print("Using client.submit:")
                print("pi ~= ", calc_pi1(client, num_trials, pts_per_trial))
                print()

                print("Using client.map:")
                print("pi ~= ", calc_pi2(client, num_trials, pts_per_trial))
        finally:
            cluster.scale(0)


if __name__ == "__main__":
    argh.dispatch_command(main)
