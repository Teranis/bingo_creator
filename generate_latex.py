import random
import numpy as np
import textwrap


from categories import epigenetics_categories, personal_categories
all_categories = epigenetics_categories + personal_categories

valid_grids = np.load('valid_grids.npy', allow_pickle=True)
col_width = "3cm"  # Width of each column in the LaTeX table
number_bingos = 85
width = 16  # Maximum width of each cell in characters for splitting text
target_lines= int(width /2.2)

def latex_header():
    return r"""\documentclass{article}
\usepackage[table]{xcolor}
\usepackage{array}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage[backend=biber]{biblatex}
\addbibresource{dummy.bib}
\usepackage{makecell}
\usepackage{setspace}
\setstretch{0.5} % Change this value as needed
\usepackage{lmodern}

\begin{document}
\pagenumbering{gobble}
\begin{center}
\renewcommand{\arraystretch}{1.0}
"""

def latex_footer():
    return r"""\end{center}
\printbibliography
\end{document}
"""

def split_cell_text(text, width=25):
    """
    Split text into lines of at most `width` characters, breaking at spaces.
    Returns a string with \n as line breaks for LaTeX.
    """
    # Ensure text is a string
    text = str(text)
    # Use textwrap to split at spaces
    lines = textwrap.wrap(text, width=width)
    return lines


def latex_table(content, cell_width='3cm', target_lines=target_lines):
    """
    Create a LaTeX table with horizontally centered and top-aligned text,
    fixed cell width, and balanced row heights by padding with empty lines.
    Supports multi-line cells (auto-inserts \n for long lines).
    """
    num_cols = len(content[0]) if content else 0
    col_format = "|".join([f"p{{{cell_width}}}" for _ in range(num_cols)])    
    latex = []

    latex.append("\\renewcommand{\\arraystretch}{1.0}")
    latex.append("\\begin{tabular}{" + "|" + col_format + "|}")
    latex.append("\\hline")

    for row in content:
        # Split and wrap each cell's text
        # Pad each cell with empty lines so all have the same number of lines
        padded_cells = [
            [''] + lines + [''] * (target_lines - len(lines))
            for lines in row
        ]
        # Join lines with LaTeX line breaks
        row_str = " & ".join(
            f"\\makecell[t]{{{r'\\\\'.join(lines)}}}" for lines in padded_cells
        ) + " \\\\ \\hline"
        latex.append(row_str)

    latex.append("\\end{tabular}")

    return "\n".join(latex)


def group_categories(categories):
    """
    Group categories by their values.
    """
    grouped = {}
    for category, value in categories:
        if value not in grouped:
            grouped[value] = []
        category = format_category(category)
        grouped[value].append(category)
    return grouped

def format_category(category):
    """
    Format the category string for LaTeX.
    """
    # Replace underscores with spaces and escape special characters
    category = category.replace("_", " ")
    category = category.replace("%", "\\%")
    category = category.replace("$", "\\$")
    category = category.replace("&", "\\&")
    category = category.replace("<", "\\textless ")
    category = category.replace(">", "\\textgreater ")
    category = split_cell_text(category, width=width)
    return category

def latex_other_page_content():
    """
    Generate LaTeX code for the other page content.
    """
    instructions = r"""
\end{center}

\begin{spacing}{1}
\section*{Instructions}
Each player gets a bingo sheet. The goal is to fill in a row, column or diagonal by finding colleagues 
who match the respective categories. When you find someone who matches a category, write their name in 
the corresponding cell. You will have time until 10:50.\\
If you finish early, you can talk to one of the organizers to get a new bingo sheet.\\
\end{spacing}
\begin{center}

"""

    return instructions


def latex_bingo_sheet(grid, dict_categories, col_width="2cm"):
    """
    Generate LaTeX code for a bingo card.
    """
    rareness, count = np.unique(grid, return_counts=True)

    local_categories = dict()
    for rareness, count in zip(rareness, count):
        rareness_categories = dict_categories[rareness]
        local_categories[rareness] = random.sample(rareness_categories, count) 

    rareness_counts = dict()
    grid_text = [[None for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            rareness = grid[i][j]
            if rareness not in rareness_counts:
                rareness_counts[rareness] = 0
            grid_text[i][j] = local_categories[rareness][rareness_counts[rareness]]
            rareness_counts[rareness] += 1

    table = latex_table(grid_text, cell_width =col_width)
    other_page_content = latex_other_page_content()
    latex = [table, other_page_content, r"\newpage"]
    content = "\n".join(latex)

    return content

def generate_latex_bingo_sheets(valid_grids, categories, number_bingos=5, col_width="2cm"):
    """
    Generate LaTeX code for multiple bingo sheets.
    """
    dict_categories = group_categories(categories)
    
    latex_content = latex_header()
    
    for i in range(number_bingos):
        grid = valid_grids[i]
        latex_content += latex_bingo_sheet(grid, dict_categories,col_width=col_width)
    
    latex_content += latex_footer()
    
    return latex_content

def save_latex_file(filename, content):
    """
    Save the LaTeX content to a file.
    """
    with open(filename, 'w') as f:
        f.write(content)

def main():
    latex_content = generate_latex_bingo_sheets(valid_grids, all_categories, number_bingos, col_width=col_width)
    save_latex_file('bingo_sheets.tex', latex_content)
    print("LaTeX bingo sheets generated and saved to 'bingo_sheets.tex'.")

if __name__ == "__main__":
    main()