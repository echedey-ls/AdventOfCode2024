# %%
import numpy as np
import pandas as pd

from pathlib import Path

TEST_FILE = Path(__file__).parent / "test.data"
INPUT_FILE = Path(__file__).parent / "puzzle.data"


# %%
def monotonic_increase(arr):
    return np.all(arr[1:] > arr[:-1])


def monotonic_decrease(arr):
    return np.all(arr[1:] < arr[:-1])


def unsafe_increments(arr):
    return np.any(np.abs(arr[1:] - arr[:-1]) > 3)


# %%
# read data
data = pd.read_csv(
    INPUT_FILE,
    header=None,
    sep=" ",
)


# %%
# Part 1
def filter(arr):
    # remove NaNs from arr
    arr = arr[~np.isnan(arr)]
    is_ok = (
        monotonic_increase(arr) or monotonic_decrease(arr)
    ) and not unsafe_increments(arr)
    return is_ok


data_safe = data.apply(filter, axis=1, raw=True)
print(np.sum(data_safe))


# %%
# Part 2
def problem_dampener_monotonic_assumption(arr):
    # remove NaNs from arr
    diffs = arr[1:] - arr[:-1]
    diffs_clip = np.sign(diffs)
    common_sign = np.sign(np.sum(diffs_clip))
    
    if diffs_clip[0] != common_sign:
        if monotonic_decrease(arr[1:]) or monotonic_increase(arr[1:]):
            new_arr = arr[1:]
        else:
            new_arr = np.concatenate(([arr[0]], arr[2:]))
    elif diffs_clip[-1] != common_sign:
        if monotonic_decrease(arr[:-1]) or monotonic_increase(arr[:-1]):
            new_arr = arr[:-1]
        else:
            new_arr = np.concatenate((arr[:-2], [arr[-1]]))
    else:
        new_arr = arr[np.append(diffs_clip, False) == common_sign]
    return new_arr


def problem_dampener_unsafe_increments(arr):
    # remove NaNs from arr
    diffs = arr[1:] - arr[:-1]
    big_diffs = np.abs(diffs) > 3
    if np.count_nonzero(big_diffs == True) > 1:
        new_arr = arr
    else:
        if big_diffs[0]:
            if not unsafe_increments(arr[1:]):
                new_arr = arr[1:]
            else:
                new_arr = arr[~big_diffs]
        elif big_diffs[-1]:
            if not unsafe_increments(arr[:-1]):
                new_arr = arr[:-1]
            else:
                new_arr = arr[~big_diffs]
        else:
            big_diffs = np.append(big_diffs, False)
            new_arr = arr[~big_diffs]
    return new_arr


def filter2(arr):
    # remove NaNs from arr
    arr = arr[~np.isnan(arr)]
    is_monotonic = monotonic_increase(arr) or monotonic_decrease(arr)
    if not is_monotonic:
        arr = problem_dampener_monotonic_assumption(arr)
    if unsafe_increments(arr):
        arr = problem_dampener_unsafe_increments(arr)
    return filter(arr)


# %%
# test cases
data = pd.read_csv(
    TEST_FILE,
    header=None,
    sep=" ",
)

data_safe = data.apply(filter2, axis=1, raw=True)
print(np.sum(data_safe))

# %%
# edge cases
data = pd.DataFrame(
    [
        # [1, 2, 3, 4, 5, 6],
        # [1, 2, 3, 4, 5, 5],
        # [1, 1, 3, 4, 5, 6],
        # [1, 2, 3, 3, 5, 6],
        # [6, 5, 4, 3, 2, 1],
        # [6, 5, 4, 3, 2, 2],
        # [6, 6, 4, 3, 2, 1],
        # [6, 5, 4, 4, 2, 1],
        # [1, 5, 6, 7, 8, 9],
        # [1, 5, 6, 7, 8, 8],
        # [1, 5, 5, 7, 8, 9],
        # [1, 5, 6, 6, 8, 9],
        # [9, 8, 7, 6, 5, 1],
        # [9, 8, 7, 6, 5, 5],
        # [9, 9, 7, 6, 5, 1],
        # [9, 8, 7, 7, 5, 1],
        # [1, 5, 4, 7, 8, 9],
        # [1, 4, 3, 6, 8, 9],
        # [1, 4, 3, 6, 8, 8],
        # [1, 5, 6, 6, 8, 9],
        # [10, 9, 4, 7],
        # [10, 4, 2, 1],
        # [7, 6, 5, 1],
        # [14, 15, 20, 18, 19, 22],
        # [80, 77, 60, 76, 75],
        # [1, 4, 3, 2, 1],
        [1, 2, 3, 4, 1],
    ]
)


data_safe = data.apply(filter2, axis=1, raw=True)
print(np.sum(data_safe))

# %%
# real data
data = pd.read_csv(
    INPUT_FILE,
    header=None,
    sep=" ",
)

data_safe = data.apply(filter2, axis=1, raw=True)
print(np.sum(data_safe))


# %%
# Desperation, lets try brute force
def filter3(arr):
    res = filter(arr)
    if not res:
        for i in range(len(arr)):
            if filter(np.concatenate((arr[:i], arr[i+1:]))):
                return True
    return res


# %%
# real data
data = pd.read_csv(
    INPUT_FILE,
    header=None,
    sep=" ",
)

data_safe = data.apply(filter3, axis=1, raw=True)
print(np.sum(data_safe))
# %%
