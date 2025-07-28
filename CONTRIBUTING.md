# Contributing to Bug Bounty Automation Tools

Thank you for your interest in contributing to this project! 

## How to Contribute

1. **Fork the Repository**
   - Click the "Fork" button at the top right of this repository

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/bugbounty.git
   cd bugbounty
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation if needed

5. **Test Your Changes**
   ```bash
   python app.py
   # Test all features in the web interface
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

7. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

- Use meaningful variable names
- Keep functions focused and small
- Add error handling for external tool calls
- Validate all user inputs
- Follow Python PEP 8 style guide

## Bug Reports

If you find a bug, please create an issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)

## Feature Requests

For new features:
- Check if the feature aligns with the project goals
- Describe the use case
- Consider security implications
- Ensure it doesn't break existing functionality

## Security

If you discover a security vulnerability, please email the maintainers directly rather than creating a public issue.
