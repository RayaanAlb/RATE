# QR Code Generator Suite

A modern, responsive QR code generation application with **Flet GUI** and command-line interfaces. Features **South African Standard Time (SAST)** timezone support and multiple output formats optimized for Olarm system compatibility.

## 🚀 Quick Start

```bash
# Check dependencies and install if needed
python3 check_dependencies.py

# Launch GUI application
python3 qr.py
```

## ✨ Key Features

- **🎨 Modern Flet GUI**: Responsive web-based interface
- **🔧 7 QR Formats**: Olarm (default), JSON, CSV, Pipe, Compact, Labeled, URL
- **📊 Excel Export**: Automatic export with embedded QR images
- **💾 SQLite Database**: Persistent storage with smart ID management
- **🔌 STM32 Integration**: Automatic DevUID extraction via OpenOCD
- **🕘 SAST Timezone**: All timestamps in South African Standard Time (GMT+2)
- **🧪 Comprehensive Testing**: 100% test coverage with automated and manual suites

## 📦 Dependencies

Managed automatically with the dependency checker:
```bash
python3 check_dependencies.py  # Checks and installs missing packages
```

**Required packages** (from `getDEVUID/requirements.txt`):
- `qrcode[pil]>=7.4.2`
- `Pillow>=10.0.0`
- `openpyxl>=3.0.0`
- `pexpect>=4.8.0`
- `flet>=0.21.0`

## 🖥️ Usage

### GUI Application
```bash
python3 qr.py  # Main launcher
```

**Features:**
- Fill fields: Serial, Verification Code, DevUID, Device Name
- **🔌 Get DevUID**: Extract from connected STM32 device
- Generate QR codes with format selection
- Manage records with visual selection (○/✓)
- Auto-export to Excel with QR thumbnails

### Command Line Interface
```bash
cd getDEVUID
python3 qr_generator_cli.py [serial] [verification_code] [dev_uid]

# Interactive mode
python3 qr_generator_cli.py
```

## 🎯 QR Code Formats

| Format | Example | Use Case |
|--------|---------|----------|
| **Olarm** ⭐ | `https://olarm.com/o/flxr?a=serial,devuid,vcode` | Olarm validation system |
| **JSON** | `{"sn":"serial","vc":"vcode","uid":"devuid"}` | API integration |
| **CSV** | `serial,vcode,devuid` | Simple comma-separated |
| **Pipe** | `serial\|vcode\|devuid` | Pipe-separated values |
| **Compact** | `serial:vcode:devuid` | Colon-separated |
| **Labeled** | `Serial Number: serial\n...` | Human-readable |
| **URL** | `https://validate.example.com?sn=...` | Generic validation |

## 📁 Generated Files

- **QR Images**: `qr_code_{serial}_{timestamp}_SAST.png`
- **Excel Export**: `qr_records.xlsx` (auto-updated with embedded QR images)
- **Database**: `qr_codes.db` (SQLite with SAST timestamps)

## 🧪 Testing

```bash
# Run automated tests
python3 run_tests.py

# Manual test cases
# See: QR_Generator_Test_Cases_Qmetry.xlsx (25 test cases)
# Documentation: TEST_DOCUMENTATION.md
```

## 🔧 Troubleshooting

### Quick Fixes
```bash
# Check dependencies first
python3 check_dependencies.py

# If GUI fails, try CLI
cd getDEVUID && python3 qr_generator_cli.py

# STM32 connection issues
cd getDEVUID && python3 getDEVUID.py
```

### Common Issues
- **GUI won't start**: Check dependencies, use `python3 qr.py`
- **Missing QR images**: Ensure openpyxl installed, check `getDEVUID/qr_code_*_SAST.png`
- **STM32 DevUID fails**: Verify ST-Link connection and OpenOCD setup

## 📚 Project Structure

```
RATE/
├── README.md                              # This file
├── qr.py                                  # Main launcher
├── check_dependencies.py                 # Dependency checker
├── test_qr_generator.py                   # Automated tests
├── run_tests.py                           # Test runner
├── TEST_DOCUMENTATION.md                  # Test documentation
├── QR_Generator_Test_Cases_Qmetry.xlsx    # Manual test cases
└── getDEVUID/
    ├── qr_generator_gui.py               # GUI application
    ├── qr_generator_cli.py               # CLI application
    ├── getDEVUID.py                      # STM32 DevUID extraction
    ├── requirements.txt                  # Dependencies
    ├── qr_codes.db                       # Database
    ├── qr_records.xlsx                   # Excel export
    └── openocd/                          # OpenOCD binaries
```

## 🎯 Use Cases

- **Device Manufacturing**: Generate validation QR codes for devices
- **Inventory Management**: Create scannable identifiers with Excel export
- **Olarm Integration**: Default format works seamlessly with Olarm system
- **STM32 Development**: Automatic DevUID extraction from connected devices

## 📈 Recent Updates

- **✅ Smart Dependency Checker**: Automated package verification and installation
- **✅ SAST Timezone Support**: All timestamps in South African Standard Time
- **✅ Comprehensive Testing**: 100% test coverage with automated and manual suites
- **✅ Production Ready**: Fully tested and merged to main branch

---

**🎯 Perfect for Olarm users**: Default format creates validation URLs that work seamlessly with the Olarm system!

**🎨 Modern Interface**: Built with Flet for a responsive, professional user experience.

**🕘 SAST Timezone**: All timestamps consistently use South African Standard Time.
