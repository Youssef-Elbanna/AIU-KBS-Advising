TEST_COURSES = [
    {
        "Course Code": "MAT111",
        "Course Name": "Mathematics I",
        "Description": "The calculus part covers functions",
        "Prerequisites": "",
        "Co-requisites": "",
        "Credit Hours": 3,
        "Semester Offered": "FALL"
    },
    {
        "Course Code": "CSE014",
        "Course Name": "Structured Programming",
        "Description": "Introduction to programming",
        "Prerequisites": "",
        "Co-requisites": "",
        "Credit Hours": 3,
        "Semester Offered": "FALL"
    },
    {
        "Course Code": "CSE015",
        "Course Name": "Object Oriented Programming",
        "Description": "OOP concepts",
        "Prerequisites": "CSE014",
        "Co-requisites": "",
        "Credit Hours": 3,
        "Semester Offered": "SPRING"
    }
]

TEST_POLICIES = [
    {
        "Category": "Credit Limit",
        "Condition": "CGPA < 2.00",
        "max": 12,
        "Policy Description": "Fall, Spring"
    },
    {
        "Category": "Credit Limit",
        "Condition": "2.00 ≤ CGPA < 3.00",
        "max": 20,
        "Policy Description": "Fall, Spring"
    },
    {
        "Category": "Credit Limit",
        "Condition": "CGPA ≥ 3.00",
        "max": 22,
        "Policy Description": "Fall, Spring"
    }
]

TEST_STUDENT_PROFILES = [
    {
        "cgpa": 3.5,
        "semester": "FALL",
        "passed_courses": [],
        "failed_courses": []
    },
    {
        "cgpa": 3.0,
        "semester": "SPRING",
        "passed_courses": ["CSE014"],
        "failed_courses": []
    }
] 