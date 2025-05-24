# AIU Knowledge-Based Academic Advising System
## Final Report

### Project Information
**Project Title:** AIU Knowledge-Based Academic Advising System  
**Course:** AIE212 - Knowledge-based Systems  
**Institution:** Alamein International University, Faculty of Computer Science & Engineering

**Team Members and Roles:**
- [Student Name 1] - Knowledge Base Design & Rule Implementation
- [Student Name 2] - Inference Engine & Testing
- [Student Name 3] - User Interface & Documentation
- [Student Name 4] - Integration & Quality Assurance

### Application Description

#### System Overview
The AIU Knowledge-Based Academic Advising System is an intelligent advisory system that assists students in course selection and academic planning. The system uses expert system principles to provide personalized course recommendations based on:
- Academic performance (CGPA)
- Completed courses
- Failed courses
- Semester availability
- Prerequisites and co-requisites
- Credit hour limits

#### Domain Model
The system models the academic advising domain through:
1. Course Relationships
   - Prerequisites
   - Co-requisites
   - Credit hours
   - Semester offerings

2. Academic Policies
   - CGPA-based credit limits
   - Course retake rules
   - Semester restrictions

### Rules Implementation

#### 1. Credit Limit Rules
```python
def get_dynamic_credit_limit(self):
    credit_policies = self.policies_df[self.policies_df["Category"].str.strip() == "Credit Limit"]
    rules = []

    for _, row in credit_policies.iterrows():
        condition = str(row["Condition"])
        max_credit = int(row["max"])
        match = re.findall(r'(\d+\.\d+)', condition)

        if "≥" in condition or ">=" in condition:
            rules.append((lambda cgpa, val=float(match[0]): cgpa >= val, max_credit))
        elif "≤" in condition and len(match) == 2:
            l, u = float(match[0]), float(match[1])
            rules.append((lambda cgpa, l=l, u=u: l <= cgpa < u, max_credit))
        elif "<" in condition:
            rules.append((lambda cgpa, val=float(match[0]): cgpa < val, max_credit))

    for rule, limit in rules:
        if rule(self.student_data["cgpa"]):
            return limit
    return 12  # Default fallback
```

**Example:**
- Student with CGPA 3.5 → Credit limit: 22 hours
- Student with CGPA 2.5 → Credit limit: 20 hours
- Student with CGPA 1.8 → Credit limit: 12 hours

#### 2. Prerequisite Validation Rules
```python
def validate_prerequisites(self, course_code, passed_courses):
    course = self.get_course_info(course_code)
    if not course:
        return False, "Course not found"
    
    prereqs = [p.strip() for p in str(course["Prerequisites"]).split(",") if p.strip()]
    missing = [p for p in prereqs if p not in passed_courses]
    
    if missing:
        return False, f"Missing prerequisites: {', '.join(missing)}"
    return True, None
```

**Example:**
- Course: CSE015 (OOP)
  - Prerequisite: CSE014
  - If CSE014 not in passed_courses → Cannot take CSE015
  - Explanation generated: "CSE015 is not recommended due to unmet prerequisite: CSE014"

#### 3. Course Offering Rules
```python
def validate_semester_offering(self, course_code, semester):
    course = self.get_course_info(course_code)
    offered = str(course["Semester Offered"]).strip().upper()
    
    if semester.upper() not in offered and offered != "BOTH":
        return False, f"{course_code} is only offered in {offered} semester"
    return True, None
```

**Example:**
- MAT111 offered in FALL
  - If current semester = SPRING → Course not available
  - Explanation: "MAT111 is not offered in SPRING semester"

#### 4. Failed Course Priority Rules
```python
def process_failed_courses(self):
    for course in self.courses:
        code = str(course["Course Code"]).strip()
        if code in self.student_data["failed_courses"]:
            valid_prereqs, _ = self.validate_prerequisites(code, self.student_data["passed_courses"])
            valid_semester, _ = self.validate_semester_offering(code, self.student_data["semester"])
            
            if valid_prereqs and valid_semester:
                if self.total_credits + course["Credit Hours"] <= self.credit_limit:
                    self.recommended_courses.append(course)
                    self.total_credits += course["Credit Hours"]
                    self.explanations.append(
                        f"{code} is prioritized because you failed it previously and met its prerequisites"
                    )
```

**Example:**
- Student failed CSE014
  - No prerequisites → Can retake immediately
  - Explanation: "CSE014 is prioritized for retaking"
- Student failed CSE015
  - Has prerequisite CSE014
  - If CSE014 not passed → Cannot retake yet

### Knowledge Base

#### Content Structure
1. **Course Database (`courses.csv`)**
   ```csv
   Course Code,Course Name,Description,Prerequisites,Co-requisites,Credit Hours,Semester Offered
   MAT111,Mathematics I,"The calculus part covers functions, Properties of functions",,3,FALL
   CSE014,Structured Programming,"Primitive data types, control structures",,3,FALL
   CSE015,Object Oriented Programming,"Classes, inheritance, polymorphism",CSE014,,3,SPRING
   CSE111,Data Structures,"Arrays, linked lists, trees",CSE015,,3,FALL
   ```

2. **Academic Policies (`policies.csv`)**
   ```csv
   Category,Condition,max,Policy Description
   Credit Limit,CGPA < 2.00,12,"Fall, Spring"
   Credit Limit,2.00 ≤ CGPA < 3.00,20,"Fall, Spring"
   Credit Limit,CGPA ≥ 3.00,22,"Fall, Spring"
   Credit Limit,Summer Semester,9,Summer
   ```

#### Editor Functionality
1. **Course Management Interface**
   ```python
   def add_course(self, course_data):
       # Validate course data
       if not self.validate_course_data(course_data):
           return False, "Invalid course data"
           
       # Check for existing course
       if course_data["code"] in self.courses:
           return False, "Course already exists"
           
       # Validate prerequisites
       if not self.validate_prerequisites(course_data["prerequisites"]):
           return False, "Invalid prerequisites"
           
       # Add course to database
       self.courses[course_data["code"]] = course_data
       return True, "Course added successfully"
   ```

2. **Data Validation Rules**
   ```python
   def validate_course_data(self, data):
       required_fields = ["code", "name", "credits", "semester"]
       if not all(field in data for field in required_fields):
           return False
           
       if not (0 < data["credits"] <= 4):
           return False
           
       if data["semester"] not in ["FALL", "SPRING", "BOTH"]:
           return False
           
       return True
   ```

### Inference Engine

#### Core Components

1. **Fact Model**
   ```python
   class StudentProfile(Fact):
       """Student academic profile fact"""
       pass

   class Course(Fact):
       """Course information fact"""
       pass

   class AcademicPolicy(Fact):
       """Academic policy fact"""
       pass
   ```

2. **Rule Definitions**
   ```python
   @Rule(
       StudentProfile(cgpa=MATCH.cgpa),
       AcademicPolicy(
           category="Credit Limit",
           condition=MATCH.condition,
           max_credits=MATCH.limit
       )
   )
   def apply_credit_limit(self, cgpa, condition, limit):
       """Apply credit limit based on CGPA"""
       if eval(condition.replace("CGPA", str(cgpa))):
           self.credit_limit = limit
           self.explanations.append(
               f"Credit limit set to {limit} based on CGPA of {cgpa}"
           )
   ```

3. **Recommendation Logic**
   ```python
   def generate_recommendations(self):
       """Main recommendation generation process"""
       self.process_failed_courses()  # Priority 1
       self.process_required_courses()  # Priority 2
       self.process_elective_courses()  # Priority 3
       
       if not self.recommended_courses:
           self.explanations.append(
               "No courses could be recommended based on your profile"
           )
   ```

#### Decision Making Process

1. **Course Eligibility Check**
   ```python
   def is_course_eligible(self, course, student_profile):
       checks = [
           self.check_prerequisites(course, student_profile),
           self.check_semester_offering(course, student_profile),
           self.check_credit_limit(course),
           self.check_course_history(course, student_profile)
       ]
       return all(check[0] for check in checks)
   ```

2. **Recommendation Prioritization**
   ```python
   def prioritize_courses(self, eligible_courses):
       priority_order = [
           self.get_failed_courses,
           self.get_required_courses,
           self.get_elective_courses
       ]
       
       recommended = []
       for get_courses in priority_order:
           courses = get_courses(eligible_courses)
           if self.can_add_courses(courses):
               recommended.extend(courses)
       return recommended
   ```

3. **Explanation Generation**
   ```python
   def generate_explanation(self, course, status, reason=None):
       if status == "recommended":
           return f"{course.code} is recommended because {reason}"
       elif status == "rejected":
           return f"{course.code} cannot be taken because {reason}"
       elif status == "warning":
           return f"Warning for {course.code}: {reason}"
   ```

### User Interaction

#### Input Interface
![Student Input Form](path_to_screenshot1.png)
- CGPA entry with validation
- Semester selection dropdown
- Multi-select for passed courses
- Multi-select for failed courses

#### Output Display
![Recommendations Display](path_to_screenshot2.png)
- Recommended courses table
- Credit hour summary
- Decision explanations
- Warning messages

### Explanation System

#### Generation Process
1. **Rule-Based Explanations**
   ```python
   self.explanations.append(f"{code} is recommended because you passed {prereqs}")
   self.explanations.append(f"{code} is not added due to credit limit")
   ```

2. **Display Format**
   - Clear, natural language explanations
   - Context-specific reasoning
   - User-friendly formatting

### Streamlit Interface

#### Design Features
1. **Main Dashboard**
   - Clean, intuitive layout
   - Responsive design
   - Error handling
   - Real-time updates

2. **Course Management**
   - Interactive forms
   - Data validation
   - Success/error messages
   - Tabular data display

#### Implementation
```python
def main():
    st.title("Course Recommendation System")
    col1, col2 = st.columns(2)
    with col1:
        semester = st.selectbox("Select Semester", options)
        cgpa = st.number_input("Enter CGPA", 0.0, 4.0)
```

### GitHub Collaboration

#### Workflow
1. **Branch Strategy**
   - main: Production-ready code
   - develop: Integration branch
   - feature/*: Individual features
   - hotfix/*: Emergency fixes

2. **Code Review Process**
   - Pull request reviews
   - Code quality checks
   - Test coverage validation

#### Repository Structure
```
AIU-KBS-Advising/
├── src/
│   ├── Inference_engine_KBS.py
│   ├── kbsEditor.py
│   └── usrInteractModule.py
├── data/
│   ├── courses.csv
│   └── policies.csv
├── tests/
└── docs/
```

### Testing and Quality Assurance

#### Test Coverage
- Overall: 71%
- Core Components:
  - Inference Engine: 81%
  - Data Manager: 68%
  - KBS Editor: 21%
  - User Interface: 39%

#### Validation Results
1. **Integration Tests**
   - Data flow validation
   - Rule application
   - Policy enforcement

2. **User Interface Tests**
   - Input validation
   - Error handling
   - Response accuracy

### Future Enhancements

1. **Planned Features**
   - Machine learning integration
   - Mobile interface
   - Advanced analytics
   - API integration

2. **Improvement Areas**
   - Test coverage
   - User interface
   - Performance optimization
   - Data management

### Repository Link
[AIU-KBS-Advising GitHub Repository](https://github.com/yourusername/AIU-KBS-Advising)

### Video Demonstration
[Link to 5-minute demonstration video](video_url)
- System launch
- Sample data entry
- Recommendation display
- Edge case handling 

### User Interface

#### Student Dashboard Implementation
```python
def create_student_dashboard():
    st.set_page_config(
        page_title="Course Recommendation System",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("Course Recommendation System")
    
    # Create two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        semester = st.selectbox(
            "Select Current Semester",
            options=get_semester_options(),
            help="Choose your current semester"
        )

        cgpa = st.number_input(
            "Enter CGPA",
            min_value=0.0,
            max_value=4.0,
            step=0.01,
            format="%.2f",
            help="Enter your CGPA (0.0-4.0)"
        )

    with col2:
        passed_courses = st.multiselect(
            "Select Passed Courses",
            options=get_available_courses(),
            help="Select all courses you have passed"
        )

        failed_courses = st.multiselect(
            "Select Failed Courses",
            options=[c for c in get_available_courses() if c not in passed_courses],
            help="Select all courses you have failed"
        )
```

#### Course Management Interface
```python
def create_course_editor():
    st.markdown("""
        <style>
        .main { padding: 2rem; }
        .stButton { margin: 1rem 0; }
        .warning { color: #ff4b4b; }
        </style>
    """, unsafe_allow_html=True)

    st.title("Course Management System")
    
    action = st.sidebar.radio(
        "Choose Action",
        ["View Courses", "Add Course", "Edit Course", "Delete Course"]
    )

    if action == "Add Course":
        with st.form("add_course_form"):
            code = st.text_input("Course Code").strip().upper()
            name = st.text_input("Course Name")
            credits = st.number_input("Credit Hours", 1, 4)
            prereqs = st.multiselect("Prerequisites", get_available_courses())
            submit = st.form_submit_button("Add Course")
```

#### Data Visualization
```python
def display_recommendations(recommendations):
    st.success("Here are your recommended courses:")
    
    # Create DataFrame for display
    df = pd.DataFrame(recommendations)
    df = df[["Course Code", "Course Name", "Credit Hours"]]
    
    # Display course table
    st.dataframe(
        df.style.highlight_max("Credit Hours"),
        use_container_width=True
    )
    
    # Display credit summary
    total_credits = df["Credit Hours"].sum()
    st.metric(
        "Total Credits",
        f"{total_credits} hours",
        delta=f"{22 - total_credits} remaining"
    )
```

### Testing and Validation

#### Unit Tests
```python
class TestAdvisingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AdvisingEngine(TEST_COURSES, TEST_POLICIES)
        
    def test_credit_limit_calculation(self):
        """Test credit limit calculation based on CGPA"""
        test_cases = [
            (3.5, 22),  # High CGPA
            (2.5, 20),  # Medium CGPA
            (1.8, 12),  # Low CGPA
        ]
        
        for cgpa, expected_limit in test_cases:
            with self.subTest(cgpa=cgpa):
                self.engine.student_data["cgpa"] = cgpa
                self.assertEqual(
                    self.engine.get_dynamic_credit_limit(),
                    expected_limit
                )
                
    def test_prerequisite_validation(self):
        """Test prerequisite validation logic"""
        test_cases = [
            (
                "CSE015",
                ["CSE014"],
                True,
                "Prerequisites met"
            ),
            (
                "CSE015",
                [],
                False,
                "Missing prerequisite: CSE014"
            ),
        ]
        
        for course, passed, expected, message in test_cases:
            with self.subTest(course=course):
                result = self.engine.validate_prerequisites(course, passed)
                self.assertEqual(result[0], expected, message)
```

#### Integration Tests
```python
def test_full_recommendation_flow():
    """Test complete recommendation workflow"""
    # Setup test data
    student_data = {
        "cgpa": 3.0,
        "semester": "FALL",
        "passed_courses": ["CSE014"],
        "failed_courses": []
    }
    
    # Initialize engine
    engine = AdvisingEngine(TEST_COURSES, student_data, TEST_POLICIES)
    engine.reset()
    engine.declare(StudentProfile(**student_data))
    engine.run()
    
    # Verify recommendations
    assert len(engine.recommended_courses) > 0
    assert any(
        course["Course Code"] == "CSE015"
        for course in engine.recommended_courses
    )
    assert engine.total_credits <= engine.credit_limit
```

#### Performance Testing
```python
def test_system_performance():
    """Test system performance with large datasets"""
    start_time = time.time()
    
    # Load test data
    large_course_set = generate_test_courses(1000)
    student_data = generate_test_profile()
    
    # Run recommendation engine
    engine = AdvisingEngine(large_course_set, student_data, TEST_POLICIES)
    engine.reset()
    engine.declare(StudentProfile(**student_data))
    engine.run()
    
    # Assert performance requirements
    execution_time = time.time() - start_time
    assert execution_time < 2.0  # Should complete within 2 seconds
    assert engine.total_credits <= engine.credit_limit
``` 