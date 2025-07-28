# EAXY

Easy EXSY analysis

## Overview

`eaxy` is a simple tool for analyzing EXSY (Exchange Spectroscopy) NMR data. It fits intensity ratios over mixing times from an EXSY experiment to extract exchange rate constants, following the equation described in [J. Phys. Chem. Lett. 2019, 10, 7, 1514–1519](https://pubs.acs.org/doi/abs/10.1021/acs.jpclett.9b00052).

## Features

- Fits intensity ratios (I12/I11) vs. mixing time to extract forward and reverse exchange rates (`k_12`, `k_21`)
- Calculates the exchange ratio (`K_ex = k_12 / k_21`) and its error
- Plots the data and fitted curve
- Supports error bars in input data
- Customizable matplotlib style

## Requirements and installation

- Python 3
- numpy
- matplotlib
- scipy

To install `eaxy`, start from the command line; first clone this repository and move into the cloned repo:
```sh
git clone https://github.com/darianyang/eaxy.git
cd eaxy
```

Assuming that you have Python already installed, you can then install `eaxy` and its dependencies directly with `pip`:
```sh
pip install .
```

All done! Now you can use the `eaxy` command within the Python env that you just installed into.

You can test that things are working by running the following from within the `eaxy` directory that you just changed into.
```sh
eaxy iratios.txt --style eaxy.mplstyle -o test_plot.pdf
```

## Usage

First, prepare a text file (e.g., `iratios.txt`) with mixing times and intensity ratios, you can use `#` to denote headers and columns should be separated by tabs or commas or spaces:

```
# mixing_time(ms)    I12/I11    [I12/I11_err]
2    0.0747429207    0.0070743411
5    0.2342992127    0.0105126053
10   0.3756389618    0.0141767065
15   0.4150403440    0.0141054088
25   0.4408375025    0.0131581232
35   0.4425624013    0.0141708783
50   0.4392259419    0.0159461681
75   0.4361551702    0.0134360635
100  0.4391582906    0.0139806627
200  0.4413508475    0.0151571719
```

Note that if you don't have errors that's okay, it should still run and will use no error bars in that case.

You can run eaxy from the command line after installation by using the `eaxy` command with the path to your text file of intensity ratios and mixing times:
```sh
eaxy iratios.txt
```

## More usage options

To see available arguments:
```sh
eaxy -h
```

Optional arguments:
- `-o`, `--output`: Prefix for output PDF file (default: `exsy`)
- `--style`: Path to a matplotlib `.mplstyle` file for custom plotting

Example with a custom style file (see `eaxy.mplstyle`) which you can edit to change plot specifications:

```sh
eaxy iratios.txt --style eaxy.mplstyle
```

There are also pre-included matplotlib style options that you can use, see [here](https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html) for a full list.

For example:
```sh
eaxy iratios.txt --style ggplot
```

## Output

- Prints fitted rate constants and exchange ratio with errors
- Saves a PDF plot of the data and fit (e.g., `fit.pdf`)

To update the name of the output pdf file:
```sh
eaxy iratios.txt -o output_file_name
```
