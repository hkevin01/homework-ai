"""
Problem 1: Tuberculosis Test Assessment

This module solves the tuberculosis test assessment problem using Bayesian 
probability. The problem involves calculating probabilities related to disease 
testing accuracy.

Question:
A new medical test for tuberculosis has been developed. The test has the following 
characteristics:
- 80% of patients with tuberculosis test positive (sensitivity = 0.80)
- 90% of patients without tuberculosis test negative (specificity = 0.90)
- The prevalence of tuberculosis in the population is 0.4% (prior probability = 0.004)

Given that a patient tests positive, what is the probability that they actually 
have tuberculosis? Calculate both the prior and posterior probabilities and 
analyze whether this test is useful for medical diagnosis.

Learning Objectives:
- Apply Bayes' theorem to medical diagnosis problems
- Understand the difference between prior and posterior probabilities
- Analyze test sensitivity, specificity, and predictive values
- Evaluate the clinical usefulness of diagnostic tests
"""


class TuberculosisTestAnalyzer:
    """Analyzer for tuberculosis test assessment problem."""
    
    def __init__(self):
        """Initialize the analyzer with given probabilities."""
        # Prior information
        self.p_disease = 0.004  # 0.4% of population has tuberculosis
        
        # Test accuracy
        self.p_positive_given_disease = 0.80  # 80% true positive rate
        self.p_negative_given_no_disease = 0.90  # 90% true negative rate
        
        # Calculate derived probabilities
        self.p_no_disease = 1 - self.p_disease
        self.p_positive_given_no_disease = 1 - self.p_negative_given_no_disease
        self.p_negative_given_disease = 1 - self.p_positive_given_disease
    
    def calculate_prior_probability(self):
        """
        Calculate the prior probability that a patient has tuberculosis.
        
        Returns:
            float: Prior probability P(B|I) = 0.004
        """
        return self.p_disease
    
    def calculate_posterior_probability(self):
        """
        Calculate the posterior probability that a patient has tuberculosis 
        given a positive test result.
        
        Returns:
            float: Posterior probability P(B|A,I)
        """
        # P(A|B,I) = P(positive|disease) = 0.80
        p_positive_given_disease = self.p_positive_given_disease
        
        # P(A|not B,I) = P(positive|no disease) = 0.10
        p_positive_given_no_disease = self.p_positive_given_no_disease
        
        # P(A|I) = P(positive) = P(positive|disease)*P(disease) + 
        # P(positive|no disease)*P(no disease)
        p_positive = (p_positive_given_disease * self.p_disease + 
                     p_positive_given_no_disease * self.p_no_disease)
        
        # Bayes' theorem: P(B|A,I) = P(A|B,I) * P(B|I) / P(A|I)
        posterior = (p_positive_given_disease * self.p_disease) / p_positive
        
        return posterior
    
    def analyze_test_usefulness(self):
        """
        Analyze the usefulness of the tuberculosis test.
        
        Returns:
            dict: Analysis results including probabilities and interpretation
        """
        prior = self.calculate_prior_probability()
        posterior = self.calculate_posterior_probability()
        
        # Calculate likelihood ratio
        likelihood_ratio = (self.p_positive_given_disease / 
                           self.p_positive_given_no_disease)
        
        # Calculate odds ratio
        prior_odds = prior / (1 - prior)
        posterior_odds = posterior / (1 - posterior)
        odds_ratio = posterior_odds / prior_odds
        
        return {
            'prior_probability': prior,
            'posterior_probability': posterior,
            'likelihood_ratio': likelihood_ratio,
            'odds_ratio': odds_ratio,
            'test_accuracy': {
                'sensitivity': self.p_positive_given_disease,
                'specificity': self.p_negative_given_no_disease
            }
        }


def main():
    """Main function to demonstrate the tuberculosis test analysis."""
    analyzer = TuberculosisTestAnalyzer()
    
    print("=== Tuberculosis Test Assessment ===")
    prior = analyzer.calculate_prior_probability()
    posterior = analyzer.calculate_posterior_probability()
    print(f"Prior probability of disease: {prior:.4f}")
    print(f"Posterior probability given positive test: {posterior:.4f}")
    
    results = analyzer.analyze_test_usefulness()
    print("\nTest Analysis:")
    print(f"Likelihood ratio: {results['likelihood_ratio']:.2f}")
    print(f"Odds ratio: {results['odds_ratio']:.2f}")
    print(f"Sensitivity: {results['test_accuracy']['sensitivity']:.2f}")
    print(f"Specificity: {results['test_accuracy']['specificity']:.2f}")


if __name__ == "__main__":
    main() 