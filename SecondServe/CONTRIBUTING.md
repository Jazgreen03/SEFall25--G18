# Contributing to SecondServe

Thank you for your interest in contributing to SecondServe! We welcome contributions from the community to help improve this food donation and delivery platform.

## Getting Started

### Prerequisites
Before contributing, ensure you have:
- Docker and Docker Compose installed
- Node.js (v18+) for frontend development
- Python (v3.11+) for backend development
- Familiarity with Angular, Django, and MongoDB

### Development Setup

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/SecondServe.git
   cd SecondServe
   ```
2. **Set Up Environment**
```bash
cp env.template .env
# Edit .env with your configuration
```
3. **Start Development Environment**
```bash
docker compose up --build
```
## Contribution Workflow
1. **Create a Feature Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```
2. **Make Your Changes**
* Follow existing code style and patterns
* Write clear, descriptive commit messages
* Include tests for new functionality
* Update documentation as needed

3. **Testing Requirements**
**Backend Testing**
```bash
cd backend
pytest --cov
```
**Frontend Testing**
```bash
cd frontend/web
npm run test:coverage
```

4. **Documentation Updates**
Update relevant documentation:
* Code comments using JSDoc/TypeDoc for frontend
* Docstrings for backend Python code
* README.md for significant changes
* API documentation if endpoints are modified

5. **Submit Pull Request**
1. Push your branch: ```git push origin feature/your-feature-name```
2. Create a Pull Request against the main repository
3. Fill out the PR template with:
    * Description of changes
    * Testing performed
    * Screenshots (for UI changes)
    * Related issue numbers

## Code Standards
### Frontend (Angular)
* Use TypeScript strict mode
* Follow Angular style guide
* Use reactive forms over template-driven forms
* Implement proper error handling
* Write component documentation

### Backend (Django)
* Follow Django best practices
* Use Django REST Framework for APIs
* Write comprehensive tests
* Include proper validation and error handling
* Use environment variables for configuration

### General Guidelines
* Write clear, self-documenting code
* Keep functions small and focused
* Use meaningful variable names
* Comment complex logic
* Follow existing project structure

## Issue Reporting
When reporting issues, please include:
* Clear description of the problem
* Steps to reproduce
* Expected vs actual behavior
* Environment details
* Screenshots (if applicable)

## Feature Requests
We welcome feature requests! Please:
1. Check if the feature already exists
2. Explain the problem it solves
3. Describe your proposed solution
4. Include any relevant examples

## Review Process
1. Automated Checks: PRs must pass:
    * All tests
    * Code coverage requirements
    * Linting checks
2. Code Review: At least one maintainer must approve
3. Merge: After approval, maintainers will merge

## Areas Needing Contribution
### High Priority
* Admin pages
* Map integration for deliveries
* Enhanced order tracking
* Performance optimizations

### Documentation
* Tutorials and guides
* API documentation improvements
* Deployment guides

### Testing
* Additional test coverage
* Integration tests
* Performance testing

## Communication
* Use GitHub issues for bug reports and feature requests
* Keep discussions professional and respectful
* Ask questions if you're unsure about implementation

## Recognition
Contributors will be:
* Listed in our CONTRIBUTORS.md file
* Recognized in release notes
* Credited for significant contributions

## Code of Conduct
We expect all contributors to:
* Be respectful and inclusive
* Provide constructive feedback
* Help create a welcoming environment
* Follow the project's coding standards

Violations of the code of conduct may result in removal from the project.

### Getting Help
* Check existing documentation
* Review closed issues for similar problems
* Ask questions in GitHub discussions
* Contact maintainers for complex issues

Thank you for contributing to SecondServe! Your efforts help reduce food waste and support communities. 🥫

---

*Note: This project follows the MIT License. By contributing, you agree that your contributions will be licensed under the same license.*