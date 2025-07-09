# QR Code Generator Suite

A modern, responsive QR code generation application with **Flet GUI** and command-line interfaces. Designed for device validation, inventory management, and Olarm system compatibility.

## 🚀 Features

- **🎨 Modern Flet GUI**: Responsive web-based interface that works on all screen sizes
- **💻 Command-Line Interface**: Full-featured CLI for automation and scripting
- **🔧 Multiple QR Formats**: 7 different output formats including Olarm-specific validation URLs
- **📊 Excel Integration**: Automatic export with embedded QR code images and device names
- **💾 SQLite Database**: Persistent storage with smart ID management
- **🖼️ QR Preview**: Real-time preview with larger thumbnail display
- **📱 Device Names**: Optional device naming for better organization
- **🔍 Record Management**: Select, view, and remove records with visual feedback
- **📈 Responsive Design**: Perfect text centering and layout at all window sizes

## 📦 Installation

### Prerequisites
- Python 3.7+
- Modern web browser (for Flet GUI)

### Quick Setup
```bash
# Navigate to project directory
cd getDEVUID

# Install dependencies
pip3 install -r requirements.txt

# Launch GUI application
python3 qr_generator_gui.py
```

### Alternative Launchers
```bash
# Smart launcher with fallback
python3 launch_qr_generator.py

# Run launcher
python3 run_qr_generator.py
```

## 🎯 QR Code Formats

### 1. **Olarm (Default)** ⭐
- **Format**: `https://olarm.com/o/flxr?a=serial,devuid,vcode`
- **Use**: Compatible with Olarm validation system

### 2. **JSON**
- **Format**: `{"sn":"serial","vc":"vcode","uid":"devuid"}`
- **Use**: Structured data format for APIs

### 3. **CSV**
- **Format**: `serial,vcode,devuid`
- **Use**: Simple comma-separated values

### 4. **Pipe**
- **Format**: `serial|vcode|devuid`
- **Use**: Pipe-separated values

### 5. **Compact**
- **Format**: `serial:vcode:devuid`
- **Use**: Colon-separated compact format

### 6. **Labeled**
- **Format**: `Serial Number: serial\nVerification Code: vcode\nDevUID: devuid`
- **Use**: Human-readable format (legacy)

### 7. **URL**
- **Format**: `https://validate.example.com?sn=serial&vc=vcode&uid=devuid`
- **Use**: Generic validation URL

## 🖥️ GUI Application

### Features
- **📱 Responsive Design**: Works perfectly from small windows to full screen
- **🎨 Modern Interface**: Clean, professional Flet-based UI
- **🔍 QR Preview**: 80x80 pixel thumbnails with real-time generation preview
- **📝 Device Names**: Optional field for naming devices (e.g., "Living Room Sensor")
- **⚡ Auto-Export**: Automatic Excel file updates after each record
- **🎯 Smart Selection**: Custom selection buttons with visual feedback
- **📊 Data Table**: View all records with QR thumbnails and device information

### GUI Usage
1. **Fill Fields**: Enter Serial Number, Verification Code, DevUID, and optional Device Name
   - **🔌 Get DevUID**: Click button to automatically extract DevUID from connected STM32 device
2. **Select Format**: Choose from dropdown (Olarm recommended)
3. **Generate**: Click "Generate QR Code" to create and save
4. **Manage Records**: Use selection buttons (○/✓) to select and remove records
5. **Export**: Records automatically exported to Excel with QR images

### Button Functions
- **Generate QR Code**: Creates QR code and saves to database
- **🔌 Get DevUID**: Extracts DevUID from connected STM32 device via ST-Link/OpenOCD
- **Clear Fields**: Clears all input fields
- **Fill Test Data**: Generates random test data for testing
- **Export to Excel**: Manual Excel export (auto-export happens automatically)
- **Remove Selected Record**: Deletes selected record and associated QR file

## 💻 Command Line Interface

### Quick Generation
```bash
python3 qr_generator_cli.py [serial] [verification_code] [dev_uid]
```

**Example**:
```bash
python3 qr_generator_cli.py 1234567890 123456 ABCDEF1234567890
```

### Interactive Mode
```bash
python3 qr_generator_cli.py
```

**Interactive Features**:
- Generate QR codes with format selection
- View records with pagination
- Remove specific records
- Manual Excel export
- Format selection menu

## 📁 Files & Database

### Generated Files
- **QR Images**: `qr_code_{serial}_{timestamp}.png`
- **Excel Export**: `qr_records.xlsx` (auto-updated)
- **Database**: `qr_codes.db` (SQLite)

### Database Schema
**Table**: `qr_records`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY | Sequential ID (reuses deleted IDs) |
| `serial_number` | TEXT NOT NULL | Device serial number |
| `verification_code` | TEXT NOT NULL | Verification code |
| `dev_uid` | TEXT NOT NULL | Device UID |
| `device_name` | TEXT | Optional device name |
| `qr_filename` | TEXT NOT NULL | Generated QR filename |
| `created_at` | TIMESTAMP | Creation timestamp |

### Excel Export Features
- **Embedded QR Images**: 100x100 pixel QR codes in spreadsheet
- **Device Names**: Dedicated column for device identification
- **Auto-Update**: Updates with every new record
- **Complete Data**: All fields included with proper formatting

## 🛠️ Technical Details

### Dependencies
```
flet>=0.21.0
qrcode
pillow
openpyxl
```

### Architecture
- **Frontend**: Flet (Flutter-based GUI framework)
- **Backend**: SQLite database with smart ID management
- **QR Generation**: qrcode library with PIL integration
- **Excel Export**: openpyxl with embedded image support
- **STM32 Integration**: OpenOCD with ST-Link for automatic DevUID extraction

### Responsive Design
- **Window Sizes**: Supports 800x600 minimum to full screen
- **Text Centering**: Perfect alignment at all screen sizes
- **Button Layout**: Adaptive column layout for different screens
- **Table Display**: Horizontal scrolling for wide content

## 🎯 Use Cases

### Device Manufacturing
- Generate QR codes for device validation
- Track serial numbers and verification codes
- Export complete inventories to Excel
- Organize devices by location/type with names

### Inventory Management
- Create scannable device identifiers
- Maintain database of all generated codes
- Export for external systems integration
- Remove invalid/replaced devices

### Olarm Integration
- Generate validation URLs compatible with Olarm system
- Default format matches Olarm requirements
- Batch processing capabilities
- Excel exports for system integration

## 🔧 Troubleshooting

### GUI Won't Start
**Issue**: Flet application fails to launch

**Solutions**:
```bash
# Try the launcher
python3 launch_qr_generator.py

# Use fallback CLI if GUI fails
python3 qr_generator_cli.py
```

### Database Issues
**Issue**: Database corruption or ID conflicts

**Solutions**:
- CLI automatically migrates old databases
- Smart ID management reuses deleted numbers
- Database file: `getDEVUID/qr_codes.db`

### Excel Export Problems
**Issue**: Images not showing in Excel

**Solutions**:
```bash
# Ensure openpyxl is installed
pip3 install openpyxl

# Check QR image files exist
ls getDEVUID/qr_code_*.png
```

### STM32 DevUID Extraction Issues
**Issue**: "Get DevUID" button fails

**Requirements**:
- STM32 device connected via ST-Link
- OpenOCD installed and configured
- Device powered and in programming mode

**Solutions**:
```bash
# Check OpenOCD installation
./openocd/bin/openocd --version

# Test ST-Link connection
./openocd/bin/openocd -f interface/stlink.cfg -f target/stm32wlx.cfg -c "init" -c "exit"

# Manually run DevUID extraction
python3 getDEVUID.py
```

## 📚 Project Structure

```
RATE/
├── README.md                           # This file
└── getDEVUID/
    ├── qr_generator_gui.py            # Main Flet GUI application
    ├── qr_generator_cli.py            # Command-line interface
    ├── launch_qr_generator.py         # Smart launcher script
    ├── run_qr_generator.py            # Alternative launcher
    ├── getDEVUID.py                   # STM32 device UID extraction
    ├── requirements.txt               # Python dependencies
    ├── qr_codes.db                    # SQLite database
    ├── qr_records.xlsx                # Excel export file
    └── README.md                      # Detailed documentation
```

## 📖 Examples

### CLI Example
```bash
$ python3 qr_generator_cli.py 1234567890 123456 ABCDEF1234567890

✅ QR code generated successfully!
📁 Saved as: qr_code_1234567890_20250710_143022.png
🔧 Format: olarm
📋 Content: https://olarm.com/o/flxr?a=1234567890,ABCDEF1234567890,123456
💾 Record saved to database
📊 Excel file updated: qr_records.xlsx
```

### GUI Workflow
1. **Launch**: `python3 qr_generator_gui.py`
2. **Enter Data**: Fill serial, v-code, DevUID, device name
3. **Generate**: Click "Generate QR Code"
4. **View**: See QR preview and table entry
5. **Export**: Records automatically in Excel
6. **Manage**: Select records with ○/✓ buttons to remove

## 🎨 Screenshots

The modern Flet GUI features:
- **Clean Layout**: Professional appearance with proper spacing
- **Responsive Design**: Perfect on any screen size
- **Visual Feedback**: Green selection buttons and blue row highlighting
- **QR Thumbnails**: 80x80 pixel previews in the records table
- **Centered Text**: Perfect alignment throughout the interface

## 🚀 Getting Started

**Quick Start (GUI)**:
```bash
cd getDEVUID
python3 qr_generator_gui.py
```

**Quick Start (CLI)**:
```bash
cd getDEVUID
python3 qr_generator_cli.py
```

**Generate Your First QR Code**:
1. Enter device information (or use "🔌 Get DevUID" for STM32 devices)
2. Optionally add device name
3. Select format (Olarm recommended)
4. Click Generate
5. View in Excel export

---

**🎯 Perfect for Olarm users**: Default format creates validation URLs that work seamlessly with the Olarm system!

**🎨 Modern Interface**: Built with Flet for a responsive, professional user experience across all devices and screen sizes.
