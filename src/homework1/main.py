"""
Main script for Homework 1 - Introduction to Scientific Machine Learning

This script runs all four problems and provides a unified interface for the 
homework solutions.
"""

from problem1_tuberculosis_test import TuberculosisTestAnalyzer
from problem2_discrete_random_variables import CategoricalRandomVariable
from problem3_earthquake_prediction import EarthquakeAnalyzer
from problem4_mechanical_failure import MechanicalFailureAnalyzer


def run_problem1():
    """Run Problem 1: Tuberculosis Test Assessment."""
    print("\n" + "="*60)
    print("PROBLEM 1: Tuberculosis Test Assessment")
    print("="*60)
    
    analyzer = TuberculosisTestAnalyzer()
    
    print("A. Prior probability of disease:")
    prior = analyzer.calculate_prior_probability()
    print(f"   P(B|I) = {prior:.4f}")
    
    print("\nB. Posterior probability given positive test:")
    posterior = analyzer.calculate_posterior_probability()
    print(f"   P(B|A,I) = {posterior:.4f}")
    
    results = analyzer.analyze_test_usefulness()
    print(f"\nC. Test Analysis:")
    print(f"   Likelihood ratio: {results['likelihood_ratio']:.2f}")
    print(f"   Odds ratio: {results['odds_ratio']:.2f}")
    print(f"   Sensitivity: {results['test_accuracy']['sensitivity']:.2f}")
    print(f"   Specificity: {results['test_accuracy']['specificity']:.2f}")


def run_problem2():
    """Run Problem 2: Discrete Random Variables."""
    print("\n" + "="*60)
    print("PROBLEM 2: Practice with Discrete Random Variables")
    print("="*60)
    
    # X ~ Categorical(0.3, 0.1, 0.2, 0.4)
    probabilities = [0.3, 0.1, 0.2, 0.4]
    rv = CategoricalRandomVariable(probabilities)
    
    print(f"X ~ Categorical({', '.join(map(str, probabilities))})")
    
    print("\nA. Expectation E[X]:")
    expectation = rv.calculate_expectation()
    print(f"   E[X] = {expectation:.2f}")
    
    print("\nB. Variance V[X]:")
    variance = rv.calculate_variance()
    print(f"   V[X] = {variance:.2f}")
    
    print("\nC. Probability Mass Function:")
    stats_dict = rv.get_statistics()
    for value, prob in stats_dict['probabilities'].items():
        print(f"   P(X = {value}) = {prob:.2f}")
    
    print("\nPlotting PMF...")
    rv.plot_pmf()


def run_problem3():
    """Run Problem 3: Earthquake Prediction."""
    print("\n" + "="*60)
    print("PROBLEM 3: Earthquake Prediction in Southern California")
    print("="*60)
    
    # Earthquake data by decade (1900-2019)
    eq_data = np.array([0, 1, 2, 0, 3, 2, 1, 2, 1, 2, 1, 0])
    analyzer = EarthquakeAnalyzer(eq_data)
    
    print("Earthquake data by decade:")
    for i, count in enumerate(eq_data):
        decade = 1900 + i * 10
        print(f"   {decade}-{decade+9}: {count} major earthquakes")
    
    stats_dict = analyzer.calculate_statistics()
    print(f"\nA. Statistics:")
    print(f"   Mean earthquakes per decade: {stats_dict['mean_per_decade']:.2f}")
    print(f"   Variance: {stats_dict['variance']:.2f}")
    print(f"   Standard deviation: {stats_dict['std_deviation']:.2f}")
    
    print(f"\nB. Poisson Model Analysis:")
    poisson_model = analyzer.fit_poisson_model()
    print(f"   Estimated λ = {poisson_model['lambda_estimate']:.3f}")
    
    print(f"\nC. Predictions for next decade:")
    prob_1plus = analyzer.predict_next_decade_probability(threshold=1)
    prob_2plus = analyzer.predict_next_decade_probability(threshold=2)
    print(f"   P(≥1 major earthquake) = {prob_1plus:.3f}")
    print(f"   P(≥2 major earthquakes) = {prob_2plus:.3f}")
    
    print("\nPlotting earthquake data and Poisson fit...")
    analyzer.plot_earthquake_data()
    analyzer.plot_poisson_fit()


def run_problem4():
    """Run Problem 4: Mechanical Component Failure."""
    print("\n" + "="*60)
    print("PROBLEM 4: Mechanical Component Failure Analysis")
    print("="*60)
    
    # Failure time data (years)
    failure_times = np.array([10.5, 7.5, 8.1, 9.2, 6.8, 11.3, 8.9, 7.2, 9.8, 8.5])
    analyzer = MechanicalFailureAnalyzer(failure_times)
    
    print("Failure time data:")
    for i, time in enumerate(failure_times):
        print(f"   Gear {i+1}: {time:.1f} years")
    
    stats_dict = analyzer.calculate_basic_statistics()
    print(f"\nA. Basic Statistics:")
    print(f"   Mean failure time: {stats_dict['mean']:.2f} years")
    print(f"   Standard deviation: {stats_dict['std_deviation']:.2f} years")
    print(f"   Median failure time: {stats_dict['median']:.2f} years")
    
    comparison = analyzer.compare_distributions()
    print(f"\nB. Distribution Comparison:")
    print(f"   Exponential Distribution:")
    print(f"     λ = {comparison['exponential']['lambda']:.3f}")
    print(f"     Mean lifetime = {comparison['exponential']['mean_lifetime']:.2f} years")
    print(f"     KS p-value = {comparison['exponential']['ks_pvalue']:.3f}")
    
    print(f"   Weibull Distribution:")
    print(f"     Shape parameter = {comparison['weibull']['shape']:.3f}")
    print(f"     Scale parameter = {comparison['weibull']['scale']:.3f}")
    print(f"     KS p-value = {comparison['weibull']['ks_pvalue']:.3f}")
    
    print(f"\nC. Reliability Predictions:")
    reliability_5yr = analyzer.predict_reliability(5.0)
    reliability_10yr = analyzer.predict_reliability(10.0)
    print(f"   At 5 years:")
    print(f"     Exponential: {reliability_5yr['exponential_reliability']:.3f}")
    print(f"     Weibull: {reliability_5yr['weibull_reliability']:.3f}")
    print(f"   At 10 years:")
    print(f"     Exponential: {reliability_10yr['exponential_reliability']:.3f}")
    print(f"     Weibull: {reliability_10yr['weibull_reliability']:.3f}")
    
    print("\nPlotting failure data and distribution fits...")
    analyzer.plot_failure_data()


def main():
    """Main function to run all homework problems."""
    print("Homework 1 - Introduction to Scientific Machine Learning")
    print("Solutions and Analysis")
    print("="*60)
    
    try:
        run_problem1()
        run_problem2()
        run_problem3()
        run_problem4()
        
        print("\n" + "="*60)
        print("All problems completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\nError running homework problems: {e}")
        print("Please check that all required packages are installed.")


if __name__ == "__main__":
    main() 