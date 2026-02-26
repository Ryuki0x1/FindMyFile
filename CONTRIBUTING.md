# Contributing to FindMyPic

Thank you for your interest in contributing to FindMyPic! This document provides guidelines and instructions for contributing.

## 🎯 How Can I Contribute?

### Reporting Bugs
1. Check [existing issues](../../issues) to avoid duplicates
2. Use the [bug report template](../../issues/new?template=bug_report.md)
3. Provide detailed information:
   - System specs (OS, Python version, GPU)
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages or logs

### Suggesting Features
1. Check [existing feature requests](../../issues?q=label%3Aenhancement)
2. Use the [feature request template](../../issues/new?template=feature_request.md)
3. Explain the use case and benefit
4. Consider privacy implications (we're privacy-first!)

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

---

## 🛠️ Development Setup

### Prerequisites
- Python 3.10 or newer
- Node.js 18 or newer
- Git
- (Optional) NVIDIA GPU with CUDA support

### Initial Setup
```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/FindMyPic.git
cd FindMyPic

# Run setup
SETUP.bat

# Start development servers
start.bat
```

### Project Structure
```
FindMyPic/
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── ai/       # AI models (CLIP, FaceNet, OCR)
│   │   ├── core/     # Core logic
│   │   ├── db/       # Database layer
│   │   └── models/   # Data schemas
│   └── requirements.txt
│
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   └── services/
│   └── package.json
│
└── docs/            # Documentation
```

---

## 📝 Code Style

### Python (Backend)
- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes

```python
def search_files(
    query: str,
    n_results: int = 20,
) -> dict:
    """
    Search indexed files with natural language.
    
    Args:
        query: Search query string
        n_results: Maximum number of results to return
        
    Returns:
        dict: Search results with metadata
    """
    # Implementation
```

### TypeScript (Frontend)
- Use ESLint configuration
- Use TypeScript strict mode
- Use functional components with hooks
- Use meaningful variable names

```typescript
interface SearchFilters {
  fileType: string;
  folderPath: string;
  minScore: number;
}

export function SearchBar({ onResults }: SearchBarProps) {
  // Implementation
}
```

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add dark/light theme toggle
fix: resolve GPU detection issue on AMD cards
docs: update installation instructions
refactor: improve vector store performance
test: add tests for incremental indexing
```

---

## 🧪 Testing

### Running Tests
```bash
# Backend tests (when available)
cd backend
.venv\Scripts\python.exe -m pytest

# Frontend tests
cd frontend
npm test
```

### Testing Checklist
- [ ] Test on Windows 10/11
- [ ] Test with CPU version
- [ ] Test with GPU version (if applicable)
- [ ] Test all search modes (Visual, Face, OCR)
- [ ] Test with various file formats
- [ ] Test error handling
- [ ] Test edge cases

### Manual Testing
1. Index a folder with 100+ images
2. Test visual search with various queries
3. Test face search with uploaded photo
4. Test OCR with screenshots/receipts
5. Test filters (folder, min score, file type)
6. Test incremental indexing

---

## 🏗️ Architecture Guidelines

### Backend Principles
- **Lazy Loading:** Load AI models only when needed
- **Batch Processing:** Process files in optimized batches
- **Error Handling:** Gracefully handle errors, never crash
- **Privacy First:** No external API calls except model downloads
- **Performance:** Optimize for large photo libraries (50,000+)

### Frontend Principles
- **Responsive Design:** Work on all screen sizes
- **Accessibility:** Keyboard navigation, ARIA labels
- **Performance:** Virtual scrolling for large result sets
- **User Feedback:** Loading states, progress indicators
- **Offline First:** Work without internet after initial setup

### Privacy Guidelines
- ❌ **Never** send user data to external services
- ❌ **Never** add telemetry or analytics
- ❌ **Never** require internet after setup
- ✅ **Always** process data locally
- ✅ **Always** give users control over their data

---

## 📚 Adding New Features

### 1. Plan
- Open an issue to discuss the feature
- Get feedback from maintainers
- Consider privacy implications
- Plan implementation approach

### 2. Implement
- Create feature branch
- Write code with tests
- Update documentation
- Test thoroughly

### 3. Document
- Update README.md if needed
- Update CHANGELOG.md
- Add code comments
- Update API documentation

### 4. Submit
- Open Pull Request
- Fill out PR template completely
- Respond to review feedback
- Ensure CI passes (when available)

---

## 🎨 UI/UX Guidelines

### Design Principles
- **Dark Theme First:** Primary UI is dark theme
- **Glassmorphism:** Use backdrop blur and transparency
- **Smooth Animations:** 300ms transitions
- **Clear Feedback:** Loading states, success/error messages
- **Accessibility:** Proper contrast ratios, keyboard navigation

### Colors
```css
Primary: #7c3aed (Purple)
Secondary: #667eea (Blue)
Success: #10b981 (Green)
Error: #ef4444 (Red)
Background: #1a1a2e (Dark)
```

---

## 🐛 Debugging Tips

### Backend Issues
```bash
# Enable debug mode
cd backend
set DEBUG=1
.venv\Scripts\python.exe -m app.main
```

### Frontend Issues
```bash
# Check browser console
# Use React DevTools
# Check network tab for API calls
```

### Common Issues
1. **Import errors:** Check virtual environment is activated
2. **CUDA errors:** Verify GPU drivers installed
3. **Port conflicts:** Check ports 8000 and 5173 are free
4. **Model download fails:** Check internet connection

---

## 📖 Documentation

### What to Document
- New features
- API changes
- Configuration options
- Breaking changes
- Migration guides

### Where to Document
- **README.md:** User-facing features
- **Code comments:** Implementation details
- **CHANGELOG.md:** Version history
- **docs/:** Technical documentation

---

## 🤝 Code Review Process

### What Reviewers Look For
- Code quality and style
- Test coverage
- Documentation updates
- Performance implications
- Privacy considerations
- Breaking changes

### Response Time
- Bug fixes: 1-2 days
- Features: 3-7 days
- Documentation: 1-3 days

---

## 🎖️ Recognition

Contributors will be:
- Listed in CHANGELOG.md
- Mentioned in release notes
- Added to README.md contributors section (when we add one)
- Given credit in commit messages

---

## 📞 Getting Help

- **Questions:** Open a [Discussion](../../discussions)
- **Bug Reports:** Open an [Issue](../../issues/new?template=bug_report.md)
- **Feature Ideas:** Open a [Feature Request](../../issues/new?template=feature_request.md)
- **Pull Requests:** Use the [PR template](../../compare)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You!

Every contribution, no matter how small, helps make FindMyPic better for everyone. Thank you for being part of this project!

**Happy Coding! 🚀**
