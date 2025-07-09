# QR Generator Test Documentation

## Overview
This document describes the comprehensive test suite for the QR Generator application, including manual test cases in Qmetry format and automated tests.

## Test Artifacts Created

### 1. Qmetry Test Cases (Excel Format)
**File**: `QR_Generator_Test_Cases_Qmetry.xlsx`
- **Total Test Cases**: 25
- **Format**: Industry-standard Qmetry format
- **Categories**: 
  - QR Code Generation (5 test cases)
  - Database Management (4 test cases)
  - Device Connection (3 test cases)
  - Export Functionality (3 test cases)
  - UI/UX Testing (4 test cases)
  - Field Validation (2 test cases)
  - Performance Testing (2 test cases)
  - Security Testing (2 test cases)

### 2. Automated Test Suite
**File**: `test_qr_generator.py`
- **Total Test Classes**: 4
- **Test Categories**:
  - Core Functionality Tests
  - Security Tests
  - Performance Tests
  - Integration Tests

### 3. Test Runner Script
**File**: `run_tests.py`
- **Purpose**: Automated test execution for pre-merge validation
- **Features**:
  - Dependency checking
  - Multiple test execution modes
  - Comprehensive reporting
  - Exit codes for CI/CD integration

## Test Coverage

### Core Functionality
- ✅ QR code generation with different formats (Olarm, JSON, CSV, etc.)
- ✅ Database CRUD operations
- ✅ Excel export functionality
- ✅ Input validation
- ✅ Error handling

### Security
- ✅ SQL injection prevention
- ✅ Path traversal prevention
- ✅ Input sanitization

### Performance
- ✅ QR generation speed (< 1 second average)
- ✅ Database operation performance
- ✅ Memory usage validation

### Integration
- ✅ End-to-end workflow testing
- ✅ GUI launch validation
- ✅ Database schema verification

## How to Run Tests

### Quick Test (Recommended for development)
```bash
python3 run_tests.py --quick
```

### Full Test Suite (Recommended for merge)
```bash
python3 run_tests.py
```

### Unit Tests Only
```bash
python3 run_tests.py --unit-only
```

### Direct Unit Test Execution
```bash
python3 test_qr_generator.py
```

## Test Results Interpretation

### Success Indicators
- **Exit Code 0**: All tests passed
- **Green checkmarks**: Individual test success
- **"ALL TESTS PASSED - READY FOR MERGE!"**: Ready for production

### Failure Indicators
- **Exit Code 1**: Some tests failed
- **Red X marks**: Individual test failures
- **"SOME TESTS FAILED - REVIEW BEFORE MERGE"**: Requires investigation

## Test Dependencies

### Required Packages
- `qrcode`: QR code generation
- `PIL` (Pillow): Image processing
- `openpyxl`: Excel file handling
- `pandas`: Data manipulation for test case generation

### Installation Command
```bash
pip3 install --break-system-packages qrcode Pillow openpyxl pandas
```

## CI/CD Integration

The test runner is designed for CI/CD integration:

```bash
# In your CI/CD pipeline
python3 run_tests.py
if [ $? -eq 0 ]; then
    echo "Tests passed - proceeding with merge"
else
    echo "Tests failed - blocking merge"
    exit 1
fi
```

## Manual Test Execution

For manual testing, refer to the Qmetry Excel file:
1. Open `QR_Generator_Test_Cases_Qmetry.xlsx`
2. Follow test steps for each test case
3. Record actual results
4. Update status (Pass/Fail)

## Test Case Categories Explained

### QR Generation Tests
- Verify QR code creation with valid/invalid inputs
- Test different QR format options
- Validate QR code file creation and storage

### Database Management Tests
- Test record creation, reading, updating, deletion
- Verify table structure and constraints
- Test record selection and management

### Device Connection Tests
- Test STM32 device connection via OpenOCD
- Verify DevUID extraction functionality
- Test error handling for connection failures

### Export Functionality Tests
- Test Excel export with QR code images
- Verify automatic export after operations
- Test export file format and content

### UI/UX Tests
- Test responsive design across window sizes
- Verify visual elements display correctly
- Test user interaction feedback

### Security Tests
- SQL injection prevention
- Path traversal attack prevention
- Input sanitization validation

### Performance Tests
- QR generation speed benchmarks
- Database operation performance
- Memory usage validation

## Best Practices

1. **Run tests before every merge**: Use `python3 run_tests.py`
2. **Update test cases**: When adding new features, update both manual and automated tests
3. **Document test failures**: Include screenshots and error messages
4. **Regular test maintenance**: Review and update tests quarterly
5. **Performance monitoring**: Monitor test execution times for regressions

## Troubleshooting

### Common Issues
1. **Missing dependencies**: Run with `--skip-deps` flag or install required packages
2. **GUI tests failing**: Ensure display is available or run with `--unit-only`
3. **Database locked**: Ensure no other instances are running
4. **Permission errors**: Check file system permissions for test directories

### Debug Commands
```bash
# Check dependencies
python3 run_tests.py --skip-deps

# Run specific test
python3 -m unittest test_qr_generator.TestQRGeneratorCore.test_qr_generation_basic

# Verbose output
python3 test_qr_generator.py -v
```

## Maintenance

### Adding New Tests
1. Add test cases to `QR_Generator_Test_Cases_Qmetry.xlsx`
2. Implement automated tests in `test_qr_generator.py`
3. Update test runner if needed
4. Update this documentation

### Test Data Management
- Test data is automatically generated and cleaned up
- Temporary files are created in system temp directories
- Database tests use in-memory databases where possible

---

**Last Updated**: July 9, 2025
**Version**: 1.0
**Status**: Ready for Production Use 