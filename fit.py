"""
Take the intensity ratios over mixing times from an EXSY 
experiment and fit to extract rate constants.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
import argparse
import os

def calc_iratio(t_m, k_12, k_21):
    """
    Fitting to equation 3 in SI: 
    https://pubs.acs.org/doi/abs/10.1021/acs.jpclett.9b00052

    Parameters
    ----------
    t_m : array_like
        Mixing times (ms).
    k_12 : float
        Forward exchange rate (s⁻¹).
    k_21 : float
        Reverse exchange rate (s⁻¹).
    """
    return ((1 - np.exp(-(k_12 + k_21) * t_m)) * k_12) / \
           (k_21 + k_12 * np.exp(-(k_12 + k_21) * t_m))

def calc_rates(times, ratios):
    """
    Fit the intensity ratios to extract exchange rates k_12 and k_21.

    Parameters
    ----------
    times : array_like
        Mixing times (ms).
    ratios : array_like
        Intensity ratios (I12/I11).

    Returns
    -------
    param : array_like
        Fitted parameters [k_12, k_21].
    p_sigma : array_like
        Standard deviations of the fitted parameters.
    Kex : float
        Exchange ratio k_12/k_21.
    K_error : float
        Error in the exchange ratio.
    """
    param, param_cov = scipy.optimize.curve_fit(calc_iratio, times, ratios)
    # diagonal of cov matrix is the variance per parameter
    # sqrt of the variance is the stdev
    p_sigma = np.sqrt(np.diag(param_cov))

     # s^-1 to ms^-1
    k12 = param[0] * 1000 
    k21 = param[1] * 1000
    k12_err = p_sigma[0] * 1000
    k21_err = p_sigma[1] * 1000

    # exchange ratio
    Kex = param[0] / param[1]
    # propagate the error from division of rates
    # for z = x/y: ∆z/z = sqrt( (∆x/x)^2 + (∆y/y)^2 + ... ) | solving for ∆z
    K_error = Kex * np.sqrt((p_sigma[0]/param[0])**2 + (p_sigma[1]/param[1])**2)

    print(f"k_12 = {k12:.3f} ± {k12_err:.3f} ms⁻¹")
    print(f"k_21 = {k21:.3f} ± {k21_err:.3f} ms⁻¹")
    print(f"K_ex = {Kex:.3f} ± {K_error:.3f}")

    return param, p_sigma, Kex, K_error

def plot_fit(times, ratios, yerr, fit_params, output_prefix):
    """
    Plot the fitted curve along with the raw data.

    Parameters
    ----------
    times : array_like
        Mixing times (ms).
    ratios : array_like
        Intensity ratios (I12/I11).
    yerr : array_like
        Errors in intensity ratios.
    fit_params : array_like
        Fitted parameters [k_12, k_21].
    output_prefix : str
        Prefix for output PDF file.
    """
    fig, ax = plt.subplots()

    # Plot raw data
    ax.errorbar(times, ratios, yerr=yerr, fmt="o", capsize=3, capthick=2)

    # Plot fitted curve
    x_fit = np.linspace(0, max(times)*1.1, 500)
    y_fit = calc_iratio(x_fit, *fit_params)
    ax.plot(x_fit, y_fit, "--", color="tab:blue")

    ax.set(xlabel="t(m): Mixing Time (ms)", ylabel="I$_{12}$/I$_{11}$")
    fig.tight_layout()

    # Save PDF only
    pdf_file = f"{output_prefix}_fit.pdf"
    fig.savefig(pdf_file)
    print(f"Saved plot to: {pdf_file}")
    plt.show()

def load_data(input_file):
    data = np.loadtxt(input_file)
    times = data[:, 0]
    ratios = data[:, 1]
    if data.shape[1] > 2:
        errors = data[:, 2]
    else:
        errors = np.zeros_like(ratios)
    return times, ratios, errors

def main():
    parser = argparse.ArgumentParser(description="Fit EXSY intensity ratios to extract exchange rates.")
    parser.add_argument("input", help="Text file with columns: mixing_time(ms) I12/I11 [I12/I11_err]")
    parser.add_argument("-o", "--output", default="exsy", help="Prefix for output PDF file")
    parser.add_argument("--style", help="Matplotlib .mplstyle file to use for plotting")

    args = parser.parse_args()

    if args.style:
        if os.path.exists(args.style):
            plt.style.use(args.style)

    if not os.path.exists(args.input):
        print(f"Error: File '{args.input}' not found.")
        return

    times, ratios, errors = load_data(args.input)
    fit_params, fit_errors, Kex, Kex_err = calc_rates(times, ratios)
    output_prefix = os.path.splitext(args.output)[0]
    plot_fit(times, ratios, errors, fit_params, output_prefix)

if __name__ == "__main__":
    main()

