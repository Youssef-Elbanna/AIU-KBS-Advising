import unittest
import pandas as pd
from usrInteractModule import validate_cgpa, get_semester_options, load_courses
from datetime import datetime
import tempfile
import os
import shutil

class TestUserInteraction(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.temp_dir, "courses.csv")
        self.test_data = {
            "Course Code": ["CSE101", "MAT101", "PHY101"],
            "Course Name": ["Intro to CS", "Basic Math", "Physics I"],
            "Description": ["CS Basics", "Math Basics", "Physics Basics"],
            "Prerequisites": ["", "CSE101", "MAT101"],
            "Co-requisites": ["", "", ""],
            "Credit Hours": [3, 3, 4],
            "Semester Offered": ["FALL", "SPRING", "FALL"]
        }
        pd.DataFrame(self.test_data).to_csv(self.test_csv, index=False)
        
        # Store the original courses.csv path if it exists
        self.original_courses_csv = None
        if os.path.exists('courses.csv'):
            self.original_courses_csv = 'courses.csv'
            shutil.copy('courses.csv', 'courses.csv.bak')

    def test_validate_cgpa_valid(self):
        """Test CGPA validation with valid inputs"""
        test_cases = [
            (0.0, True),
            (2.5, True),
            (4.0, True),
            (3.75, True)
        ]
        for cgpa, expected in test_cases:
            result, error = validate_cgpa(cgpa)
            self.assertEqual(result, expected)
            self.assertIsNone(error)

    def test_validate_cgpa_invalid(self):
        """Test CGPA validation with invalid inputs"""
        test_cases = [
            (-1.0, False),
            (4.1, False),
            ("abc", False),
            (5.0, False)
        ]
        for cgpa, expected in test_cases:
            result, error = validate_cgpa(cgpa)
            self.assertEqual(result, expected)
            self.assertIsNotNone(error)

    def test_validate_cgpa_edge_cases(self):
        """Test CGPA validation with edge cases"""
        test_cases = [
            (None, False),
            ("", False),
            (" ", False),
            ("3.5.5", False),
            ("3,5", False)
        ]
        for cgpa, expected in test_cases:
            result, error = validate_cgpa(cgpa)
            self.assertEqual(result, expected)
            self.assertIsNotNone(error)

    def test_validate_cgpa_boundary_values(self):
        """Test CGPA validation with boundary values"""
        test_cases = [
            (-0.01, False),
            (0.0, True),
            (0.01, True),
            (3.99, True),
            (4.0, True),
            (4.01, False)
        ]
        for cgpa, expected in test_cases:
            result, error = validate_cgpa(cgpa)
            self.assertEqual(result, expected)
            self.assertEqual(error is None, expected)

    def test_get_semester_options(self):
        """Test semester options generation"""
        current_year = datetime.now().year
        expected_options = [
            f"Fall {current_year}",
            f"Spring {current_year}",
            f"Fall {current_year + 1}",
            f"Spring {current_year + 1}"
        ]
        options = get_semester_options()
        self.assertEqual(options, expected_options)

    def test_get_semester_options_order(self):
        """Test semester options are in correct order"""
        options = get_semester_options()
        # Verify Fall comes before Spring for each year
        for i in range(0, len(options), 2):
            self.assertTrue("Fall" in options[i])
            if i + 1 < len(options):
                self.assertTrue("Spring" in options[i + 1])

    def test_load_courses_success(self):
        """Test successful course loading"""
        # Temporarily set the working directory to the temp directory
        original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        try:
            df = load_courses()
            self.assertFalse(df.empty)
            self.assertEqual(len(df), 3)
            self.assertTrue("Course Code" in df.columns)
            # Verify all required columns are present
            required_columns = ["Course Code", "Course Name", "Description", 
                              "Prerequisites", "Co-requisites", "Credit Hours", 
                              "Semester Offered"]
            for col in required_columns:
                self.assertIn(col, df.columns)
        finally:
            os.chdir(original_dir)

    def test_load_courses_failure(self):
        """Test course loading with missing file"""
        # Remove courses.csv if it exists
        if os.path.exists('courses.csv'):
            os.remove('courses.csv')
        
        df = load_courses()
        self.assertTrue(df.empty)

    def test_load_courses_corrupted_file(self):
        """Test course loading with corrupted file"""
        # Create a corrupted CSV file
        with open(self.test_csv, 'w') as f:
            f.write("Invalid,CSV,Content\nNo,Header,Row")
        
        original_dir = os.getcwd()
        os.chdir(self.temp_dir)
        try:
            df = load_courses()
            # The function should return a DataFrame but log an error
            self.assertFalse(df.empty)  # DataFrame is created from corrupted file
            self.assertNotEqual(list(df.columns), ["Course Code", "Course Name", "Description",
                                                 "Prerequisites", "Co-requisites", "Credit Hours",
                                                 "Semester Offered"])  # Wrong columns
        finally:
            os.chdir(original_dir)

    def tearDown(self):
        # Clean up temporary files
        try:
            os.remove(self.test_csv)
            os.rmdir(self.temp_dir)
            
            # Restore original courses.csv if it existed
            if self.original_courses_csv and os.path.exists('courses.csv.bak'):
                shutil.move('courses.csv.bak', 'courses.csv')
        except:
            pass

if __name__ == '__main__':
    unittest.main() 