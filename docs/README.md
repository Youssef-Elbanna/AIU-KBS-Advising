# AIU Knowledge-Based Academic Advising System Documentation

## Project Overview

The AIU Knowledge-Based Academic Advising System is an intelligent system that helps students make informed decisions about their course selections. It uses expert system principles to recommend courses based on various factors including:

- Academic performance (CGPA)
- Course prerequisites and co-requisites
- Semester availability
- Credit hour limits
- Previous academic history

## System Components

### 1. Core Engine (`src/Inference_engine_KBS.py`)
- Implements the expert system logic using the Experta framework
- Handles course recommendation rules and policies
- Manages credit limits and prerequisites validation

### 2. User Interface (`src/usrInteractModule.py`)
- Streamlit-based web interface
- Handles user input collection
- Displays course recommendations
- Provides explanations for decisions

### 3. Course Management (`src/kbsEditor.py`)
- Interface for managing course data
- Supports CRUD operations on courses
- Validates course relationships

### 4. Data Management (`src/integration/data_manager.py`)
- Handles data validation and processing
- Manages data persistence
- Ensures data integrity

### 5. Utility Modules
- `src/frozendict_patch.py`: Provides support for frozen dictionaries

## Data Files

### Course Database (`data/courses.csv`)
Contains information about all available courses:
- Course Code
- Course Name
- Description
- Prerequisites
- Co-requisites
- Credit Hours
- Semester Availability

### Academic Policies (`data/policies.csv`)
Defines academic rules and policies:
- Credit hour limits based on CGPA
- Other academic regulations

## Testing

The system includes comprehensive test coverage:
- Integration tests
- Component-specific tests
- Edge case handling

Run tests using:
```bash
python run_tests.py
```

## Development Guidelines

1. Code Organization
   - Keep business logic in the core engine
   - Maintain separation of concerns
   - Follow modular design principles

2. Testing
   - Write tests for new features
   - Maintain test coverage above 70%
   - Test edge cases and error conditions

3. Data Management
   - Use consistent data formats
   - Validate data integrity
   - Handle errors gracefully

4. User Interface
   - Follow Streamlit best practices
   - Provide clear user feedback
   - Maintain responsive design 