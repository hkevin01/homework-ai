"""
Problem 4: Mechanical Component Failure Analysis

This module analyzes mechanical component failure data and determines appropriate 
probability distributions for failure times.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.optimize import curve_fit


class MechanicalFailureAnalyzer:
    """Analyzer for mechanical component failure problems."""
    
    def __init__(self, failure_times):
        """
        Initialize with failure time data.
        
        Args:
            failure_times (array): Array of failure times in years
        """
        self.failure_times = np.array(failure_times)
        self.n_samples = len(failure_times)
        
    def calculate_basic_statistics(self):
        """
        Calculate basic statistics of failure times.
        
        Returns:
            dict: Dictionary containing mean, variance, and other statistics
        """
        mean_time = np.mean(self.failure_times)
        variance_time = np.var(self.failure_times, ddof=1)  # Sample variance
        
        return {
            'mean': mean_time,
            'variance': variance_time,
            'std_deviation': np.sqrt(variance_time),
            'median': np.median(self.failure_times),
            'min_time': np.min(self.failure_times),
            'max_time': np.max(self.failure_times),
            'sample_size': self.n_samples
        }
    
    def fit_exponential_distribution(self):
        """
        Fit exponential distribution to failure data.
        
        Returns:
            dict: Fitted exponential distribution parameters
        """
        # Estimate lambda (rate parameter) from data
        lambda_estimate = 1 / np.mean(self.failure_times)
        
        # Create exponential distribution
        exp_rv = stats.expon(scale=1/lambda_estimate)
        
        return {
            'lambda_estimate': lambda_estimate,
            'mean_lifetime': 1/lambda_estimate,
            'exponential_distribution': exp_rv
        }
    
    def fit_weibull_distribution(self):
        """
        Fit Weibull distribution to failure data.
        
        Returns:
            dict: Fitted Weibull distribution parameters
        """
        # Fit Weibull distribution
        shape, loc, scale = stats.weibull_min.fit(self.failure_times)
        
        # Create Weibull distribution
        weibull_rv = stats.weibull_min(shape, loc, scale)
        
        return {
            'shape_parameter': shape,
            'location_parameter': loc,
            'scale_parameter': scale,
            'weibull_distribution': weibull_rv
        }
    
    def plot_failure_data(self, save_path=None):
        """
        Plot failure time data and fitted distributions.
        
        Args:
            save_path (str, optional): Path to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Histogram of failure times
        axes[0, 0].hist(self.failure_times, bins=8, alpha=0.7, 
                       color='lightblue', edgecolor='black', density=True)
        axes[0, 0].set_xlabel('Failure Time (years)')
        axes[0, 0].set_ylabel('Density')
        axes[0, 0].set_title('Histogram of Failure Times')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Empirical CDF
        sorted_times = np.sort(self.failure_times)
        empirical_cdf = np.arange(1, len(sorted_times) + 1) / len(sorted_times)
        axes[0, 1].step(sorted_times, empirical_cdf, where='post', 
                       label='Empirical CDF', linewidth=2)
        axes[0, 1].set_xlabel('Failure Time (years)')
        axes[0, 1].set_ylabel('Cumulative Probability')
        axes[0, 1].set_title('Empirical Cumulative Distribution Function')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].legend()
        
        # Exponential fit
        exp_fit = self.fit_exponential_distribution()
        x_range = np.linspace(0, max(self.failure_times) * 1.2, 100)
        exp_pdf = exp_fit['exponential_distribution'].pdf(x_range)
        exp_cdf = exp_fit['exponential_distribution'].cdf(x_range)
        
        axes[1, 0].hist(self.failure_times, bins=8, alpha=0.7, 
                       color='lightblue', edgecolor='black', density=True)
        axes[1, 0].plot(x_range, exp_pdf, 'r-', linewidth=2, 
                       label=f'Exponential(λ={exp_fit["lambda_estimate"]:.3f})')
        axes[1, 0].set_xlabel('Failure Time (years)')
        axes[1, 0].set_ylabel('Density')
        axes[1, 0].set_title('Exponential Distribution Fit')
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].legend()
        
        # Weibull fit
        weibull_fit = self.fit_weibull_distribution()
        weibull_pdf = weibull_fit['weibull_distribution'].pdf(x_range)
        weibull_cdf = weibull_fit['weibull_distribution'].cdf(x_range)
        
        axes[1, 1].hist(self.failure_times, bins=8, alpha=0.7, 
                       color='lightblue', edgecolor='black', density=True)
        axes[1, 1].plot(x_range, weibull_pdf, 'g-', linewidth=2, 
                       label=f'Weibull(shape={weibull_fit["shape_parameter"]:.2f})')
        axes[1, 1].set_xlabel('Failure Time (years)')
        axes[1, 1].set_ylabel('Density')
        axes[1, 1].set_title('Weibull Distribution Fit')
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def compare_distributions(self):
        """
        Compare different distribution fits using goodness-of-fit tests.
        
        Returns:
            dict: Comparison results with test statistics
        """
        # Fit distributions
        exp_fit = self.fit_exponential_distribution()
        weibull_fit = self.fit_weibull_distribution()
        
        # Kolmogorov-Smirnov tests
        ks_exp = stats.kstest(self.failure_times, 
                             exp_fit['exponential_distribution'].cdf)
        ks_weibull = stats.kstest(self.failure_times, 
                                 weibull_fit['weibull_distribution'].cdf)
        
        return {
            'exponential': {
                'lambda': exp_fit['lambda_estimate'],
                'mean_lifetime': exp_fit['mean_lifetime'],
                'ks_statistic': ks_exp.statistic,
                'ks_pvalue': ks_exp.pvalue
            },
            'weibull': {
                'shape': weibull_fit['shape_parameter'],
                'scale': weibull_fit['scale_parameter'],
                'ks_statistic': ks_weibull.statistic,
                'ks_pvalue': ks_weibull.pvalue
            }
        }
    
    def predict_reliability(self, time_threshold):
        """
        Predict reliability at a given time threshold.
        
        Args:
            time_threshold (float): Time threshold in years
            
        Returns:
            dict: Reliability predictions from different models
        """
        exp_fit = self.fit_exponential_distribution()
        weibull_fit = self.fit_weibull_distribution()
        
        # Reliability = 1 - CDF
        exp_reliability = 1 - exp_fit['exponential_distribution'].cdf(time_threshold)
        weibull_reliability = 1 - weibull_fit['weibull_distribution'].cdf(time_threshold)
        
        return {
            'time_threshold': time_threshold,
            'exponential_reliability': exp_reliability,
            'weibull_reliability': weibull_reliability
        }


def main():
    """Main function to demonstrate mechanical failure analysis."""
    # Failure time data from the problem
    time_to_fail_data = np.array([
        10.5, 7.5, 8.1, 9.2, 6.8, 11.3, 8.9, 7.2, 9.8, 8.5
    ])
    
    print("=== Problem 4: Mechanical Component Failure ===")
    print("Failure time data (years):")
    for i, time in enumerate(time_to_fail_data):
        print(f"  Gear {i+1}: {time:.1f} years")
    
    # Create analyzer
    analyzer = MechanicalFailureAnalyzer(time_to_fail_data)
    
    # Calculate basic statistics
    stats_dict = analyzer.calculate_basic_statistics()
    print(f"\nBasic Statistics:")
    print(f"Mean failure time: {stats_dict['mean']:.2f} years")
    print(f"Standard deviation: {stats_dict['std_deviation']:.2f} years")
    print(f"Median failure time: {stats_dict['median']:.2f} years")
    print(f"Range: {stats_dict['min_time']:.1f} - {stats_dict['max_time']:.1f} years")
    
    # Compare distributions
    comparison = analyzer.compare_distributions()
    print(f"\nDistribution Comparison:")
    print(f"Exponential Distribution:")
    print(f"  λ = {comparison['exponential']['lambda']:.3f}")
    print(f"  Mean lifetime = {comparison['exponential']['mean_lifetime']:.2f} years")
    print(f"  KS statistic = {comparison['exponential']['ks_statistic']:.3f}")
    print(f"  KS p-value = {comparison['exponential']['ks_pvalue']:.3f}")
    
    print(f"\nWeibull Distribution:")
    print(f"  Shape parameter = {comparison['weibull']['shape']:.3f}")
    print(f"  Scale parameter = {comparison['weibull']['scale']:.3f}")
    print(f"  KS statistic = {comparison['weibull']['ks_statistic']:.3f}")
    print(f"  KS p-value = {comparison['weibull']['ks_pvalue']:.3f}")
    
    # Predict reliability
    reliability_5yr = analyzer.predict_reliability(5.0)
    reliability_10yr = analyzer.predict_reliability(10.0)
    
    print(f"\nReliability Predictions:")
    print(f"At 5 years:")
    print(f"  Exponential: {reliability_5yr['exponential_reliability']:.3f}")
    print(f"  Weibull: {reliability_5yr['weibull_reliability']:.3f}")
    
    print(f"At 10 years:")
    print(f"  Exponential: {reliability_10yr['exponential_reliability']:.3f}")
    print(f"  Weibull: {reliability_10yr['weibull_reliability']:.3f}")
    
    # Plot data and fits
    print(f"\nPlotting failure data and distribution fits...")
    analyzer.plot_failure_data()


if __name__ == "__main__":
    main() 