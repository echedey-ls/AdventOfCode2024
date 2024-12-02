# %%
from pathlib import Path

THIS_FILE = Path(__file__)
THIS_DIR = THIS_FILE.parent
INPUT_FILE = THIS_DIR / "puzzle.data"
TEST_FILE = THIS_DIR / "test.data"

# %%
import numpy as np
import pandas as pd

# %%
datos = pd.read_csv(
    INPUT_FILE,
    header=None,
    sep=";",
)

# %%
col1 = datos[0].to_numpy()
col2 = datos[1].to_numpy()

# # %%
# col1_sorted = np.sort(col1)
# col2_sorted = np.sort(col2)

# # %%
# dist = np.abs(col1_sorted - col2_sorted)

# # %%
# total_dist = np.sum(dist)

# %%
# Part 2
similaridad_acumulada = 0
for num1 in col1:
    repeticiones_de_num1 = np.count_nonzero(col2 == num1)
    similaridad_acumulada += num1 * repeticiones_de_num1

# %%
