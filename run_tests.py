import pytest
import sys
import os

def main():
    """Run all tests and generate coverage report"""
    # Add the project root and src directory to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, 'src')
    sys.path.insert(0, project_root)
    sys.path.insert(0, src_path)

    # Run tests with coverage
    pytest.main([
        'tests/test_integration.py',
        'tests/test_kbs_editor.py',
        'tests/test_user_interaction.py',
        '-v',
        '--cov=src',
        '--cov-report=term-missing',
        '--cov-report=html'
    ])

if __name__ == '__main__':
    main() 