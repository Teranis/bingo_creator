from itertools import permutations, product
import numpy as np
from concurrent.futures import ThreadPoolExecutor as Executor
import tqdm
import random

def precompute_valid_rows_np(values, grid_size, ok_sums):
    # Generate all rows (might be large!)
    all_rows = np.array(list(product(values, repeat=grid_size)))
    # Filter rows by sum in ok_sums
    row_sums = np.sum(all_rows, axis=1)
    mask = np.isin(row_sums, ok_sums)
    valid_rows = all_rows[mask]
    return valid_rows

def check_grid_batch(grids, ok_sums):
    """
    grids: shape (B, N, N)
    Returns: mask of shape (B,) where True means grid is valid
    """

    # Check column sums
    col_sums = np.sum(grids, axis=1)  # shape (B, N)
    col_ok = np.all(np.isin(col_sums, ok_sums), axis=1)

    # Check main diagonal sums
    main_diag_sums = np.einsum('bii->b', grids)
    main_diag_ok = np.isin(main_diag_sums, ok_sums)

    # Check anti-diagonal sums
    flipped = np.flip(grids, axis=2)  # horizontal flip for anti-diagonal
    anti_diag_sums = np.einsum('bii->b', flipped)
    anti_diag_ok = np.isin(anti_diag_sums, ok_sums)

    # Combine all checks
    return col_ok & main_diag_ok & anti_diag_ok

def generate_unique_valid_grids(values, grid_size=5, target_sum=14, variance=0, total_grids=1000, batch_size=500):
    ok_sums = np.arange(target_sum - variance, target_sum + variance + 1)
    print(ok_sums)
    values = np.array(values)

    valid_grids = []
    seen_hashes = set()

    pbar = tqdm.tqdm(total=total_grids, desc="Valid unique grids")
    pbar2 = tqdm.tqdm(desc='Grids checked')

    valid_rows = precompute_valid_rows_np(values, grid_size, ok_sums)

    while len(valid_grids) < total_grids:
        idx = np.random.randint(0, len(valid_rows), size=(batch_size, grid_size))
        grids = valid_rows[idx]

        valid_mask = check_grid_batch(grids, ok_sums)
        valid_candidates = grids[valid_mask]
        pbar2.update(batch_size)

        for grid in valid_candidates:
            grid_hash = grid.tobytes()
            if grid_hash not in seen_hashes:
                seen_hashes.add(grid_hash)
                valid_grids.append(grid)
                pbar.update(1)
                if len(valid_grids) >= total_grids:
                    break

    return np.stack(valid_grids)



values = [1, 2, 3, 4, 5]
grid_size = 5
target_sum = 13
total_grids = 1000
batch_size=1000000

valid_grids = generate_unique_valid_grids(values, grid_size, target_sum, total_grids=total_grids, batch_size=batch_size)
np.save('valid_grids.npy', valid_grids)

for grid in valid_grids[:100]:
    print(grid)
