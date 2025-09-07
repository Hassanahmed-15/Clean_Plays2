 # GPT-5 Macbeth Notes Processor

A comprehensive Python solution that uses GPT-5 API to process Shakespeare commentary notes with OCR bibliography extraction and PDF export.
   
## 🎯 What This Processor Does

1. **Extracts Bibliography**: Uses OCR to read all bibliography entries from 5 PNG image files (Capture.PNG through Capture5.PNG)
2. **Processes Notes**: Uses GPT-5 API to expand reference abbreviations in Shakespeare commentary notes
3. **Exports to PDF**: Generates individual PDFs for each Act plus a combined complete PDF
4. **Maintains Accuracy**: Ensures 100% content preservation with only reference expansions

## 🔧 Prerequisites

### Required Software
- **Python 3.8+**
- **Tesseract OCR** (for reading PNG images)

### Tesseract Installation
- **Windows**: Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

## 📦 Installation

1. **Clone or download** this repository
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Verify Tesseract installation**:
   ```bash
   tesseract --version
   ```

## 🚀 Usage

### Step 1: Prepare Your Files
Ensure you have these files in your working directory:
- `Capture.PNG`, `Capture2.PNG`, `Capture3.PNG`, `Capture4.PNG`, `Capture5.PNG` (bibliography images)
- `macbeth_notes.json` (Shakespeare commentary notes)
- `api_key.pdf` (contains your GPT-5 API key)

### Step 2: Run the Processor
```bash
python gpt5_macbeth_processor.py
```

### Step 3: Check Output
The processor will generate:
- Individual PDFs for each Act: `macbeth_act_1_gpt5_processed.pdf`, etc.
- Combined PDF: `macbeth_complete_gpt5_processed.pdf`

## 🔍 How It Works

### 1. Bibliography Extraction
- Uses OCR to read all 5 PNG bibliography images
- Parses entries into a structured dictionary
- Handles various bibliography formats (Author, Title, Place, Year)

### 2. GPT-5 Processing
- Processes one Act at a time
- For each note, sends text + bibliography to GPT-5 API
- Uses precise prompts to ensure only reference expansion (no summarization)
- Flags unresolved references with `[UNRESOLVED: abbreviation]`

### 3. PDF Export
- Creates professional PDFs with proper formatting
- Individual Act PDFs for focused review
- Combined PDF for complete reference

## 📋 GPT-5 Prompt Strategy

The processor uses carefully crafted prompts to ensure GPT-5:
- **ONLY expands references** (e.g., "Abbott" → "E. A. Abbott, Shakespearean Grammar, London, 1870")
- **DOES NOT change, summarize, or paraphrase** any other text
- **DOES NOT cut off or truncate** any content
- **Flags unresolved references** clearly

## 🔒 Security Features

- API key stored in PDF format (not in code)
- Automatic API key extraction
- Secure API communication
- No hardcoded credentials

## 📊 Output Structure

### Individual Act PDFs
- Professional formatting with clear headers
- Scene-by-scene organization
- Line-by-line commentary with expanded references
- Page breaks between scenes

### Combined PDF
- Complete Macbeth commentary in one file
- Organized by Act → Scene → Line
- All references expanded
- Professional academic formatting

## ⚠️ Important Notes

1. **API Costs**: Each note requires a GPT-5 API call. Monitor your usage.
2. **Processing Time**: Large files may take significant time due to API calls.
3. **Content Preservation**: The processor is designed to maintain 100% original content.
4. **Error Handling**: Failed API calls return original text to prevent data loss.

## 🛠️ Troubleshooting

### OCR Issues
- Ensure Tesseract is properly installed
- Check PNG image quality and resolution
- Verify image file paths

### API Issues
- Check API key validity in `api_key.pdf`
- Verify internet connection
- Monitor API rate limits and quotas

### PDF Generation Issues
- Ensure sufficient disk space
- Check file permissions
- Verify ReportLab installation

## 📈 Performance Optimization

- **Batch Processing**: Processes one Act at a time to manage memory
- **Error Recovery**: Continues processing even if individual API calls fail
- **Progress Tracking**: Real-time updates on processing status
- **Comprehensive Logging**: Detailed output for debugging

## 🔄 Customization

### Modify Bibliography Patterns
Edit the `parse_bibliography_entry` method in `BibliographyExtractor` class to handle different bibliography formats.

### Adjust GPT-5 Parameters
Modify the `expand_references_with_gpt5` method to change:
- Model parameters (temperature, max_tokens)
- API timeout settings
- Error handling behavior

### Customize PDF Formatting
Edit the `PDFExporter` class to modify:
- Page layouts and margins
- Font styles and sizes
- Header formatting
- Page break behavior

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Verify all prerequisites are installed
3. Ensure file paths and permissions are correct
4. Monitor API usage and quotas

## 🎉 Success Indicators

The processor is working correctly when you see:
- ✅ OCR successfully extracts bibliography entries
- ✅ GPT-5 API calls complete successfully
- ✅ PDF files are generated without errors
- ✅ Final report shows all acts processed
- ✅ No content is lost or truncated

## 📚 Example Output

### Before Processing
```
"Abbott says the witches are supernatural beings..."
```

### After Processing
```
"E. A. Abbott, Shakespearean Grammar, London, 1870 says the witches are supernatural beings..."
```

### Unresolved Reference
```
"[UNRESOLVED: UnknownAuthor] suggests..."
```

This processor ensures your Shakespeare commentary notes are professionally formatted with all references properly expanded, ready for academic use or publication.
