import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt


# Function to calculate the minimum number of samples required for SPR testing
def min_samples_sprt(p0, p1, alpha, beta):
    log_alpha = np.log(beta / (1 - alpha))
    log_beta = np.log((1 - beta) / alpha)
    n = 0  # Initial number of samples
    log_likelihood_ratio = 0

    # Incrementally calculate likelihood ratios until a decision threshold is met
    while True:
        n += 1
        # Calculate probability of seeing a defective part under H0 and H1
        likelihood_0 = binom.pmf(1, 1, p0)  # Probability of defective under H0
        likelihood_1 = binom.pmf(1, 1, p1)  # Probability of defective under H1
        # Update log likelihood ratio
        log_likelihood_ratio += np.log(likelihood_1 / likelihood_0)

        # Check if either decision threshold is met
        if log_likelihood_ratio >= log_beta or log_likelihood_ratio <= log_alpha:
            break

    return n


# Given values
p0 = 0.10
p1 = 0.15  # Alternative hypothesis slightly higher defect rate

# Scenario 1: Alpha = 5%, Beta = 10%
n_samples_1 = min_samples_sprt(p0, p1, alpha=0.000005, beta=0.10)

# Scenario 2: Alpha = 10%, Beta = 5%
n_samples_2 = min_samples_sprt(p0, p1, alpha=0.000010, beta=0.05)

# Print the results
print(f"Minimum samples required for scenario 1 (95% confidence): {n_samples_1}")
print(f"Minimum samples required for scenario 2 (90% confidence): {n_samples_2}")
