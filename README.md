# AIU Knowledge-Based Academic Advising System

A Knowledge-Based System (KBS) for academic advising at AIU, built with Python, Streamlit, and Expert Systems principles.

## Features

- Course recommendation based on student profile
- CGPA-based credit limit calculation
- Prerequisite and co-requisite validation
- Semester-specific course offerings
- Course management system (Add/Edit/Delete courses)
- Interactive web interface

## Project Structure

```
AIU-KBS-Advising/
├── src/
│   ├── integration/
│   │   └── data_manager.py      # Data management and validation
│   ├── Inference_engine_KBS.py  # Core KBS engine
│   ├── kbsEditor.py            # Course management interface
│   ├── usrInteractModule.py    # User interaction module
│   └── frozendict_patch.py     # Utility module
├── data/
│   ├── courses.csv            # Course database
│   └── policies.csv          # Academic policies
├── tests/
│   ├── conftest.py          # Test configurations
│   ├── test_integration.py  # Integration tests
│   ├── test_kbs_editor.py   # KBS Editor tests
│   └── test_user_interaction.py # User interaction tests
├── docs/                    # Documentation
├── run_tests.py           # Test runner
└── requirements.txt       # Project dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AIU-KBS-Advising.git
cd AIU-KBS-Advising
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run src/usrInteractModule.py
```

2. Access the application in your web browser (typically http://localhost:8501)

3. Enter your academic information:
   - Current CGPA
   - Semester
   - Passed courses
   - Failed courses

4. Get personalized course recommendations

## Testing

Run the test suite:
```bash
python run_tests.py
```

Current test coverage: 71%
- Integration tests: 27 tests
- Component-specific tests
- Edge case handling

## Dependencies

- Python 3.x
- Streamlit
- Pandas
- Experta (Expert System framework)
- Pytest (for testing)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- AIU Faculty and Staff
- Expert Systems Community
- Open Source Contributors