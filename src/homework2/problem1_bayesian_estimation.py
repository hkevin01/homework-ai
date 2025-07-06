"""
Problem 1: Bayesian Parameter Estimation

This problem focuses on implementing Bayesian parameter estimation for a simple model.
We'll estimate the parameters of a normal distribution given observed data.

Learning Objectives:
- Understand prior and posterior distributions
- Implement Bayesian parameter updates
- Visualize uncertainty in parameter estimates
- Compare Bayesian vs. frequentist approaches
"""

from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


class BayesianNormalEstimator:
    """Bayesian estimator for normal distribution parameters."""
    
    def __init__(self, prior_mu: float = 0.0, prior_sigma: float = 1.0,
                 prior_alpha: float = 1.0, prior_beta: float = 1.0):
        """
        Initialize with priors for mean and precision.
        
        Args:
            prior_mu: Prior mean for the mean parameter
            prior_sigma: Prior standard deviation for the mean parameter
            prior_alpha: Shape parameter for precision prior (Gamma distribution)
            prior_beta: Rate parameter for precision prior (Gamma distribution)
        """
        self.prior_mu = prior_mu
        self.prior_sigma = prior_sigma
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        
        # Posterior parameters (updated with data)
        self.posterior_mu = prior_mu
        self.posterior_sigma = prior_sigma
        self.posterior_alpha = prior_alpha
        self.posterior_beta = prior_beta
        
        self.data = []
    
    def update_posterior(self, data: np.ndarray) -> None:
        """Update posterior distributions given observed data."""
        self.data = data
        n = len(data)
        sample_mean = np.mean(data)
        sample_var = np.var(data, ddof=1) if n > 1 else 0
        
        # Update posterior parameters for normal-gamma conjugate prior
        prior_precision = 1 / (self.prior_sigma ** 2)
        
        # Posterior for mean (normal distribution)
        posterior_precision = prior_precision + n / sample_var if sample_var > 0 else prior_precision
        self.posterior_sigma = 1 / np.sqrt(posterior_precision)
        self.posterior_mu = (prior_precision * self.prior_mu + n * sample_mean / sample_var) / posterior_precision if sample_var > 0 else self.prior_mu
        
        # Posterior for precision (gamma distribution)
        self.posterior_alpha = self.prior_alpha + n / 2
        if n > 1:
            ss = np.sum((data - sample_mean) ** 2)
            self.posterior_beta = self.prior_beta + ss / 2 + (prior_precision * n * (sample_mean - self.prior_mu) ** 2) / (2 * posterior_precision)
        else:
            self.posterior_beta = self.prior_beta
    
    def sample_posterior(self, n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Sample from the posterior distributions."""
        # Sample precision from gamma distribution
        precision_samples = np.random.gamma(self.posterior_alpha, 1/self.posterior_beta, n_samples)
        
        # Sample mean from normal distribution (conditional on precision)
        sigma_samples = 1 / np.sqrt(precision_samples)
        mu_samples = np.random.normal(self.posterior_mu, self.posterior_sigma, n_samples)
        
        return mu_samples, sigma_samples
    
    def posterior_predictive(self, x_new: np.ndarray) -> np.ndarray:
        """Compute posterior predictive distribution for new data points."""
        # For normal-gamma posterior, predictive is Student's t
        nu = 2 * self.posterior_alpha
        scale = np.sqrt(self.posterior_beta * (1 + 1) / self.posterior_alpha)
        
        return stats.t.pdf(x_new, nu, loc=self.posterior_mu, scale=scale)


def demonstrate_bayesian_estimation():
    """Demonstrate Bayesian parameter estimation with visualization."""
    print("🔬 Bayesian Parameter Estimation Demonstration")
    print("=" * 50)
    
    # Generate synthetic data
    true_mu = 2.5
    true_sigma = 1.2
    n_data_points = 20
    
    np.random.seed(42)  # For reproducibility
    observed_data = np.random.normal(true_mu, true_sigma, n_data_points)
    
    print(f"True parameters: μ = {true_mu}, σ = {true_sigma}")
    print(f"Generated {n_data_points} data points")
    print(f"Sample mean: {np.mean(observed_data):.3f}")
    print(f"Sample std: {np.std(observed_data, ddof=1):.3f}")
    
    # Create Bayesian estimator
    estimator = BayesianNormalEstimator(
        prior_mu=0.0,      # Neutral prior on mean
        prior_sigma=2.0,   # Somewhat broad prior
        prior_alpha=1.0,   # Weak prior on precision
        prior_beta=1.0
    )
    
    # Update with data
    estimator.update_posterior(observed_data)
    
    print(f"\nPosterior parameters:")
    print(f"Posterior μ: {estimator.posterior_mu:.3f} ± {estimator.posterior_sigma:.3f}")
    print(f"Posterior precision shape: {estimator.posterior_alpha:.3f}")
    print(f"Posterior precision rate: {estimator.posterior_beta:.3f}")
    
    # Sample from posterior
    mu_samples, sigma_samples = estimator.sample_posterior(5000)
    
    print(f"\nPosterior sample statistics:")
    print(f"Mean estimate: {np.mean(mu_samples):.3f} ± {np.std(mu_samples):.3f}")
    print(f"Sigma estimate: {np.mean(sigma_samples):.3f} ± {np.std(sigma_samples):.3f}")
    
    # Create visualizations
    create_bayesian_plots(estimator, observed_data, mu_samples, sigma_samples, true_mu, true_sigma)
    
    # Compare with frequentist approach
    compare_approaches(observed_data, mu_samples, sigma_samples, true_mu, true_sigma)


def create_bayesian_plots(estimator, data, mu_samples, sigma_samples, true_mu, true_sigma):
    """Create comprehensive plots for Bayesian analysis."""
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Bayesian Parameter Estimation Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Data histogram with true and estimated distributions
    ax1 = axes[0, 0]
    ax1.hist(data, bins=12, density=True, alpha=0.7, color='lightblue', label='Observed Data')
    
    x_range = np.linspace(data.min() - 1, data.max() + 1, 100)
    
    # True distribution
    true_pdf = stats.norm.pdf(x_range, true_mu, true_sigma)
    ax1.plot(x_range, true_pdf, 'r-', linewidth=2, label=f'True: N({true_mu}, {true_sigma:.1f}²)')
    
    # Posterior mean estimate
    post_mean_mu = np.mean(mu_samples)
    post_mean_sigma = np.mean(sigma_samples)
    est_pdf = stats.norm.pdf(x_range, post_mean_mu, post_mean_sigma)
    ax1.plot(x_range, est_pdf, 'g--', linewidth=2, label=f'Estimated: N({post_mean_mu:.2f}, {post_mean_sigma:.2f}²)')
    
    ax1.set_xlabel('Value')
    ax1.set_ylabel('Density')
    ax1.set_title('Data vs. Estimated Distribution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Posterior distribution of mean
    ax2 = axes[0, 1]
    ax2.hist(mu_samples, bins=50, density=True, alpha=0.7, color='orange', label='Posterior μ')
    ax2.axvline(true_mu, color='red', linestyle='--', linewidth=2, label=f'True μ = {true_mu}')
    ax2.axvline(np.mean(mu_samples), color='green', linestyle='-', linewidth=2, 
                label=f'Posterior mean = {np.mean(mu_samples):.3f}')
    ax2.set_xlabel('μ (Mean)')
    ax2.set_ylabel('Density')
    ax2.set_title('Posterior Distribution of Mean')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Posterior distribution of sigma
    ax3 = axes[0, 2]
    ax3.hist(sigma_samples, bins=50, density=True, alpha=0.7, color='purple', label='Posterior σ')
    ax3.axvline(true_sigma, color='red', linestyle='--', linewidth=2, label=f'True σ = {true_sigma}')
    ax3.axvline(np.mean(sigma_samples), color='green', linestyle='-', linewidth=2, 
                label=f'Posterior mean = {np.mean(sigma_samples):.3f}')
    ax3.set_xlabel('σ (Standard Deviation)')
    ax3.set_ylabel('Density')
    ax3.set_title('Posterior Distribution of Std Dev')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Joint posterior (scatter plot)
    ax4 = axes[1, 0]
    scatter = ax4.scatter(mu_samples[::10], sigma_samples[::10], alpha=0.3, c='blue', s=1)
    ax4.scatter(true_mu, true_sigma, color='red', s=100, marker='x', linewidth=3, label='True parameters')
    ax4.scatter(np.mean(mu_samples), np.mean(sigma_samples), color='green', s=100, marker='+', 
                linewidth=3, label='Posterior mean')
    ax4.set_xlabel('μ (Mean)')
    ax4.set_ylabel('σ (Standard Deviation)')
    ax4.set_title('Joint Posterior Distribution')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Plot 5: Posterior predictive distribution
    ax5 = axes[1, 1]
    x_pred = np.linspace(data.min() - 2, data.max() + 2, 100)
    
    # Sample multiple predictive distributions
    n_pred_samples = 100
    pred_samples = []
    for i in range(0, len(mu_samples), len(mu_samples)//n_pred_samples):
        pred_dist = stats.norm.pdf(x_pred, mu_samples[i], sigma_samples[i])
        pred_samples.append(pred_dist)
        if i < 10:  # Show first few
            ax5.plot(x_pred, pred_dist, 'gray', alpha=0.1)
    
    # Mean predictive
    mean_pred = np.mean(pred_samples, axis=0)
    ax5.plot(x_pred, mean_pred, 'blue', linewidth=2, label='Mean Predictive')
    
    # True distribution
    true_pred = stats.norm.pdf(x_pred, true_mu, true_sigma)
    ax5.plot(x_pred, true_pred, 'red', linewidth=2, label='True Distribution')
    
    ax5.hist(data, bins=12, density=True, alpha=0.3, color='lightblue', label='Data')
    ax5.set_xlabel('Value')
    ax5.set_ylabel('Density')
    ax5.set_title('Posterior Predictive Distribution')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # Plot 6: Credible intervals
    ax6 = axes[1, 2]
    
    # Calculate credible intervals
    mu_ci = np.percentile(mu_samples, [2.5, 50, 97.5])
    sigma_ci = np.percentile(sigma_samples, [2.5, 50, 97.5])
    
    # Plot credible intervals
    categories = ['Mean (μ)', 'Std Dev (σ)']
    true_values = [true_mu, true_sigma]
    medians = [mu_ci[1], sigma_ci[1]]
    lower_bounds = [mu_ci[0], sigma_ci[0]]
    upper_bounds = [mu_ci[2], sigma_ci[2]]
    
    x_pos = np.arange(len(categories))
    ax6.errorbar(x_pos, medians, 
                yerr=[np.array(medians) - np.array(lower_bounds), 
                      np.array(upper_bounds) - np.array(medians)],
                fmt='go', capsize=5, capthick=2, label='95% Credible Interval')
    ax6.scatter(x_pos, true_values, color='red', s=100, marker='x', 
                linewidth=3, label='True Values')
    
    ax6.set_xticks(x_pos)
    ax6.set_xticklabels(categories)
    ax6.set_ylabel('Parameter Value')
    ax6.set_title('95% Credible Intervals')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def compare_approaches(data, mu_samples, sigma_samples, true_mu, true_sigma):
    """Compare Bayesian vs. frequentist approaches."""
    print("\n📊 Comparison: Bayesian vs. Frequentist")
    print("=" * 45)
    
    # Frequentist estimates
    freq_mu = np.mean(data)
    freq_sigma = np.std(data, ddof=1)
    n = len(data)
    
    # Frequentist confidence intervals (assuming normal distribution)
    mu_se = freq_sigma / np.sqrt(n)
    mu_ci_freq = [freq_mu - 1.96 * mu_se, freq_mu + 1.96 * mu_se]
    
    # Bayesian estimates
    bayes_mu = np.mean(mu_samples)
    bayes_sigma = np.mean(sigma_samples)
    mu_ci_bayes = np.percentile(mu_samples, [2.5, 97.5])
    sigma_ci_bayes = np.percentile(sigma_samples, [2.5, 97.5])
    
    print(f"{'Parameter':<12} {'True':<8} {'Frequentist':<12} {'Bayesian':<12}")
    print("-" * 45)
    print(f"{'Mean':<12} {true_mu:<8.3f} {freq_mu:<12.3f} {bayes_mu:<12.3f}")
    print(f"{'Std Dev':<12} {true_sigma:<8.3f} {freq_sigma:<12.3f} {bayes_sigma:<12.3f}")
    
    print(f"\n95% Intervals for Mean:")
    print(f"Frequentist CI: [{mu_ci_freq[0]:.3f}, {mu_ci_freq[1]:.3f}]")
    print(f"Bayesian CI:    [{mu_ci_bayes[0]:.3f}, {mu_ci_bayes[1]:.3f}]")
    print(f"Contains true value: Freq={mu_ci_freq[0] <= true_mu <= mu_ci_freq[1]}, "
          f"Bayes={mu_ci_bayes[0] <= true_mu <= mu_ci_bayes[1]}")
    
    print(f"\n95% Credible Interval for Std Dev:")
    print(f"Bayesian CI: [{sigma_ci_bayes[0]:.3f}, {sigma_ci_bayes[1]:.3f}]")
    print(f"Contains true value: {sigma_ci_bayes[0] <= true_sigma <= sigma_ci_bayes[1]}")


if __name__ == "__main__":
    print("🎯 Starting Problem 1: Bayesian Parameter Estimation")
    print("This problem demonstrates Bayesian inference for parameter estimation")
    print()
    
    try:
        demonstrate_bayesian_estimation()
        print("\n✅ Problem 1 completed successfully!")
        print("📈 Check the generated plots to understand:")
        print("   • How priors influence posterior distributions")
        print("   • Uncertainty quantification in parameter estimates")
        print("   • Comparison between Bayesian and frequentist approaches")
        
    except Exception as e:
        print(f"\n❌ Error in Problem 1: {e}")
        import traceback
        traceback.print_exc()
