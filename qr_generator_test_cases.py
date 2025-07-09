#!/usr/bin/env python3
"""
QR Generator Test Cases Generator
Creates comprehensive test cases in Qmetry XLS format
"""

import pandas as pd
from datetime import datetime
import os

def create_qmetry_test_cases():
    """Create comprehensive test cases for QR Generator in Qmetry format"""
    
    # Test cases data structure (Qmetry format)
    test_cases = [
        # QR Code Generation Test Cases
        {
            'Test Case ID': 'QR_GEN_001',
            'Test Case Name': 'Generate QR Code with Valid Data',
            'Module': 'QR Generation',
            'Priority': 'High',
            'Test Type': 'Functional',
            'Description': 'Verify QR code generation with valid serial number, verification code, and DevUID',
            'Preconditions': 'Application is launched and GUI is displayed',
            'Test Steps': '1. Enter valid serial number (e.g., TEST123456789012)\n2. Enter valid verification code (e.g., 123456)\n3. Enter valid DevUID (e.g., E5DDA7D74D91EC53)\n4. Select QR format (Olarm)\n5. Click Generate QR Code button',
            'Test Data': 'Serial: TEST123456789012, V-Code: 123456, DevUID: E5DDA7D74D91EC53, Format: olarm',
            'Expected Result': 'QR code is generated successfully, displayed in preview area, saved to file, and record added to database',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'QR_GEN_002',
            'Test Case Name': 'Generate QR Code with Device Name',
            'Module': 'QR Generation',
            'Priority': 'Medium',
            'Test Type': 'Functional',
            'Description': 'Verify QR code generation with optional device name field',
            'Preconditions': 'Application is launched and GUI is displayed',
            'Test Steps': '1. Enter valid serial number\n2. Enter valid verification code\n3. Enter valid DevUID\n4. Enter device name (e.g., Living Room Sensor)\n5. Click Generate QR Code button',
            'Test Data': 'Serial: TEST123456789012, V-Code: 123456, DevUID: E5DDA7D74D91EC53, Device Name: Living Room Sensor',
            'Expected Result': 'QR code is generated successfully and device name is stored in database record',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'QR_GEN_003',
            'Test Case Name': 'Generate QR Code with Empty Fields',
            'Module': 'QR Generation',
            'Priority': 'High',
            'Test Type': 'Negative',
            'Description': 'Verify error handling when required fields are empty',
            'Preconditions': 'Application is launched and GUI is displayed',
            'Test Steps': '1. Leave serial number field empty\n2. Enter valid verification code\n3. Enter valid DevUID\n4. Click Generate QR Code button',
            'Test Data': 'Serial: (empty), V-Code: 123456, DevUID: E5DDA7D74D91EC53',
            'Expected Result': 'Error message displayed: "Please fill in all fields"',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'QR_GEN_004',
            'Test Case Name': 'Test Different QR Formats',
            'Module': 'QR Generation',
            'Priority': 'Medium',
            'Test Type': 'Functional',
            'Description': 'Verify QR code generation with different format options',
            'Preconditions': 'Application is launched and GUI is displayed',
            'Test Steps': '1. Enter valid test data\n2. Select JSON format from dropdown\n3. Click Generate QR Code button\n4. Repeat with CSV, Pipe, Compact, Labeled, and URL formats',
            'Test Data': 'Serial: TEST123456789012, V-Code: 123456, DevUID: E5DDA7D74D91EC53, Formats: JSON, CSV, Pipe, Compact, Labeled, URL',
            'Expected Result': 'QR code is generated successfully for each format with correct data encoding',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'QR_GEN_005',
            'Test Case Name': 'Fill Test Data Functionality',
            'Module': 'QR Generation',
            'Priority': 'Low',
            'Test Type': 'Functional',
            'Description': 'Verify Fill Test Data button generates valid random test data',
            'Preconditions': 'Application is launched and GUI is displayed',
            'Test Steps': '1. Click Fill Test Data button\n2. Verify all fields are populated with test data\n3. Click Generate QR Code button',
            'Test Data': 'Auto-generated test data',
            'Expected Result': 'Valid test data is filled in all fields and QR code can be generated successfully',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        
        # Database Management Test Cases
        {
            'Test Case ID': 'DB_MAN_001',
            'Test Case Name': 'View Records in Database Table',
            'Module': 'Database Management',
            'Priority': 'High',
            'Test Type': 'Functional',
            'Description': 'Verify records are displayed correctly in the database table',
            'Preconditions': 'Database contains at least 5 QR records',
            'Test Steps': '1. Launch application\n2. Observe Recent Records section\n3. Verify all columns are displayed\n4. Check QR thumbnails are visible',
            'Test Data': 'Existing database records',
            'Expected Result': 'All records are displayed with ID, QR thumbnail, Serial Number, V-Code, DevUID, Device Name, and Created timestamp',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'DB_MAN_002',
            'Test Case Name': 'Select Record Functionality',
            'Module': 'Database Management',
            'Priority': 'High',
            'Test Type': 'Functional',
            'Description': 'Verify record selection using custom selection buttons',
            'Preconditions': 'Database contains at least 3 QR records',
            'Test Steps': '1. Click ○ button next to a record\n2. Verify button changes to ✓ and row is highlighted\n3. Click ✓ button to deselect\n4. Verify button changes back to ○ and highlighting is removed',
            'Test Data': 'Existing database records',
            'Expected Result': 'Record selection works correctly with visual feedback (green button, blue row highlight)',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'DB_MAN_003',
            'Test Case Name': 'Remove Selected Record',
            'Module': 'Database Management',
            'Priority': 'High',
            'Test Type': 'Functional',
            'Description': 'Verify selected record can be removed from database',
            'Preconditions': 'Database contains at least 3 QR records',
            'Test Steps': '1. Select a record by clicking ○ button\n2. Click Remove Selected Record button\n3. Verify record is removed from database and table\n4. Verify QR file is deleted from filesystem',
            'Test Data': 'Existing database records',
            'Expected Result': 'Selected record is removed from database, table is refreshed, and QR file is deleted',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'DB_MAN_004',
            'Test Case Name': 'Remove Record Without Selection',
            'Module': 'Database Management',
            'Priority': 'Medium',
            'Test Type': 'Negative',
            'Description': 'Verify error handling when trying to remove record without selection',
            'Preconditions': 'Database contains at least 1 QR record',
            'Test Steps': '1. Ensure no record is selected\n2. Click Remove Selected Record button',
            'Test Data': 'No record selected',
            'Expected Result': 'Error message displayed: "No record selected! Please click the ○ button next to a record to select it first."',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        
        # Device Connection Test Cases
        {
            'Test Case ID': 'DEV_CON_001',
            'Test Case Name': 'Get DevUID from Connected Device',
            'Module': 'Device Connection',
            'Priority': 'High',
            'Test Type': 'Functional',
            'Description': 'Verify DevUID extraction from connected STM32 device',
            'Preconditions': 'STM32 device is connected via ST-Link, OpenOCD is available',
            'Test Steps': '1. Connect STM32 device via ST-Link\n2. Click Get DevUID button\n3. Verify DevUID is extracted and populated in field',
            'Test Data': 'Connected STM32 device',
            'Expected Result': 'DevUID is successfully extracted and populated in the DevUID field',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'DEV_CON_002',
            'Test Case Name': 'Get DevUID Without Device Connected',
            'Module': 'Device Connection',
            'Priority': 'Medium',
            'Test Type': 'Negative',
            'Description': 'Verify error handling when no device is connected',
            'Preconditions': 'No STM32 device connected',
            'Test Steps': '1. Ensure no device is connected\n2. Click Get DevUID button',
            'Test Data': 'No device connected',
            'Expected Result': 'Error message displayed indicating device connection failed',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'DEV_CON_003',
            'Test Case Name': 'Get DevUID with Timeout',
            'Module': 'Device Connection',
            'Priority': 'Medium',
            'Test Type': 'Negative',
            'Description': 'Verify timeout handling for device connection',
            'Preconditions': 'Device connection is slow or problematic',
            'Test Steps': '1. Simulate slow device connection\n2. Click Get DevUID button\n3. Wait for timeout (15 seconds)',
            'Test Data': 'Slow/problematic device connection',
            'Expected Result': 'Timeout error message displayed after 15 seconds',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        
        # Export Functionality Test Cases
        {
            'Test Case ID': 'EXP_FUN_001',
            'Test Case Name': 'Export Records to Excel',
            'Module': 'Export Functionality',
            'Priority': 'High',
            'Test Type': 'Functional',
            'Description': 'Verify records can be exported to Excel with QR code images',
            'Preconditions': 'Database contains at least 5 QR records',
            'Test Steps': '1. Click Export to Excel button\n2. Verify Excel file is created\n3. Open Excel file and verify data\n4. Verify QR code images are embedded',
            'Test Data': 'Existing database records',
            'Expected Result': 'Excel file qr_records.xlsx is created with all records, proper formatting, and embedded QR images',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'EXP_FUN_002',
            'Test Case Name': 'Auto-Export After QR Generation',
            'Module': 'Export Functionality',
            'Priority': 'Medium',
            'Test Type': 'Functional',
            'Description': 'Verify Excel file is automatically updated after generating new QR code',
            'Preconditions': 'Application is launched and Excel file exists',
            'Test Steps': '1. Generate a new QR code\n2. Check Excel file timestamp\n3. Open Excel file and verify new record is added',
            'Test Data': 'New QR code generation',
            'Expected Result': 'Excel file is automatically updated with new record after QR code generation',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'EXP_FUN_003',
            'Test Case Name': 'Auto-Export After Record Deletion',
            'Module': 'Export Functionality',
            'Priority': 'Medium',
            'Test Type': 'Functional',
            'Description': 'Verify Excel file is automatically updated after deleting record',
            'Preconditions': 'Database contains at least 3 QR records',
            'Test Steps': '1. Delete a record from database\n2. Check Excel file timestamp\n3. Open Excel file and verify record is removed',
            'Test Data': 'Existing database records',
            'Expected Result': 'Excel file is automatically updated with record removed after deletion',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        
        # UI/UX Test Cases
        {
            'Test Case ID': 'UI_UX_001',
            'Test Case Name': 'Responsive Design Testing',
            'Module': 'UI/UX',
            'Priority': 'Medium',
            'Test Type': 'Functional',
            'Description': 'Verify application layout adapts to different window sizes',
            'Preconditions': 'Application is launched',
            'Test Steps': '1. Resize window to minimum size (800x600)\n2. Verify all elements are visible and usable\n3. Resize to large size (1920x1080)\n4. Verify layout utilizes space efficiently',
            'Test Data': 'Various window sizes',
            'Expected Result': 'Application layout adapts properly to different window sizes with all elements accessible',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'UI_UX_002',
            'Test Case Name': 'QR Code Preview Display',
            'Module': 'UI/UX',
            'Priority': 'High',
            'Test Type': 'Functional',
            'Description': 'Verify QR code preview displays correctly after generation',
            'Preconditions': 'Application is launched',
            'Test Steps': '1. Generate a QR code\n2. Verify QR code appears in preview area\n3. Verify image quality and size (180x180)\n4. Verify image is clear and scannable',
            'Test Data': 'Valid QR code generation',
            'Expected Result': 'QR code preview displays correctly with good quality and proper size',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'UI_UX_003',
            'Test Case Name': 'QR Thumbnails in Table',
            'Module': 'UI/UX',
            'Priority': 'Medium',
            'Test Type': 'Functional',
            'Description': 'Verify QR code thumbnails display correctly in records table',
            'Preconditions': 'Database contains QR records',
            'Test Steps': '1. Observe records table\n2. Verify QR thumbnails are visible (80x80)\n3. Verify thumbnails are clear and properly sized\n4. Verify tooltips work on hover',
            'Test Data': 'Existing database records',
            'Expected Result': 'QR thumbnails display correctly in table with proper size and tooltips',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'UI_UX_004',
            'Test Case Name': 'Status Messages Display',
            'Module': 'UI/UX',
            'Priority': 'Medium',
            'Test Type': 'Functional',
            'Description': 'Verify status messages display correctly for different actions',
            'Preconditions': 'Application is launched',
            'Test Steps': '1. Perform various actions (generate QR, clear fields, etc.)\n2. Verify appropriate status messages appear\n3. Verify message colors (green for success, red for error)\n4. Verify messages are properly formatted',
            'Test Data': 'Various application actions',
            'Expected Result': 'Status messages display correctly with appropriate colors and formatting',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        
        # Field Validation Test Cases
        {
            'Test Case ID': 'VAL_001',
            'Test Case Name': 'Clear Fields Functionality',
            'Module': 'Field Validation',
            'Priority': 'Low',
            'Test Type': 'Functional',
            'Description': 'Verify Clear Fields button clears all input fields',
            'Preconditions': 'Application is launched and fields contain data',
            'Test Steps': '1. Fill all input fields with data\n2. Click Clear Fields button\n3. Verify all fields are empty\n4. Verify QR preview is cleared',
            'Test Data': 'Any valid input data',
            'Expected Result': 'All input fields are cleared and QR preview is removed',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'VAL_002',
            'Test Case Name': 'Format Dropdown Validation',
            'Module': 'Field Validation',
            'Priority': 'Medium',
            'Test Type': 'Functional',
            'Description': 'Verify format dropdown displays correct options and help text',
            'Preconditions': 'Application is launched',
            'Test Steps': '1. Click format dropdown\n2. Verify all format options are available\n3. Select each format and verify help text updates\n4. Verify default format is Olarm',
            'Test Data': 'Format options: olarm, json, csv, pipe, compact, labeled, url',
            'Expected Result': 'Format dropdown works correctly with all options and appropriate help text',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        
        # Performance Test Cases
        {
            'Test Case ID': 'PERF_001',
            'Test Case Name': 'QR Generation Performance',
            'Module': 'Performance',
            'Priority': 'Low',
            'Test Type': 'Performance',
            'Description': 'Verify QR code generation completes within acceptable time',
            'Preconditions': 'Application is launched',
            'Test Steps': '1. Fill valid test data\n2. Click Generate QR Code button\n3. Measure time from click to completion\n4. Repeat 10 times and calculate average',
            'Test Data': 'Valid test data',
            'Expected Result': 'QR code generation completes within 3 seconds on average',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'PERF_002',
            'Test Case Name': 'Database Loading Performance',
            'Module': 'Performance',
            'Priority': 'Low',
            'Test Type': 'Performance',
            'Description': 'Verify database records load within acceptable time',
            'Preconditions': 'Database contains 100+ records',
            'Test Steps': '1. Launch application\n2. Measure time to load records table\n3. Perform record operations and measure refresh time',
            'Test Data': 'Database with 100+ records',
            'Expected Result': 'Records load within 5 seconds, table refreshes within 2 seconds',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        
        # Security Test Cases
        {
            'Test Case ID': 'SEC_001',
            'Test Case Name': 'Database Security',
            'Module': 'Security',
            'Priority': 'High',
            'Test Type': 'Security',
            'Description': 'Verify database operations are secure and prevent SQL injection',
            'Preconditions': 'Application is launched',
            'Test Steps': '1. Enter SQL injection code in input fields\n2. Attempt to generate QR code\n3. Verify database is not compromised',
            'Test Data': 'SQL injection attempts: \'; DROP TABLE qr_records; --',
            'Expected Result': 'Application handles malicious input safely without database compromise',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        },
        {
            'Test Case ID': 'SEC_002',
            'Test Case Name': 'File System Security',
            'Module': 'Security',
            'Priority': 'Medium',
            'Test Type': 'Security',
            'Description': 'Verify file operations are secure and prevent path traversal',
            'Preconditions': 'Application is launched',
            'Test Steps': '1. Enter path traversal characters in input fields\n2. Generate QR code\n3. Verify files are created in correct location only',
            'Test Data': 'Path traversal attempts: ../../../etc/passwd, ..\\\\windows\\\\system32',
            'Expected Result': 'Application prevents path traversal and creates files only in designated directory',
            'Status': 'Not Executed',
            'Author': 'QA Team',
            'Created Date': datetime.now().strftime('%Y-%m-%d')
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(test_cases)
    
    # Save to Excel with formatting
    with pd.ExcelWriter('QR_Generator_Test_Cases_Qmetry.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Test Cases', index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Test Cases']
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
            worksheet.column_dimensions[column_letter].width = adjusted_width
        
        # Make header row bold
        from openpyxl.styles import Font, PatternFill
        header_font = Font(bold=True)
        header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
        
        for cell in worksheet[1]:
            cell.font = header_font
            cell.fill = header_fill
    
    print(f"✅ Created {len(test_cases)} test cases in QR_Generator_Test_Cases_Qmetry.xlsx")
    return len(test_cases)

if __name__ == "__main__":
    create_qmetry_test_cases() 