# QR Code Generator Suite

A comprehensive QR code generation system with multiple format support, designed for device validation and inventory management. Supports both command-line and GUI interfaces with **Olarm validation system compatibility**.

## 🚀 Features

- **🔧 Multiple QR Code Formats**: 7 different output formats including Olarm-specific validation URLs
- **💻 Dual Interface**: Both CLI and GUI versions available
- **📊 Excel Export**: Automatic export with embedded QR code images
- **💾 Database Storage**: SQLite database for all records with sequential ID management
- **🔍 QR Code Preview**: Real-time preview in GUI
- **📋 Record Management**: View, export, and remove records
- **🎯 Olarm Integration**: Default format compatible with Olarm validation system

## 📦 Installation

### Prerequisites
- Python 3.7+
- Virtual environment (recommended)

### Setup
1. **Clone or download** this repository
2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### macOS Additional Setup (for GUI)
If you encounter tkinter issues:
```bash
brew install python-tk
```

## 🎯 QR Code Formats

### 1. **Olarm (Default)** ⭐
**Format**: `https://olarm.com/o/flxr?a=serial,devuid,vcode`  
**Example**: `https://olarm.com/o/flxr?a=1234505791134,914B160615E18000,203206`  
**Use**: Compatible with Olarm validation system

### 2. **JSON**
**Format**: `{"sn":"serial","vc":"vcode","uid":"devuid"}`  
**Use**: Structured data format

### 3. **CSV**
**Format**: `serial,vcode,devuid`  
**Use**: Simple comma-separated values

### 4. **Pipe**
**Format**: `serial|vcode|devuid`  
**Use**: Pipe-separated values

### 5. **Compact**
**Format**: `serial:vcode:devuid`  
**Use**: Colon-separated compact format

### 6. **Labeled**
**Format**: `Serial Number: serial\nVerification Code: vcode\nDevUID: devuid`  
**Use**: Human-readable format (legacy)

### 7. **URL**
**Format**: `https://validate.example.com?sn=serial&vc=vcode&uid=devuid`  
**Use**: Generic validation URL

## 🖥️ Usage

### Command Line Interface (CLI)

#### Quick Generation (Olarm format):
```bash
python3 qr_generator_cli.py [serial_number] [verification_code] [dev_uid]
```

**Example**:
```bash
python3 qr_generator_cli.py 1234505791134 203206 914B160615E18000
```

#### Interactive Mode:
```bash
python3 qr_generator_cli.py
```

**Interactive Features**:
- Generate QR codes with format selection
- View records with pagination
- Remove specific records
- Export to Excel manually
- Exit option

### Graphical User Interface (GUI)

#### Launch GUI:
```bash
# Using launcher (recommended)
python3 launch_qr_generator.py

# Direct launch
/opt/homebrew/bin/python3 qr_generator_gui.py  # macOS
python3 qr_generator_gui.py                    # Linux/Windows
```

#### GUI Features:
- **Format Selection**: Dropdown with 7 format options
- **Real-time Help**: Dynamic descriptions for each format
- **QR Preview**: Instant preview of generated QR codes
- **Records Table**: View recent records in the interface
- **All Records Window**: Comprehensive record viewer

### Device UID Extraction

Extract device UID from STM32 devices:
```bash
python3 getDEVUID.py
```

**Requirements**: 
- STM32 device connected via ST-Link
- OpenOCD configured and available

## 📁 Output Files

### Generated Files:
- **QR Images**: `qr_code_{serial}_{timestamp}.png`
- **Excel Export**: `qr_records.xlsx` (auto-updated)
- **Database**: `qr_codes.db`

### Excel Export Features:
- **Embedded QR Images**: Visual QR codes in spreadsheet
- **Complete Records**: All data fields included
- **Auto-Update**: Updates with every new record
- **Sequential Numbering**: Easy reference system

## 🗃️ Database Schema

**Table**: `qr_records`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Sequential ID (reuses deleted numbers) |
| `serial_number` | TEXT NOT NULL | Device serial number |
| `verification_code` | TEXT NOT NULL | Verification code |
| `dev_uid` | TEXT NOT NULL | Device UID |
| `qr_filename` | TEXT NOT NULL | Generated QR filename |
| `created_at` | TIMESTAMP | Creation timestamp |

## 🛠️ Troubleshooting

### GUI Issues
**Problem**: `ModuleNotFoundError: No module named '_tkinter'`

**Solution**:
```bash
# macOS
brew install python-tk

# Ubuntu/Debian
sudo apt-get install python3-tk

# Use system Python for GUI
/opt/homebrew/bin/python3 qr_generator_gui.py  # macOS
```

### Excel Export Issues
**Problem**: `ModuleNotFoundError: No module named 'openpyxl'`

**Solution**:
```bash
# Activate virtual environment first
source venv/bin/activate
pip install openpyxl
```

### Virtual Environment
**Always use virtual environment for CLI**:
```bash
source venv/bin/activate
python3 qr_generator_cli.py
```

## 📚 Script Reference

### Core Scripts:
- **`qr_generator_cli.py`**: Command-line interface with full functionality
- **`qr_generator_gui.py`**: Graphical interface with visual controls
- **`launch_qr_generator.py`**: Smart launcher (GUI → CLI fallback)

### Utility Scripts:
- **`getDEVUID.py`**: Extract device UID from STM32 via OpenOCD
- **`run_qr_generator.py`**: Alternative launcher script
- **`test_formats.py`**: Test different QR code formats

## 🔧 Configuration

### Default Settings:
- **QR Format**: Olarm (`https://olarm.com/o/flxr?a=...`)
- **Error Correction**: Medium (better scan reliability)
- **QR Version**: 1 (suitable for data size)
- **Excel Auto-Export**: Enabled

### Customization:
Modify format defaults in the generator classes by changing the `format_type` parameter in the `generate_qr_code` method.

## 📖 Examples

### CLI Command Line Mode:
```bash
# Generate Olarm format QR code
python3 qr_generator_cli.py 1234567890 123456 ABCDEF1234567890

# Output:
# ✅ QR code generated successfully!
# 📁 Saved as: qr_code_1234567890_20250702_143022.png
# 🔧 Format: olarm
# 📋 Content: https://olarm.com/o/flxr?a=1234567890,ABCDEF1234567890,123456
```

### CLI Interactive Mode:
```bash
python3 qr_generator_cli.py

# Interactive menu with options:
# 1. Generate new QR code (with format selection)
# 2. View recent records
# 3. Remove a record
# 4. Export to Excel
# 5. Exit
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both CLI and GUI
5. Submit a pull request

## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

---

**🎯 For Olarm users**: This generator defaults to the correct validation URL format and should work seamlessly with your validation system! 