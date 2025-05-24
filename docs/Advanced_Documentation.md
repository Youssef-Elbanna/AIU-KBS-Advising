# AIU Knowledge-Based Academic Advising System
## Advanced Documentation

### Table of Contents
1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Technical Implementation](#technical-implementation)
4. [Knowledge Base Design](#knowledge-base-design)
5. [User Interface](#user-interface)
6. [Testing and Validation](#testing-and-validation)
7. [Deployment Guide](#deployment-guide)
8. [Maintenance and Support](#maintenance-and-support)

## Executive Summary

The AIU Knowledge-Based Academic Advising System is an intelligent advisory system designed to assist students in course selection and academic planning. The system implements expert system principles using the Experta framework and provides a modern web interface using Streamlit.

### Key Features
- Intelligent course recommendations based on student profiles
- Dynamic credit limit calculation based on CGPA
- Prerequisite and co-requisite validation
- Semester-specific course offerings
- Interactive course management system
- Comprehensive explanation of decisions

### Target Users
- Students: For course selection and academic planning
- Academic Advisors: For monitoring and validating recommendations
- Administrative Staff: For managing course data and policies

## System Architecture

### Component Overview
1. **Core Engine (`Inference_engine_KBS.py`)**
   - Expert system implementation using Experta
   - Rule-based inference engine
   - Dynamic credit limit calculation
   - Course recommendation logic

2. **Data Management Layer (`data_manager.py`)**
   - Data validation and processing
   - Course and policy data handling
   - Data integrity checks
   - Error handling mechanisms

3. **User Interface Components**
   - Student Interface (`usrInteractModule.py`)
   - Course Management Interface (`kbsEditor.py`)
   - Web-based interface using Streamlit

4. **Knowledge Base**
   - Course Database (`courses.csv`)
   - Academic Policies (`policies.csv`)
   - Relationship Management

### Data Flow
```
[User Input] → [Validation Layer] → [Inference Engine] → [Knowledge Base] → [Recommendation Engine] → [User Interface]
```

## Technical Implementation

### Core Engine Implementation
```python
class AdvisingEngine(KnowledgeEngine):
    def __init__(self, courses, student_data, policies_df):
        self.courses = courses
        self.student_data = student_data
        self.policies_df = policies_df
        self.credit_limit = self.get_dynamic_credit_limit()
```

### Key Algorithms
1. **Credit Limit Calculation**
   - Dynamic calculation based on CGPA
   - Policy-based restrictions
   - Semester-specific limits

2. **Course Recommendation**
   - Prerequisite validation
   - Co-requisite checking
   - Semester availability
   - Credit hour optimization

3. **Data Validation**
   - Input sanitization
   - Data integrity checks
   - Error handling

## Knowledge Base Design

### Course Database Schema
- Course Code (Primary Key)
- Course Name
- Description
- Prerequisites
- Co-requisites
- Credit Hours
- Semester Offered

### Academic Policies
1. **Credit Limit Rules**
   - CGPA < 2.00: 12 credits
   - 2.00 ≤ CGPA < 3.00: 20 credits
   - CGPA ≥ 3.00: 22 credits

2. **Course Selection Rules**
   - Prerequisite validation
   - Co-requisite requirements
   - Semester restrictions

## User Interface

### Student Interface
1. **Input Components**
   - CGPA entry
   - Semester selection
   - Passed courses selection
   - Failed courses selection

2. **Output Components**
   - Recommended courses list
   - Credit hour summary
   - Decision explanations
   - Warning messages

### Course Management Interface
1. **CRUD Operations**
   - Add new courses
   - Edit existing courses
   - Delete courses
   - View course list

2. **Validation Features**
   - Course code uniqueness
   - Prerequisite existence
   - Credit hour validation
   - Required field checking

## Testing and Validation

### Test Coverage
- Overall coverage: 71%
- Component-specific coverage:
  - Inference Engine: 81%
  - Data Manager: 68%
  - KBS Editor: 21%
  - User Interface: 39%

### Test Categories
1. **Integration Tests**
   - Data loading validation
   - Engine initialization
   - Policy application
   - Recommendation accuracy

2. **Component Tests**
   - User interface functionality
   - Data validation
   - Error handling
   - Edge cases

3. **Performance Tests**
   - Response time
   - Memory usage
   - Concurrent users
   - Data load handling

## Deployment Guide

### System Requirements
- Python 3.x
- Required Packages:
  - Streamlit
  - Pandas
  - Experta
  - Pytest

### Installation Steps
1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Configure data files
5. Start application

### Configuration
```bash
# Environment Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Application Start
streamlit run src/usrInteractModule.py
```

## Maintenance and Support

### Regular Maintenance Tasks
1. Data Updates
   - Course catalog updates
   - Policy modifications
   - Prerequisite changes

2. System Updates
   - Package updates
   - Security patches
   - Performance optimization

### Troubleshooting Guide
1. Common Issues
   - Data loading errors
   - Validation failures
   - Interface issues

2. Resolution Steps
   - Error logging
   - Debug procedures
   - Recovery methods

### Support Resources
- Documentation
- Test Suites
- Error Logs
- Contact Information

## Future Enhancements
1. Planned Features
   - Machine learning integration
   - Advanced analytics
   - Mobile interface
   - API integration

2. Improvement Areas
   - Test coverage
   - User interface
   - Performance optimization
   - Data management 