import unittest
import pandas as pd
from kbsEditor import validate_course
import tempfile
import os

class TestKBSEditor(unittest.TestCase):
    def setUp(self):
        # Create a temporary CSV file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.temp_dir, "test_courses.csv")
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

    def test_validate_course_valid_prereqs(self):
        """Test validation of valid prerequisites"""
        existing_codes = ["CSE101", "MAT101", "PHY101"]
        result = validate_course("CSE101,MAT101", existing_codes)
        self.assertEqual(result, [])

    def test_validate_course_invalid_prereqs(self):
        """Test validation of invalid prerequisites"""
        existing_codes = ["CSE101", "MAT101", "PHY101"]
        result = validate_course("CSE102,MAT102", existing_codes)
        self.assertEqual(set(result), {"CSE102", "MAT102"})

    def test_validate_course_empty_prereqs(self):
        """Test validation of empty prerequisites"""
        existing_codes = ["CSE101", "MAT101", "PHY101"]
        result = validate_course("", existing_codes)
        self.assertEqual(result, [])

    def test_validate_course_whitespace(self):
        """Test validation with whitespace in input"""
        existing_codes = ["CSE101", "MAT101", "PHY101"]
        result = validate_course(" CSE101 , MAT101 ", existing_codes)
        self.assertEqual(result, [])

    def test_validate_course_special_chars(self):
        """Test validation with special characters"""
        existing_codes = ["CSE101", "MAT101", "PHY101"]
        result = validate_course("CSE101;MAT101", existing_codes)
        self.assertEqual(result, ["CSE101;MAT101"])

    def test_validate_course_duplicate_prereqs(self):
        """Test validation with duplicate prerequisites"""
        existing_codes = ["CSE101", "MAT101", "PHY101"]
        result = validate_course("CSE101,CSE101", existing_codes)
        self.assertEqual(result, [])

    def test_validate_course_case_sensitivity(self):
        """Test validation with different case inputs"""
        existing_codes = ["CSE101", "MAT101", "PHY101"]
        result = validate_course("cse101,mat101", existing_codes)
        self.assertEqual(set(result), {"cse101", "mat101"})

    def test_validate_course_mixed_validity(self):
        """Test validation with mix of valid and invalid prerequisites"""
        existing_codes = ["CSE101", "MAT101", "PHY101"]
        result = validate_course("CSE101,INVALID101", existing_codes)
        self.assertEqual(result, ["INVALID101"])

    def test_validate_course_empty_existing_codes(self):
        """Test validation with empty existing codes list"""
        existing_codes = []
        result = validate_course("CSE101,MAT101", existing_codes)
        self.assertEqual(set(result), {"CSE101", "MAT101"})

    def test_validate_course_none_input(self):
        """Test validation with None input"""
        existing_codes = ["CSE101", "MAT101", "PHY101"]
        result = validate_course(None, existing_codes)
        self.assertEqual(result, [])

    def tearDown(self):
        # Clean up temporary files
        try:
            os.remove(self.test_csv)
            os.rmdir(self.temp_dir)
        except:
            pass

if __name__ == '__main__':
    unittest.main() 