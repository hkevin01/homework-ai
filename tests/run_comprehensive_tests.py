"""
Comprehensive Test Runner for Homework AI Project

This script runs all test suites and provides a detailed summary report.
"""

import os
import subprocess
import sys
import time
from datetime import datetime

import pytest


def run_test_suite(test_file, description):
    """Run a specific test suite and return results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Test file: {test_file}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Run the test suite
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Parse results
        if result.returncode == 0:
            status = "PASSED"
            # Count passed tests
            passed_tests = len([line for line in result.stdout.split('\n') 
                              if 'PASSED' in line])
            failed_tests = 0
        else:
            status = "FAILED"
            # Count failed tests
            failed_tests = len([line for line in result.stdout.split('\n') 
                              if 'FAILED' in line])
            passed_tests = len([line for line in result.stdout.split('\n') 
                              if 'PASSED' in line])
        
        print(f"Status: {status}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Passed tests: {passed_tests}")
        print(f"Failed tests: {failed_tests}")
        
        if result.stdout:
            print("\nTest Output:")
            print(result.stdout)
        
        if result.stderr:
            print("\nTest Errors:")
            print(result.stderr)
        
        return {
            'status': status,
            'duration': duration,
            'passed': passed_tests,
            'failed': failed_tests,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        print("Test suite timed out after 5 minutes")
        return {
            'status': 'TIMEOUT',
            'duration': 300,
            'passed': 0,
            'failed': 0,
            'stdout': '',
            'stderr': 'Test suite timed out'
        }
    except Exception as e:
        print(f"Error running test suite: {e}")
        return {
            'status': 'ERROR',
            'duration': 0,
            'passed': 0,
            'failed': 0,
            'stdout': '',
            'stderr': str(e)
        }


def run_individual_script_tests():
    """Run tests for individual problem scripts."""
    print(f"\n{'='*60}")
    print("Testing Individual Problem Scripts")
    print(f"{'='*60}")
    
    problem_files = [
        'src/homework1/problem1_tuberculosis_test.py',
        'src/homework1/problem2_discrete_random_variables.py',
        'src/homework1/problem3_earthquake_prediction.py',
        'src/homework1/problem4_mechanical_failure.py'
    ]
    
    results = {}
    
    for problem_file in problem_files:
        if os.path.exists(problem_file):
            print(f"\nTesting: {problem_file}")
            start_time = time.time()
            
            try:
                result = subprocess.run(
                    [sys.executable, problem_file],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                end_time = time.time()
                duration = end_time - start_time
                
                if result.returncode == 0:
                    status = "PASSED"
                    print(f"✓ {problem_file} - PASSED ({duration:.2f}s)")
                else:
                    status = "FAILED"
                    print(f"✗ {problem_file} - FAILED ({duration:.2f}s)")
                    print(f"Error: {result.stderr}")
                
                results[problem_file] = {
                    'status': status,
                    'duration': duration,
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
                
            except subprocess.TimeoutExpired:
                print(f"✗ {problem_file} - TIMEOUT")
                results[problem_file] = {
                    'status': 'TIMEOUT',
                    'duration': 60,
                    'returncode': -1,
                    'stdout': '',
                    'stderr': 'Timeout'
                }
            except Exception as e:
                print(f"✗ {problem_file} - ERROR: {e}")
                results[problem_file] = {
                    'status': 'ERROR',
                    'duration': 0,
                    'returncode': -1,
                    'stdout': '',
                    'stderr': str(e)
                }
        else:
            print(f"✗ {problem_file} - FILE NOT FOUND")
            results[problem_file] = {
                'status': 'NOT_FOUND',
                'duration': 0,
                'returncode': -1,
                'stdout': '',
                'stderr': 'File not found'
            }
    
    return results


def generate_summary_report(test_results, script_results):
    """Generate a comprehensive summary report."""
    print(f"\n{'='*80}")
    print("COMPREHENSIVE TEST SUMMARY REPORT")
    print(f"{'='*80}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    # Test suite summary
    print("\nTEST SUITE RESULTS:")
    print("-" * 40)
    
    total_passed = 0
    total_failed = 0
    total_duration = 0
    
    for test_name, result in test_results.items():
        status_icon = "✓" if result['status'] == 'PASSED' else "✗"
        print(f"{status_icon} {test_name}: {result['status']} "
              f"({result['passed']} passed, {result['failed']} failed, "
              f"{result['duration']:.2f}s)")
        
        total_passed += result['passed']
        total_failed += result['failed']
        total_duration += result['duration']
    
    # Script test summary
    print("\nINDIVIDUAL SCRIPT RESULTS:")
    print("-" * 40)
    
    script_passed = 0
    script_failed = 0
    script_duration = 0
    
    for script_name, result in script_results.items():
        status_icon = "✓" if result['status'] == 'PASSED' else "✗"
        print(f"{status_icon} {os.path.basename(script_name)}: {result['status']} "
              f"({result['duration']:.2f}s)")
        
        if result['status'] == 'PASSED':
            script_passed += 1
        else:
            script_failed += 1
        script_duration += result['duration']
    
    # Overall summary
    print(f"\n{'='*80}")
    print("OVERALL SUMMARY:")
    print(f"{'='*80}")
    
    total_tests = total_passed + total_failed
    total_scripts = script_passed + script_failed
    
    if total_tests > 0:
        test_success_rate = (total_passed / total_tests) * 100
    else:
        test_success_rate = 0
    
    if total_scripts > 0:
        script_success_rate = (script_passed / total_scripts) * 100
    else:
        script_success_rate = 0
    
    print(f"Test Suites: {len(test_results)} total")
    print(f"  - Passed: {sum(1 for r in test_results.values() if r['status'] == 'PASSED')}")
    print(f"  - Failed: {sum(1 for r in test_results.values() if r['status'] != 'PASSED')}")
    print(f"  - Success Rate: {test_success_rate:.1f}%")
    
    print(f"\nIndividual Tests: {total_tests} total")
    print(f"  - Passed: {total_passed}")
    print(f"  - Failed: {total_failed}")
    print(f"  - Success Rate: {test_success_rate:.1f}%")
    
    print(f"\nProblem Scripts: {total_scripts} total")
    print(f"  - Passed: {script_passed}")
    print(f"  - Failed: {script_failed}")
    print(f"  - Success Rate: {script_success_rate:.1f}%")
    
    print(f"\nTotal Test Duration: {total_duration + script_duration:.2f} seconds")
    
    # Recommendations
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS:")
    print(f"{'='*80}")
    
    if total_failed > 0:
        print("⚠️  Some tests failed. Please review the failed tests above.")
    
    if script_failed > 0:
        print("⚠️  Some problem scripts failed. Check the script execution.")
    
    if test_success_rate < 80:
        print("⚠️  Test success rate is below 80%. Consider improving test coverage.")
    
    if total_passed > 0 and total_failed == 0:
        print("✅ All tests passed! The system is working correctly.")
    
    if script_passed == total_scripts and total_scripts > 0:
        print("✅ All problem scripts are working correctly.")
    
    print(f"\n{'='*80}")


def main():
    """Main test runner function."""
    print("Homework AI - Comprehensive Test Suite")
    print("=" * 50)
    
    # Define test suites
    test_suites = [
        ('tests/test_homework1_problems.py', 'Problem Script Tests'),
        ('tests/test_gui_functionality.py', 'GUI Functionality Tests'),
        ('tests/test_output_population.py', 'Output Population Tests'),
        ('tests/test_simple_gui_no_errors.py', 'Simple GUI Error Tests')
    ]
    
    # Run test suites
    test_results = {}
    for test_file, description in test_suites:
        if os.path.exists(test_file):
            result = run_test_suite(test_file, description)
            test_results[description] = result
        else:
            print(f"\n⚠️  Test file not found: {test_file}")
            test_results[description] = {
                'status': 'NOT_FOUND',
                'duration': 0,
                'passed': 0,
                'failed': 0,
                'stdout': '',
                'stderr': 'Test file not found'
            }
    
    # Run individual script tests
    script_results = run_individual_script_tests()
    
    # Generate summary report
    generate_summary_report(test_results, script_results)
    
    # Return appropriate exit code
    total_failed = sum(r['failed'] for r in test_results.values())
    script_failed = sum(1 for r in script_results.values() if r['status'] != 'PASSED')
    
    if total_failed > 0 or script_failed > 0:
        print("\n❌ Some tests failed. Please review the results above.")
        return 1
    else:
        print("\n✅ All tests passed successfully!")
        return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 