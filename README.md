# 🤖 Perplexity AI Automation Testing

A comprehensive automation testing framework for Perplexity AI mobile application using Appium, Flask, and semantic validation. This project provides automated testing capabilities with real-time reporting and a modern web interface.

## ✨ Features

- **Mobile App Automation**: Automated testing of Perplexity AI mobile application using Appium
- **Semantic Validation**: AI-powered response validation using BART model for semantic similarity
- **Real-time Web Interface**: Live test execution monitoring with Flask web application
- **Comprehensive Reporting**: Automated PDF report generation with pie charts and metrics
- **Excel Test Case Management**: Easy test case management using Excel files
- **Streaming Updates**: Real-time test progress updates via Server-Sent Events (SSE)

## 🏗️ Architecture

```
Automation_script/
├── app.py                 # Main Flask application
├── uploads/
│   └── main.py           # Core automation logic and validation
├── templates/
│   └── index.html        # Web interface for test monitoring
├── test_cases_.xlsx      # Test case definitions
├── perplexity.apk        # Android application package
└── README.md             # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Android SDK
- Appium Server
- Android device or emulator
- Perplexity AI APK file

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Automation_script
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Appium**
   ```bash
   npm install -g appium
   ```

4. **Start Appium Server**
   ```bash
   appium
   ```

5. **Connect Android device/emulator**
   - Enable USB debugging on your Android device
   - Or start an Android emulator

### Configuration

1. **Update test cases** in `test_cases_.xlsx`:
   - TestCaseID: Unique identifier for each test
   - Input: Text input for Perplexity AI
   - Expected Responses: Expected AI responses (separated by `||`)

2. **Update file paths** in `app.py` if needed:
   ```python
   multiple_file_path = "path/to/your/test_cases_.xlsx"
   ```

## 🧪 Running Tests

### Web Interface (Recommended)

1. **Start the Flask application**
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://localhost:5000`

3. **Click "Start Testing"** to begin automated test execution

4. **Monitor real-time progress** in the web interface

### Command Line

```bash
python uploads/main.py
```

## 📊 Test Results

The system automatically generates:

- **Real-time status updates** during test execution
- **Pass/Fail counts** with detailed metrics
- **PDF reports** with pie charts and statistics
- **Semantic similarity scores** for response validation

### Sample Report Metrics

- Total Test Cases
- Passed Cases Count
- Failed Cases Count
- Pass Rate
- Fail Rate

## 🔧 Customization

### Adding New Test Cases

1. Open `test_cases_.xlsx`
2. Add new rows with:
   - TestCaseID: Sequential numbering
   - Input: Your test input text
   - Expected Responses: Expected AI responses separated by `||`

### Modifying Validation Logic

Edit the `SemanticValidator` class in `uploads/main.py`:
- Adjust similarity threshold (currently 0.75)
- Change the BART model
- Modify validation criteria

### Customizing Reports

Modify the `prepare_pdf()` method in `uploads/main.py`:
- Change chart colors and styles
- Add custom metrics
- Modify PDF layout

## 🛠️ Technical Details

### Core Components

- **Flask Web App**: Provides web interface and streaming updates
- **Appium Driver**: Handles mobile app automation
- **SemanticValidator**: AI-powered response validation
- **PDF Generator**: Automated report creation with matplotlib

### Dependencies

- **Flask**: Web framework
- **Appium**: Mobile automation
- **Transformers**: BART model for semantic similarity
- **Pandas**: Excel file processing
- **Matplotlib**: Chart generation
- **FPDF**: PDF report creation

## 📱 Supported Platforms

- **Android**: Primary platform (APK-based)
- **iOS**: Can be extended with iOS capabilities
- **Web**: Web interface for monitoring and control

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Appium Connection Failed**
   - Ensure Appium server is running
   - Check device/emulator connection
   - Verify Android SDK setup

2. **APK Installation Failed**
   - Check APK file path
   - Ensure device has sufficient storage
   - Verify APK compatibility

3. **Semantic Validation Errors**
   - Check internet connection for model download
   - Verify expected response format
   - Adjust similarity threshold if needed

### Getting Help

- Check the [Issues](../../issues) page
- Review Appium documentation
- Verify Android SDK configuration

## 📈 Future Enhancements

- [ ] iOS platform support
- [ ] Cloud-based test execution
- [ ] Advanced analytics dashboard
- [ ] Integration with CI/CD pipelines
- [ ] Multi-language support
- [ ] Performance benchmarking

---

**Made with ❤️ for automated testing excellence**

*For questions and support, please open an issue in this repository.*
