import pytest
import pandas as pd
import os
from tests.data.test_data import TEST_COURSES, TEST_POLICIES, TEST_STUDENT_PROFILES

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    """Create test CSV files before running tests"""
    pd.DataFrame(TEST_COURSES).to_csv("test_courses.csv", index=False)
    pd.DataFrame(TEST_POLICIES).to_csv("test_policies.csv", index=False)
    yield
    # Cleanup after tests
    os.remove("test_courses.csv")
    os.remove("test_policies.csv")

@pytest.fixture
def test_student_profiles():
    """Return test student profiles"""
    return TEST_STUDENT_PROFILES

@pytest.fixture
def test_courses():
    """Return test course data"""
    return TEST_COURSES

@pytest.fixture
def test_policies():
    """Return test policy data"""
    return TEST_POLICIES 