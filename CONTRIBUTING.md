# 🤝 Contributing to AdiZenWorks Cybersecurity Toolkit

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)

---

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

---

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/adizenworks-toolkit.git
cd adizenworks-toolkit
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 4. Set Up Development Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8
```

---

## 💻 Development Process

### Project Structure

```
adizenworks-toolkit/
├── AdiZenWorks_Toolkit_BRANDED.py  # Main application
├── adizenports.py                   # Port scanner module
├── adizensecurity.py                # Security auditor module
├── adizenxss.py                     # XSS scanner module
├── adizensqli.py                    # SQL injection tester
├── adizenmapper.py                  # Network mapper
├── adizenhash.py                    # Hash generator
├── adizenheaders.py                 # Header inspector
├── adizenspider.py                  # Web spider
├── requirements.txt                 # Dependencies
├── README.md                        # Documentation
└── LICENSE                          # License file
```

### Adding a New Tool

1. Create new module file: `adizennew.py`
2. Implement tool class with standard interface
3. Add wrapper function for compatibility
4. Update main application to include new tool
5. Add tests
6. Update documentation

---

## 📝 Coding Standards

### Python Style Guide

Follow PEP 8 guidelines:

```python
# Good
def scan_ports(target, port_range):
    """Scan ports on target host."""
    results = {
        "target": target,
        "ports": port_range
    }
    return results

# Bad
def scanPorts(Target,portRange):
    results={"target":Target,"ports":portRange}
    return results
```

### Naming Conventions

- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Variables**: `snake_case`

### Documentation

All functions must have docstrings:

```python
def example_function(param1, param2):
    """
    Brief description of function.
    
    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2
    
    Returns:
        dict: Description of return value
    """
    pass
```

### Code Formatting

Use Black for automatic formatting:

```bash
black *.py
```

### Linting

Check code quality with flake8:

```bash
flake8 *.py --max-line-length=100
```

---

## 🧪 Testing

### Writing Tests

Create test files with `test_` prefix:

```python
# test_ports.py
import pytest
from adizenports import scan_ports

def test_scan_ports():
    results = scan_ports("127.0.0.1", "80")
    assert "target" in results
    assert results["target"] == "127.0.0.1"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest test_ports.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Test Coverage

Aim for at least 70% code coverage for new features.

---

## 🔄 Pull Request Process

### 1. Update Your Fork

```bash
git fetch upstream
git merge upstream/main
```

### 2. Make Your Changes

- Write clean, documented code
- Follow coding standards
- Add tests for new features
- Update documentation

### 3. Commit Your Changes

```bash
git add .
git commit -m "feat: add new security tool"
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Create Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill out the PR template
5. Submit for review

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added and passing
- [ ] Dependent changes merged

---

## 🐛 Bug Reports

### Before Submitting

1. Check existing issues
2. Verify bug on latest version
3. Collect relevant information

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the issue

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen

**Screenshots**
If applicable

**Environment:**
- OS: [e.g., Windows 10]
- Python Version: [e.g., 3.12]
- Toolkit Version: [e.g., 2.0.1]

**Additional context**
Any other relevant information
```

---

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of desired feature

**Describe alternatives considered**
Other solutions you've considered

**Additional context**
Mockups, examples, etc.
```

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Eligible for special badges

---

## 📞 Questions?

- **GitHub Discussions**: For general questions
- **Email**: contribute@adizenworks.com
- **Discord**: [Join our community](#)

---

<div align="center">

**Thank you for contributing to AdiZenWorks! 🛡️**

Together, we're securing digital futures.

[Back to README](README.md)

© 2026 AdiZenWorks Inc.

</div>
