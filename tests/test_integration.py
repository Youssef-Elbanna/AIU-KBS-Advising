import unittest
import pandas as pd
from integration.data_manager import DataManager
from tests.data.test_data import TEST_COURSES, TEST_POLICIES, TEST_STUDENT_PROFILES
import pytest
from Inference_engine_KBS import AdvisingEngine, StudentProfile

class TestDataManagerIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test CSV files
        pd.DataFrame(TEST_COURSES).to_csv('tests/data/test_courses.csv', index=False)
        pd.DataFrame(TEST_POLICIES).to_csv('tests/data/test_policies.csv', index=False)
        
    def setUp(self):
        self.data_manager = DataManager(test_mode=True)
        self.data_manager.courses_df = pd.DataFrame(TEST_COURSES)
        self.data_manager.policies_df = pd.DataFrame(TEST_POLICIES)

    def test_credit_limit_calculation(self):
        """Test credit limit calculation for different CGPA ranges"""
        test_cases = [
            (3.5, "FALL", 22),  # High CGPA
            (2.5, "FALL", 20),  # Medium CGPA
            (1.8, "FALL", 12)   # Low CGPA
        ]
        
        for cgpa, semester, expected_limit in test_cases:
            with self.subTest(cgpa=cgpa):
                limit = self.data_manager.get_credit_limit(cgpa, semester)
                self.assertEqual(limit, expected_limit)

    def test_prerequisite_validation(self):
        """Test prerequisite validation logic"""
        # Test case 1: Course with no prerequisites
        result = self.data_manager.validate_course_selection(
            "MAT111",
            [],
            "FALL"
        )
        self.assertTrue(result['valid'])
        
        # Test case 2: Course with unmet prerequisites
        result = self.data_manager.validate_course_selection(
            "CSE015",
            [],
            "SPRING"
        )
        self.assertFalse(result['valid'])
        self.assertIn("CSE014", result['reason'])
        
        # Test case 3: Course with met prerequisites
        result = self.data_manager.validate_course_selection(
            "CSE015",
            ["CSE014"],
            "SPRING"
        )
        self.assertTrue(result['valid'])

    def test_available_courses(self):
        """Test getting available courses"""
        available = self.data_manager.get_available_courses(
            passed_courses=[],
            semester="FALL",
            cgpa=3.5
        )
        assert any(course["Course Code"] == "MAT111" for course in available)
        assert any(course["Course Code"] == "CSE014" for course in available)
        assert not any(course["Course Code"] == "CSE015" for course in available)

    def test_semester_availability(self):
        """Test semester-based course availability"""
        # Test FALL semester courses
        fall_courses = self.data_manager.get_available_courses(
            [],
            "FALL",
            3.0
        )
        fall_codes = [c['Course Code'] for c in fall_courses]
        self.assertIn("MAT111", fall_codes)
        self.assertIn("CSE014", fall_codes)
        self.assertNotIn("CSE015", fall_codes)
        
        # Test SPRING semester courses
        spring_courses = self.data_manager.get_available_courses(
            ["CSE014"],
            "SPRING",
            3.0
        )
        spring_codes = [c['Course Code'] for c in spring_courses]
        self.assertIn("CSE015", spring_codes)
        self.assertNotIn("CSE014", spring_codes)

class TestKBSIntegration:
    def test_data_loading(self):
        """Test data integration between CSV files and KBS"""
        # Create test CSV files
        pd.DataFrame(TEST_COURSES).to_csv("test_courses.csv", index=False)
        pd.DataFrame(TEST_POLICIES).to_csv("test_policies.csv", index=False)
        
        # Initialize engine with test data
        student_data = TEST_STUDENT_PROFILES[0]
        engine = AdvisingEngine(TEST_COURSES, student_data, pd.DataFrame(TEST_POLICIES))
        assert len(engine.courses) > 0
        assert len(engine.policies_df) > 0

    def test_prerequisite_validation(self):
        """Test prerequisite validation logic"""
        # Test student with no completed courses
        student_data = TEST_STUDENT_PROFILES[0]
        engine = AdvisingEngine(TEST_COURSES, student_data, pd.DataFrame(TEST_POLICIES))
        engine.reset()
        engine.declare(StudentProfile(**student_data))
        engine.run()
        
        # Should recommend courses with no prerequisites
        assert any(course["Course Code"] == "MAT111" for course in engine.recommended_courses)
        assert any(course["Course Code"] == "CSE014" for course in engine.recommended_courses)
        assert not any(course["Course Code"] == "CSE015" for course in engine.recommended_courses)  # Has prerequisite

        # Test student with completed prerequisite
        student_data = TEST_STUDENT_PROFILES[1]
        engine = AdvisingEngine(TEST_COURSES, student_data, pd.DataFrame(TEST_POLICIES))
        engine.reset()
        engine.declare(StudentProfile(**student_data))
        engine.run()
        assert any(course["Course Code"] == "CSE015" for course in engine.recommended_courses)

    def test_credit_limit_policy(self):
        """Test credit hours limit policy"""
        student_data = TEST_STUDENT_PROFILES[0]
        engine = AdvisingEngine(TEST_COURSES, student_data, pd.DataFrame(TEST_POLICIES))
        engine.reset()
        engine.declare(StudentProfile(**student_data))
        engine.run()
        
        total_credits = sum(course["Credit Hours"] for course in engine.recommended_courses)
        assert total_credits <= 22  # Maximum credit limit for high CGPA

    def test_semester_offering(self):
        """Test semester-specific course offerings"""
        # Test FALL semester
        fall_student = TEST_STUDENT_PROFILES[0]
        engine = AdvisingEngine(TEST_COURSES, fall_student, pd.DataFrame(TEST_POLICIES))
        engine.reset()
        engine.declare(StudentProfile(**fall_student))
        engine.run()
        
        fall_courses = [course["Course Code"] for course in engine.recommended_courses]
        assert "MAT111" in fall_courses  # Offered in FALL
        assert "CSE015" not in fall_courses  # Not offered in FALL

        # Test SPRING semester
        spring_student = TEST_STUDENT_PROFILES[1]
        engine = AdvisingEngine(TEST_COURSES, spring_student, pd.DataFrame(TEST_POLICIES))
        engine.reset()
        engine.declare(StudentProfile(**spring_student))
        engine.run()
        
        spring_courses = [course["Course Code"] for course in engine.recommended_courses]
        assert "CSE015" in spring_courses  # Offered in SPRING

if __name__ == '__main__':
    unittest.main() 