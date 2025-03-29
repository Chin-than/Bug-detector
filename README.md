# C Code Bug Detection and Fixing System

This system combines static analysis and machine learning to detect and fix bugs in C code. It uses a SQL database to store code samples and their associated bugs, and a neural network model to learn from past bug patterns.

## Features

- Static analysis of C code using AST parsing
- Machine learning-based bug detection
- Automated bug fixing suggestions
- SQL database for storing code samples and fixes
- Support for common C bugs: 
  - Memory leaks
  - Buffer overflows
  - Null pointer dereferences
  - Uninitialized variables
  - Infinite loops
  - Missing return statements
  - Syntax errors

## Requirements

- Python 3.8+
- SQLite3
- Required Python packages (install using `pip install -r requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bug-detector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. The system will automatically create the necessary database and model files on first run.

## Usage

1. Basic usage:
```python
from main import BugDetectionSystem

# Initialize the system
system = BugDetectionSystem()

# Analyze a C file
bugs = system.analyze_file("path/to/your/code.c")

# Get fixes for the file
fixes = system.get_fixes_for_file("path/to/your/code.c")
```

2. Command line usage:
```bash
python main.py
```

## Project Structure

- `database/`: Database-related code
  - `db_handler.py`: SQL database operations
  - `schema.sql`: Database schema
- `analyzer/`: Code analysis components
  - `c_analyzer.py`: C code static analysis
- `ml/`: Machine learning components
  - `bug_detector.py`: Neural network model for bug detection
- `main.py`: Main application entry point
- `requirements.txt`: Python dependencies

## Database Schema

The system uses three main tables:
1. `code_samples`: Stores C code files and their content
2. `bugs`: Stores detected bugs and their details
3. `fixes`: Stores suggested fixes for bugs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 