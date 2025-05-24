import pandas as pd
import os
from typing import Dict, List, Optional

class DataManager:
    def __init__(self, test_mode=False):
        self.courses_df = None
        self.policies_df = None
        self.cyber_courses_df = None
        self.test_mode = test_mode
        self._load_data()

    def _load_data(self) -> None:
        """Load all necessary data files"""
        try:
            if self.test_mode:
                from tests.data.test_data import TEST_COURSES, TEST_POLICIES
                self.courses_df = pd.DataFrame(TEST_COURSES)
                self.policies_df = pd.DataFrame(TEST_POLICIES)
                self.cyber_courses_df = pd.DataFrame([])  # Empty DataFrame for testing
            else:
                self.courses_df = pd.read_csv("courses.csv", encoding='latin1')
                self.policies_df = pd.read_csv("policies.csv", encoding='latin1')
                self.cyber_courses_df = pd.read_csv("Cyber Security Courses.csv", encoding='latin1')
        except Exception as e:
            raise Exception(f"Error loading data files: {str(e)}")

    def get_course_info(self, course_code: str) -> Optional[Dict]:
        """Get detailed information about a specific course"""
        if self.courses_df is None:
            return None
        
        course = self.courses_df[self.courses_df['Course Code'] == course_code]
        if course.empty:
            return None
            
        return course.iloc[0].to_dict()

    def get_prerequisites(self, course_code: str) -> List[str]:
        """Get prerequisites for a course"""
        course = self.courses_df[self.courses_df["Course Code"] == course_code]
        if course.empty:
            return []
            
        prereqs = str(course.iloc[0]["Prerequisites"]).split(",")
        return [p.strip() for p in prereqs if p.strip()]

    def get_credit_limit(self, cgpa: float, semester: str) -> int:
        """Get credit hour limit based on CGPA"""
        credit_policies = self.policies_df[self.policies_df["Category"] == "Credit Limit"]
        for _, policy in credit_policies.iterrows():
            condition = str(policy["Condition"])
            if "≥" in condition:
                limit = float(condition.split("≥")[1].strip())
                if cgpa >= limit:
                    return int(policy["max"])
            elif "<" in condition:
                limit = float(condition.split("<")[1].strip())
                if cgpa < limit:
                    return int(policy["max"])
            elif "≤" in condition:
                parts = condition.split("≤")
                lower = float(parts[0].strip())
                upper = float(parts[2].strip())
                if lower <= cgpa < upper:
                    return int(policy["max"])
        return 12  # Default minimum

    def validate_course_selection(self, course_code: str, passed_courses: List[str], semester: str) -> Dict:
        """Validate if a course can be taken"""
        course = self.courses_df[self.courses_df["Course Code"] == course_code]
        if course.empty:
            return {"valid": False, "reason": f"Course {course_code} not found"}
            
        course = course.iloc[0]
        offered = str(course["Semester Offered"]).strip().upper()
        if semester.upper() not in offered and offered != "BOTH":
            return {"valid": False, "reason": f"Course {course_code} is not offered in {semester} semester"}
            
        prereqs = str(course["Prerequisites"]).split(",")
        prereqs = [p.strip() for p in prereqs if p.strip()]
        if any(p not in passed_courses for p in prereqs):
            missing = [p for p in prereqs if p not in passed_courses]
            return {"valid": False, "reason": f"Missing prerequisites: {', '.join(missing)}"}
            
        return {"valid": True, "reason": "Course can be taken"}

    def get_available_courses(self, passed_courses: List[str], semester: str, cgpa: float) -> List[Dict]:
        """Get available courses for a student based on their profile"""
        available = []
        for _, course in self.courses_df.iterrows():
            code = str(course["Course Code"]).strip()
            offered = str(course["Semester Offered"]).strip().upper()
            
            # Check semester availability
            if semester.upper() not in offered and offered != "BOTH":
                continue
                
            # Check prerequisites
            prereqs = str(course["Prerequisites"]).split(",")
            prereqs = [p.strip() for p in prereqs if p.strip()]
            if any(p not in passed_courses for p in prereqs):
                continue
                
            available.append(course.to_dict())
            
        return available 