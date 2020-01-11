"""
This file contains the classes handling the tests as described in the file 'run_tests'.

Each test method has the same description regarding the test as presented in 'run_tests'
"""

import unittest
import sys

from tests.test import ReqClassTestingStepOne, ReqClassTestingStepTwo, ReqClassTestingStepThree, ReqClassTestingStepFour
"""
Tests
"""

def is_finished_with_step(test_case_class_to_use):
    """Helper function to initialize, load, and run tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(
        loader.loadTestsFromTestCase(
            test_case_class_to_use
        )
    )

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.skipped:
        return False

    return result.wasSuccessful()


def is_finished_with_step_one():
    """Run the first batch of tests"""
    print('-'*70 + "\nStarting test suite 1:\n")
    return is_finished_with_step(ReqClassTestingStepOne)

def is_finished_with_step_two():
    """Run the second batch of tests"""
    print('-'*70 + "\nStarting test suite 2:\n")
    return is_finished_with_step(ReqClassTestingStepTwo)

def is_finished_with_step_three():
    """Run the second batch of tests"""
    print('-'*70 + "\nStarting test suite 3:\n")
    return is_finished_with_step(ReqClassTestingStepThree)
