# OCR Receipt Scanner

A modern, cross-platform receipt scanning application that uses OCR and AI to extract and analyze spending data from receipts.

## Features

- **Multi-format Support**: Upload images (JPG, PNG) or PDFs of receipts
- **OCR Processing**: Extract text using Tesseract and EasyOCR
- **AI Parsing**: Intelligent parsing of receipt data using Ollama LLM
- **Database Storage**: SQLite database with advanced analytics
- **Interactive Dashboard**: Streamlit UI with real-time visualization
- **Export Options**: CSV, Excel, and JSON export
- **Cross-platform**: Desktop demo with mobile-ready architecture

## Live Demo

The application is deployed on Streamlit Share: [OCR Receipt Scanner Demo](https://share.streamlit.io/your-username/ocr-receipt-scanner)

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ocr-receipt-scanner.git
   cd ocr-receipt-scanner
   ```

2. Install system dependencies:
   ```bash
   # macOS
   brew install tesseract
   
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run streamlit_app_deploy.py
   ```

## Project Structure

```
ocr_receipt_scanner/
├── streamlit_app_deploy.py      # Main Streamlit application
├── requirements.txt             # Python dependencies
├── .streamlit/                  # Streamlit configuration
│   └── config.toml
├── src/                         # Source code
│   ├── ocr/                     # OCR engine components
│   ├── ai/                      # AI parsing components
│   ├── database/                # Database layer
│   └── ui/                      # UI components
├── samples/                     # Sample receipt images
├── data/                        # Data storage
└── tests/                       # Test files
```

## Usage

1. **Upload Receipts**: Use the "Upload & Scan" page to upload receipt images or PDFs
2. **Process**: Click "Process Receipts" to extract data
3. **View Dashboard**: See spending metrics and recent receipts
4. **Analyze**: Use the Analytics page for spending trends and patterns
5. **Export**: Download your data in CSV, Excel, or JSON format

## Technology Stack

- **Frontend**: Streamlit, Plotly, Pandas
- **OCR**: Tesseract, EasyOCR, OpenCV
- **AI**: Ollama (LLM integration)
- **Database**: SQLite
- **Image Processing**: Pillow, scikit-image

## Development

The project was developed using an agent-based approach:

1. **Agent 1**: OCR Engine (Tesseract + EasyOCR integration)
2. **Agent 2**: AI Parser (Ollama LLM with rule-based fallback)
3. **Agent 3**: Database Layer (SQLite with analytics)
4. **Agent 4**: UI Layer (Streamlit dashboard)
5. **Agent 5**: Integration & Testing

## License

MIT License

## Author

Developed as part of an AI assistant project.