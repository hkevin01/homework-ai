"""
Problem 2: Practice with Discrete Random Variables

This module solves problems related to categorical random variables using scipy.stats.
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


class CategoricalRandomVariable:
    """Analyzer for categorical random variable problems."""
    
    def __init__(self, probabilities):
        """
        Initialize with probability mass function.
        
        Args:
            probabilities (list): List of probabilities for values [0, 1, 2, 3]
        """
        self.probabilities = np.array(probabilities)
        self.values = np.arange(len(probabilities))
        
        # Create scipy discrete random variable
        self.rv = stats.rv_discrete(
            values=(self.values, self.probabilities)
        )
    
    def calculate_expectation(self):
        """
        Calculate the expectation E[X].
        
        Returns:
            float: Expected value of the random variable
        """
        return self.rv.expect()
    
    def calculate_variance(self):
        """
        Calculate the variance V[X].
        
        Returns:
            float: Variance of the random variable
        """
        return self.rv.var()
    
    def plot_pmf(self, save_path=None):
        """
        Plot the probability mass function of X.
        
        Args:
            save_path (str, optional): Path to save the plot
        """
        plt.figure(figsize=(10, 6))
        
        # Create bar plot
        bars = plt.bar(self.values, self.probabilities, 
                      alpha=0.7, color='skyblue', edgecolor='navy')
        
        # Add value labels on bars
        for bar, prob in zip(bars, self.probabilities):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{prob:.2f}', ha='center', va='bottom')
        
        plt.xlabel('Values')
        plt.ylabel('Probability')
        plt.title('Probability Mass Function of Categorical Random Variable')
        plt.xticks(self.values)
        plt.grid(True, alpha=0.3)
        plt.ylim(0, max(self.probabilities) * 1.1)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def get_statistics(self):
        """
        Get comprehensive statistics of the random variable.
        
        Returns:
            dict: Dictionary containing various statistics
        """
        return {
            'expectation': self.calculate_expectation(),
            'variance': self.calculate_variance(),
            'standard_deviation': np.sqrt(self.calculate_variance()),
            'probabilities': dict(zip(self.values, self.probabilities))
        }


def main():
    """Main function to demonstrate categorical random variable analysis."""
    # Problem 2: X ~ Categorical(0.3, 0.1, 0.2, 0.4)
    probabilities = [0.3, 0.1, 0.2, 0.4]
    
    print("=== Problem 2: Discrete Random Variables ===")
    print(f"X ~ Categorical({', '.join(map(str, probabilities))})")
    
    # Create random variable object
    rv = CategoricalRandomVariable(probabilities)
    
    # Calculate expectation
    expectation = rv.calculate_expectation()
    print(f"\nA. Expectation E[X] = {expectation:.2f}")
    
    # Calculate variance
    variance = rv.calculate_variance()
    print(f"B. Variance V[X] = {variance:.2f}")
    
    # Get all statistics
    stats_dict = rv.get_statistics()
    print(f"\nAdditional Statistics:")
    print(f"Standard Deviation = {stats_dict['standard_deviation']:.2f}")
    print(f"Probability Mass Function:")
    for value, prob in stats_dict['probabilities'].items():
        print(f"  P(X = {value}) = {prob:.2f}")
    
    # Plot PMF
    print(f"\nC. Plotting Probability Mass Function...")
    rv.plot_pmf()


if __name__ == "__main__":
    main() 