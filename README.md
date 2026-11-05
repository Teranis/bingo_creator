# Bingo Sheet Generator

This project creates printable 5 × 5 bingo sheets for an epigenetics event. Each square contains a category for players to match with colleagues. A player wins by completing a row, column, or diagonal.

## Quick start

Run these commands from this project folder.

1. Install Python 3 and the two required Python packages:

   ```powershell
   python -m pip install numpy tqdm
   ```

2. Generate valid bingo grids:

   ```powershell
   python generate_grids.py
   ```

   This saves `valid_grids.npy` in the project folder. Grid generation uses random sampling and may take some time. The current settings request 1,000 grids in batches of 1,000,000 candidates. This can be skipped if you already have a suitable `valid_grids.npy` file.

3. Generate the LaTeX source for the bingo sheets:

   ```powershell
   python generate_latex.py
   ```

   This reads `valid_grids.npy` and writes `bingo_sheets.tex`.

4. Compile `bingo_sheets.tex` with a LaTeX distribution that includes Biber and the packages listed in the document preamble. For example, with `latexmk` installed:

   ```powershell
   latexmk -pdf bingo_sheets.tex
   ```

   The resulting `bingo_sheets.pdf` is ready to print. Alternatively, compile with `pdflatex`, run `biber bingo_sheets`, then run `pdflatex` twice more.

If you already have a suitable `valid_grids.npy`, you can skip step 2 and run `generate_latex.py` directly. Keep the `.npy` file in the project folder.

## How it works

### 1. Category data — `categories.py`

The file defines two lists: `epigenetics_categories` and `personal_categories`. Each entry is a `(description, rarity)` pair. Rarity is an integer from 1 to 5; it is used as the number assigned to that category when grids are checked. The two lists are combined by `generate_latex.py`.

Edit these lists to change the prompts or their rarity values. The LaTeX generator groups prompts by rarity and randomly chooses prompts to fill each grid. Make sure there are enough prompts of each rarity for the grids you intend to print.

### 2. Grid generation — `generate_grids.py`

The script builds every possible row from the configured values, keeps rows whose sums are in the allowed range, then samples grids from those rows. It accepts a grid only if every column and both diagonals also have an allowed sum. Duplicate grids are discarded, and the accepted grids are saved as `valid_grids.npy`.

The settings near the bottom of the file control the values, grid size, target sum, number of grids, and batch size. `variance` controls the permitted sum range: with a target of 13 and variance of 0, each checked row, column, and diagonal must sum to exactly 13. Increase variance to allow nearby sums. Changing the grid settings may require adjusting the values and checking that enough distinct valid grids can be generated.

### 3. LaTeX generation — `generate_latex.py`

The script groups categories by rarity, selects category descriptions to match the numbers in each saved grid, formats the cells into LaTeX tables, and adds player instructions after each sheet. It writes the resulting document to `bingo_sheets.tex`.

The settings near the top control the number of sheets, cell width, and text wrapping. The current configuration creates 85 sheets from the saved grids. The script expects `valid_grids.npy` and `dummy.bib` to be available in the project folder.

## Project files

| File or folder | Purpose |
| --- | --- |
| `categories.py` | Bingo prompts and their rarity values |
| `generate_grids.py` | Creates and saves valid numeric grids |
| `generate_latex.py` | Turns saved grids and prompts into a LaTeX document |
| `valid_grids.npy` | Generated grids used by the LaTeX generator |
| `bingo_sheets.tex` | Generated LaTeX document |
| `bingo_sheets.pdf` | Printable output (after LaTeX compilation) |
| `dummy.bib` | Bibliography file referenced by the LaTeX preamble |
| `build/` | LaTeX build files |
| `images/` | Available for images; not currently used by the scripts |
