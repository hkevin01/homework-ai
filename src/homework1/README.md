# Homework 1: Introduction to Scientific Machine Learning

## 📚 Course Overview
This assignment introduces fundamental concepts in scientific machine learning, focusing on probabilistic reasoning, Bayesian inference, and real-world applications in engineering and science.

## 🎯 Learning Objectives
By completing this assignment, students will:
- Master Bayes' theorem and its applications in medical diagnostics
- Understand discrete probability distributions and random variables
- Apply probabilistic models to earthquake prediction
- Analyze mechanical system reliability using probability theory
- Develop computational skills in Python for scientific computing

## 🧩 Problem Descriptions

### Problem 1: Tuberculosis Test Analysis 🏥
**File:** `problem1_tuberculosis_test.py`

**Scenario:** You are a medical data analyst evaluating the effectiveness of a tuberculosis screening test. The test has known sensitivity and specificity rates, and you need to determine the probability that a patient actually has tuberculosis given a positive test result.

**Key Concepts:**
- Bayes' theorem application in medical diagnostics
- Sensitivity, specificity, and positive predictive value
- Prior probability and population prevalence
- False positive and false negative rates

**Real-world Application:** This type of analysis is crucial in medical decision-making, helping doctors interpret test results and make informed treatment decisions.

### Problem 2: Discrete Random Variables 🎲
**File:** `problem2_discrete_random_variables.py`

**Scenario:** Analyze various discrete probability distributions commonly encountered in scientific applications, including binomial, Poisson, and geometric distributions.

**Key Concepts:**
- Discrete probability mass functions
- Expected value and variance calculations
- Distribution parameter estimation
- Monte Carlo simulation methods

**Real-world Application:** These distributions model count data in experiments, arrival processes, and reliability studies.

### Problem 3: Earthquake Prediction Model 🌍
**File:** `problem3_earthquake_prediction.py`

**Scenario:** Develop a probabilistic model for earthquake occurrence based on historical seismic data. Analyze the relationship between magnitude, frequency, and geographic location.

**Key Concepts:**
- Exponential and power-law distributions
- Gutenberg-Richter law for earthquake magnitudes
- Poisson processes for temporal modeling
- Risk assessment and uncertainty quantification

**Real-world Application:** Essential for seismic hazard assessment, building codes, and disaster preparedness planning.

### Problem 4: Mechanical System Reliability 🔧
**File:** `problem4_mechanical_failure.py`

**Scenario:** Analyze the reliability of a mechanical system with multiple components, each having different failure rates and dependencies.

**Key Concepts:**
- Reliability functions and hazard rates
- Series and parallel system configurations
- Weibull distribution for failure modeling
- Maintenance scheduling optimization

**Real-world Application:** Critical for aerospace, automotive, and industrial equipment design and maintenance planning.

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