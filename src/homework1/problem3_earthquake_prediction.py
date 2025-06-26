"""
Problem 3: Earthquake Prediction in Southern California

This module analyzes earthquake data and predicts the probability of major 
earthquakes in Southern California.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


class EarthquakeAnalyzer:
    """Analyzer for earthquake prediction problems."""
    
    def __init__(self, earthquake_data):
        """
        Initialize with earthquake data.
        
        Args:
            earthquake_data (array): Array of earthquake counts per decade
        """
        self.earthquake_data = np.array(earthquake_data)
        self.decades = np.arange(1900, 2020, 10)
        
    def calculate_statistics(self):
        """
        Calculate basic statistics of earthquake occurrences.
        
        Returns:
            dict: Dictionary containing mean, variance, and other statistics
        """
        mean_earthquakes = np.mean(self.earthquake_data)
        variance_earthquakes = np.var(self.earthquake_data)
        
        return {
            'mean_per_decade': mean_earthquakes,
            'variance': variance_earthquakes,
            'std_deviation': np.sqrt(variance_earthquakes),
            'total_earthquakes': np.sum(self.earthquake_data),
            'decades_with_earthquakes': np.sum(self.earthquake_data > 0)
        }
    
    def fit_poisson_model(self):
        """
        Fit a Poisson model to the earthquake data.
        
        Returns:
            dict: Fitted model parameters and statistics
        """
        # Estimate lambda (rate parameter) from data
        lambda_estimate = np.mean(self.earthquake_data)
        
        # Create Poisson distribution
        poisson_rv = stats.poisson(lambda_estimate)
        
        # Calculate goodness of fit
        observed = self.earthquake_data
        expected = poisson_rv.pmf(np.arange(max(observed) + 1))
        
        return {
            'lambda_estimate': lambda_estimate,
            'poisson_distribution': poisson_rv,
            'model_fit': {
                'observed': observed,
                'expected': expected
            }
        }
    
    def predict_next_decade_probability(self, threshold=1):
        """
        Predict probability of major earthquakes in the next decade.
        
        Args:
            threshold (int): Minimum number of earthquakes to consider "major"
            
        Returns:
            float: Probability of threshold or more earthquakes
        """
        poisson_model = self.fit_poisson_model()
        lambda_est = poisson_model['lambda_estimate']
        
        # P(X >= threshold) = 1 - P(X < threshold)
        probability = 1 - stats.poisson.cdf(threshold - 1, lambda_est)
        
        return probability
    
    def plot_earthquake_data(self, save_path=None):
        """
        Plot earthquake data over time.
        
        Args:
            save_path (str, optional): Path to save the plot
        """
        plt.figure(figsize=(12, 8))
        
        # Plot earthquake counts
        plt.subplot(2, 1, 1)
        bars = plt.bar(self.decades, self.earthquake_data, 
                      alpha=0.7, color='red', edgecolor='darkred')
        
        # Add value labels
        for bar, count in zip(bars, self.earthquake_data):
            if count > 0:
                plt.text(bar.get_x() + bar.get_width()/2., count + 0.1,
                        str(count), ha='center', va='bottom')
        
        plt.xlabel('Decade')
        plt.ylabel('Number of Major Earthquakes')
        plt.title('Major Earthquakes in Southern California by Decade')
        plt.grid(True, alpha=0.3)
        plt.xticks(self.decades[::2], rotation=45)
        
        # Plot cumulative earthquakes
        plt.subplot(2, 1, 2)
        cumulative = np.cumsum(self.earthquake_data)
        plt.plot(self.decades, cumulative, 'b-o', linewidth=2, markersize=6)
        plt.xlabel('Decade')
        plt.ylabel('Cumulative Major Earthquakes')
        plt.title('Cumulative Major Earthquakes Over Time')
        plt.grid(True, alpha=0.3)
        plt.xticks(self.decades[::2], rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_poisson_fit(self, save_path=None):
        """
        Plot Poisson model fit to the data.
        
        Args:
            save_path (str, optional): Path to save the plot
        """
        poisson_model = self.fit_poisson_model()
        lambda_est = poisson_model['lambda_estimate']
        
        plt.figure(figsize=(10, 6))
        
        # Plot observed data
        unique_counts, observed_freq = np.unique(self.earthquake_data, 
                                                return_counts=True)
        observed_prob = observed_freq / len(self.earthquake_data)
        
        plt.bar(unique_counts, observed_prob, alpha=0.7, 
               color='red', label='Observed', edgecolor='darkred')
        
        # Plot Poisson model
        x_range = np.arange(0, max(unique_counts) + 3)
        poisson_prob = stats.poisson.pmf(x_range, lambda_est)
        
        plt.plot(x_range, poisson_prob, 'bo-', linewidth=2, 
                markersize=8, label=f'Poisson(λ={lambda_est:.2f})')
        
        plt.xlabel('Number of Earthquakes per Decade')
        plt.ylabel('Probability')
        plt.title('Poisson Model Fit to Earthquake Data')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()


def main():
    """Main function to demonstrate earthquake analysis."""
    # Earthquake data from the problem
    eq_data = np.array([
        0,  # 1900-1909
        1,  # 1910-1919
        2,  # 1920-1929
        0,  # 1930-1939
        3,  # 1940-1949
        2,  # 1950-1959
        1,  # 1960-1969
        2,  # 1970-1979
        1,  # 1980-1989
        2,  # 1990-1999
        1,  # 2000-2009
        0   # 2010-2019
    ])
    
    print("=== Problem 3: Earthquake Prediction ===")
    print("Earthquake data by decade (1900-2019):")
    for i, count in enumerate(eq_data):
        decade = 1900 + i * 10
        print(f"  {decade}-{decade+9}: {count} major earthquakes")
    
    # Create analyzer
    analyzer = EarthquakeAnalyzer(eq_data)
    
    # Calculate statistics
    stats_dict = analyzer.calculate_statistics()
    print(f"\nStatistics:")
    print(f"Mean earthquakes per decade: {stats_dict['mean_per_decade']:.2f}")
    print(f"Variance: {stats_dict['variance']:.2f}")
    print(f"Standard deviation: {stats_dict['std_deviation']:.2f}")
    print(f"Total major earthquakes: {stats_dict['total_earthquakes']}")
    
    # Predict next decade probability
    prob_next_decade = analyzer.predict_next_decade_probability(threshold=1)
    print(f"\nProbability of 1+ major earthquakes in next decade: "
          f"{prob_next_decade:.3f}")
    
    prob_next_decade_2 = analyzer.predict_next_decade_probability(threshold=2)
    print(f"Probability of 2+ major earthquakes in next decade: "
          f"{prob_next_decade_2:.3f}")
    
    # Plot data
    print(f"\nPlotting earthquake data...")
    analyzer.plot_earthquake_data()
    
    print(f"Plotting Poisson model fit...")
    analyzer.plot_poisson_fit()


if __name__ == "__main__":
    main() 