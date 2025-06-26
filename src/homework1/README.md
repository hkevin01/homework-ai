# Homework 1 - Introduction to Scientific Machine Learning

This module contains complete solutions for the Scientific Machine Learning homework assignment, covering four main problems:

## Problem Structure

### Problem 1: Tuberculosis Test Assessment
- **File**: `problem1_tuberculosis_test.py`
- **Topic**: Bayesian probability and medical test evaluation
- **Key Concepts**: Prior/posterior probabilities, likelihood ratios, test accuracy

### Problem 2: Discrete Random Variables
- **File**: `problem2_discrete_random_variables.py`
- **Topic**: Categorical random variables and probability mass functions
- **Key Concepts**: Expectation, variance, PMF visualization

### Problem 3: Earthquake Prediction
- **File**: `problem3_earthquake_prediction.py`
- **Topic**: Poisson processes and earthquake probability modeling
- **Key Concepts**: Poisson distribution, time series analysis, prediction

### Problem 4: Mechanical Component Failure
- **File**: `problem4_mechanical_failure.py`
- **Topic**: Reliability analysis and failure time distributions
- **Key Concepts**: Exponential/Weibull distributions, reliability prediction

## Usage

### Running Individual Problems

```python
# Run Problem 1
python problem1_tuberculosis_test.py

# Run Problem 2
python problem2_discrete_random_variables.py

# Run Problem 3
python problem3_earthquake_prediction.py

# Run Problem 4
python problem4_mechanical_failure.py
```

### Running All Problems

```python
# Run all problems with unified output
python main.py
```

### Using as Modules

```python
from problem1_tuberculosis_test import TuberculosisTestAnalyzer
from problem2_discrete_random_variables import CategoricalRandomVariable
from problem3_earthquake_prediction import EarthquakeAnalyzer
from problem4_mechanical_failure import MechanicalFailureAnalyzer

# Create analyzers and run analyses
analyzer1 = TuberculosisTestAnalyzer()
analyzer2 = CategoricalRandomVariable([0.3, 0.1, 0.2, 0.4])
# ... etc
```

## Dependencies

Required packages (add to `requirements.txt`):
```
numpy
matplotlib
scipy
```

## Output

Each problem provides:
- Numerical solutions to all parts
- Statistical analysis and interpretations
- Visualization plots (where applicable)
- Comprehensive documentation

## Mathematical Solutions

The solutions include:
- **Problem 1**: Bayesian probability calculations using Bayes' theorem
- **Problem 2**: Expectation and variance calculations for categorical RVs
- **Problem 3**: Poisson process modeling for earthquake prediction
- **Problem 4**: Distribution fitting and reliability analysis

All mathematical derivations and interpretations are provided in the code comments and output. 