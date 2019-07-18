import numpy as np

__all__ = ['run_trial']


def run_trial(pts_per_trial):
    # return fraction random pts in the unit square that also fall within
    # the inscribed quarter of the unit-circle that square encloses
    return np.mean(np.hypot(*np.random.uniform(size=(2, pts_per_trial))) < 1)
