import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
import os

class QRGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.init_database()
        
        # Create GUI elements
        self.create_widgets()
        
        # Load existing records
        self.load_records()
    
    def init_database(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect('qr_codes.db')
        self.cursor = self.conn.cursor()
        
        # Check if we need to migrate from auto-increment to manual ID management
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='qr_records'")
        table_exists = self.cursor.fetchone()
        
        if table_exists:
            # Check if table has auto-increment
            self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='qr_records'")
            table_sql = self.cursor.fetchone()[0]
            
            if 'AUTOINCREMENT' in table_sql:
                print("🔄 Migrating database to remove auto-increment...")
                self.migrate_database()
        else:
            # Create new table without auto-increment
            self.cursor.execute('''
                CREATE TABLE qr_records (
                    id INTEGER PRIMARY KEY,
                    serial_number TEXT NOT NULL,
                    verification_code TEXT NOT NULL,
                    dev_uid TEXT NOT NULL,
                    qr_filename TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
    
    def migrate_database(self):
        """Migrate existing database to remove auto-increment"""
        try:
            # Create backup table
            self.cursor.execute('''
                CREATE TABLE qr_records_backup AS 
                SELECT * FROM qr_records ORDER BY created_at ASC
            ''')
            
            # Drop original table
            self.cursor.execute('DROP TABLE qr_records')
            
            # Create new table without auto-increment
            self.cursor.execute('''
                CREATE TABLE qr_records (
                    id INTEGER PRIMARY KEY,
                    serial_number TEXT NOT NULL,
                    verification_code TEXT NOT NULL,
                    dev_uid TEXT NOT NULL,
                    qr_filename TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Get data from backup and reassign sequential IDs
            self.cursor.execute('SELECT serial_number, verification_code, dev_uid, qr_filename, created_at FROM qr_records_backup ORDER BY created_at ASC')
            records = self.cursor.fetchall()
            
            # Insert records with sequential IDs starting from 1
            for i, record in enumerate(records, 1):
                self.cursor.execute('''
                    INSERT INTO qr_records (id, serial_number, verification_code, dev_uid, qr_filename, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (i, record[0], record[1], record[2], record[3], record[4]))
            
            # Drop backup table
            self.cursor.execute('DROP TABLE qr_records_backup')
            
            self.conn.commit()
            print("✅ Database migration completed - IDs are now sequential")
            
        except Exception as e:
            print(f"❌ Migration error: {str(e)}")
            # Restore from backup if migration fails
            try:
                self.cursor.execute('DROP TABLE IF EXISTS qr_records')
                self.cursor.execute('ALTER TABLE qr_records_backup RENAME TO qr_records')
                self.conn.commit()
                print("🔄 Restored original table")
            except:
                pass
    
    def create_widgets(self):
        """Create GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="QR Code Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input fields
        ttk.Label(main_frame, text="Serial Number:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.serial_entry = ttk.Entry(main_frame, width=30)
        self.serial_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Verification Code:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.vcode_entry = ttk.Entry(main_frame, width=30)
        self.vcode_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="DevUID:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.devuid_entry = ttk.Entry(main_frame, width=30)
        self.devuid_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Format selection
        ttk.Label(main_frame, text="QR Format:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="olarm")
        format_combo = ttk.Combobox(main_frame, textvariable=self.format_var, width=28, state="readonly")
        format_combo['values'] = (
            'olarm', 'json', 'csv', 'pipe', 'compact', 'labeled', 'url'
        )
        format_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Format help text
        self.format_help = ttk.Label(main_frame, text="Olarm (recommended) - Compatible with Olarm validation system", 
                                    font=('Arial', 8), foreground='gray')
        self.format_help.grid(row=4, column=1, sticky=tk.W, pady=(25, 0), padx=(10, 0))
        
        # Bind format selection change to update help text
        format_combo.bind('<<ComboboxSelected>>', self.on_format_change)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Generate button
        self.generate_btn = ttk.Button(button_frame, text="Generate QR Code", 
                                      command=self.generate_qr_code)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        self.clear_btn = ttk.Button(button_frame, text="Clear Fields", 
                                   command=self.clear_fields)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # View Records button
        self.view_btn = ttk.Button(button_frame, text="View All Records", 
                                  command=self.view_records)
        self.view_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Remove Record button
        self.remove_btn = ttk.Button(button_frame, text="Remove Record", 
                                    command=self.remove_record)
        self.remove_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Export to Excel button
        self.export_btn = ttk.Button(button_frame, text="Export to Excel", 
                                    command=self.export_to_excel)
        self.export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Fill Test Data button
        self.test_btn = ttk.Button(button_frame, text="Fill Test Data", 
                                  command=self.fill_test_data)
        self.test_btn.pack(side=tk.LEFT)
        
        # QR Code preview frame
        preview_frame = ttk.LabelFrame(main_frame, text="QR Code Preview", padding="10")
        preview_frame.grid(row=6, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        self.qr_label = ttk.Label(preview_frame, text="QR Code will appear here")
        self.qr_label.pack()
        
        # Records table frame
        table_frame = ttk.LabelFrame(main_frame, text="Recent Records", padding="10")
        table_frame.grid(row=7, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Treeview for records
        columns = ('ID', 'Serial Number', 'Verification Code', 'DevUID', 'Created At')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
    
    def generate_qr_code(self):
        """Generate QR code with input data"""
        serial_number = self.serial_entry.get().strip()
        verification_code = self.vcode_entry.get().strip()
        dev_uid = self.devuid_entry.get().strip()
        format_type = self.format_var.get()
        
        # Validate inputs
        if not all([serial_number, verification_code, dev_uid]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,  # Changed to Medium for better reliability
                box_size=10,
                border=4,
            )
            
            # Prepare QR code data based on format type
            if format_type == "json":
                import json
                qr_data = json.dumps({
                    "sn": serial_number,
                    "vc": verification_code,
                    "uid": dev_uid
                }, separators=(',', ':'))  # Compact JSON
            elif format_type == "csv":
                qr_data = f"{serial_number},{verification_code},{dev_uid}"
            elif format_type == "pipe":
                qr_data = f"{serial_number}|{verification_code}|{dev_uid}"
            elif format_type == "labeled":
                # Old format with labels
                qr_data = f"Serial Number: {serial_number}\nVerification Code: {verification_code}\nDevUID: {dev_uid}"
            elif format_type == "compact":
                # Very compact format
                qr_data = f"{serial_number}:{verification_code}:{dev_uid}"
            elif format_type == "url":
                # URL format for web validation (generic)
                qr_data = f"https://validate.example.com?sn={serial_number}&vc={verification_code}&uid={dev_uid}"
            elif format_type == "olarm":
                # Olarm specific URL format: serial,devuid,verification_code
                qr_data = f"https://olarm.com/o/flxr?a={serial_number},{dev_uid},{verification_code}"
            else:
                # Default to Olarm if invalid format specified
                qr_data = f"https://olarm.com/o/flxr?a={serial_number},{dev_uid},{verification_code}"
            
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_code_{serial_number}_{timestamp}.png"
            
            # Save QR code image
            qr_image.save(filename)
            
            # Display QR code in preview
            self.display_qr_preview(qr_image)
            
            # Save to database
            self.save_to_database(serial_number, verification_code, dev_uid, filename)
            
            # Auto-export to Excel after each new record
            try:
                self.export_to_excel_silent()
            except:
                pass  # Don't show error if auto-export fails
            
            # Refresh records table
            self.load_records()
            
            messagebox.showinfo("Success", f"QR code generated successfully!\n\nFile: {filename}\nFormat: {format_type}\nContent: {qr_data[:100]}{'...' if len(qr_data) > 100 else ''}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
    
    def display_qr_preview(self, qr_image):
        """Display QR code in the preview area"""
        # Resize image for preview
        preview_size = (200, 200)
        qr_preview = qr_image.resize(preview_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.qr_photo = ImageTk.PhotoImage(qr_preview)
        
        # Update label
        self.qr_label.configure(image=self.qr_photo, text="")
    
    def save_to_database(self, serial_number, verification_code, dev_uid, filename):
        """Save record to database"""
        try:
            # Find the lowest available ID (reuse deleted numbers)
            # First check if there are any records
            self.cursor.execute('SELECT COUNT(*) FROM qr_records')
            record_count = self.cursor.fetchone()[0]
            
            if record_count == 0:
                next_id = 1
            else:
                # Look for gaps in the sequence starting from 1
                self.cursor.execute('SELECT id FROM qr_records ORDER BY id')
                existing_ids = [row[0] for row in self.cursor.fetchall()]
                
                # Find the first missing number in sequence
                next_id = 1
                for existing_id in existing_ids:
                    if next_id == existing_id:
                        next_id += 1
                    else:
                        break
            
            # Insert with specific ID
            self.cursor.execute('''
                INSERT INTO qr_records (id, serial_number, verification_code, dev_uid, qr_filename)
                VALUES (?, ?, ?, ?, ?)
            ''', (next_id, serial_number, verification_code, dev_uid, filename))
            self.conn.commit()
            
            print(f"Record saved with ID: {next_id}")
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save to database: {str(e)}")
    
    def load_records(self):
        """Load records from database into treeview"""
        # Clear existing records
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Fetch records from database
        try:
            self.cursor.execute('''
                SELECT id, serial_number, verification_code, dev_uid, created_at
                FROM qr_records
                ORDER BY created_at DESC
                LIMIT 20
            ''')
            records = self.cursor.fetchall()
            
            # Insert records into treeview
            for record in records:
                # Format datetime
                created_at = datetime.fromisoformat(record[4]).strftime("%Y-%m-%d %H:%M:%S")
                self.tree.insert('', 'end', values=(record[0], record[1], record[2], record[3], created_at))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load records: {str(e)}")
    
    def on_format_change(self, event=None):
        """Update help text when format selection changes"""
        format_descriptions = {
            'olarm': 'Olarm (recommended) - Compatible with Olarm validation system',
            'json': 'JSON - Structured data format {"sn":"...","vc":"...","uid":"..."}',
            'csv': 'CSV - Comma-separated values: serial,verification,devuid',
            'pipe': 'Pipe - Pipe-separated values: serial|verification|devuid',
            'compact': 'Compact - Colon-separated: serial:verification:devuid',
            'labeled': 'Labeled - Human-readable with labels (old format)',
            'url': 'URL - Generic validation URL format'
        }
        selected_format = self.format_var.get()
        self.format_help.configure(text=format_descriptions.get(selected_format, ''))
    
    def clear_fields(self):
        """Clear all input fields"""
        self.serial_entry.delete(0, tk.END)
        self.vcode_entry.delete(0, tk.END)
        self.devuid_entry.delete(0, tk.END)
        self.qr_label.configure(image='', text="QR Code will appear here")
    
    def fill_test_data(self):
        """Fill fields with test data for easy testing"""
        import random
        
        # Clear existing data first
        self.clear_fields()
        
        # Generate test data
        test_serial = f"TEST{random.randint(100000000000, 999999999999)}"
        test_vcode = f"{random.randint(100000, 999999)}"
        test_devuid = f"{''.join(random.choices('0123456789ABCDEF', k=16))}"
        
        # Fill the fields
        self.serial_entry.insert(0, test_serial)
        self.vcode_entry.insert(0, test_vcode)
        self.devuid_entry.insert(0, test_devuid)
        
        # Set format to Olarm (default)
        self.format_var.set("olarm")
        self.on_format_change()
        
        print(f"📝 Test data filled:")
        print(f"   Serial: {test_serial}")
        print(f"   V-Code: {test_vcode}")
        print(f"   DevUID: {test_devuid}")
        print(f"   Format: olarm")
    
    def remove_record(self):
        """Remove a selected record from the database"""
        # Get selected item from treeview
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a record from the table to remove.")
            return
        
        # Get record details
        item = self.tree.item(selected_item[0])
        record_values = item['values']
        record_id = record_values[0]  # ID is the first column
        serial_number = record_values[1]
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion", 
            f"Are you sure you want to delete record ID {record_id}?\n\n"
            f"Serial Number: {serial_number}\n\n"
            f"This will also delete the QR code file.",
            icon='warning'
        )
        
        if not confirm:
            return
        
        try:
            # Get QR filename from database
            self.cursor.execute('SELECT qr_filename FROM qr_records WHERE id = ?', (record_id,))
            result = self.cursor.fetchone()
            
            if result:
                qr_filename = result[0]
                
                # Delete the QR code file if it exists
                if os.path.exists(qr_filename):
                    try:
                        os.remove(qr_filename)
                        print(f"Deleted QR code file: {qr_filename}")
                    except Exception as e:
                        print(f"Warning: Could not delete QR code file {qr_filename}: {e}")
                
                # Delete from database
                self.cursor.execute('DELETE FROM qr_records WHERE id = ?', (record_id,))
                self.conn.commit()
                
                # Auto-update Excel file
                try:
                    self.export_to_excel_silent()
                except:
                    pass  # Don't show error if auto-export fails
                
                # Refresh records table
                self.load_records()
                
                # Clear QR preview if it was showing the deleted record
                self.qr_label.configure(image='', text="QR Code will appear here")
                
                messagebox.showinfo("Success", f"Record ID {record_id} deleted successfully!")
            else:
                messagebox.showerror("Error", f"Record ID {record_id} not found in database.")
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete record: {str(e)}")
    
    def export_to_excel(self):
        """Export all records to Excel with QR code images"""
        try:
            from openpyxl import Workbook
            from openpyxl.drawing.image import Image as OpenpyxlImage
            from openpyxl.styles import Font, Alignment, PatternFill
            
            # Fetch all records from database
            self.cursor.execute('''
                SELECT id, serial_number, verification_code, dev_uid, qr_filename, created_at
                FROM qr_records
                ORDER BY created_at ASC
            ''')
            records = self.cursor.fetchall()
            
            if not records:
                messagebox.showinfo("No Data", "No records found to export.")
                return
            
            # Create workbook and worksheet
            wb = Workbook()
            ws = wb.active
            ws.title = "QR Code Records"
            
            # Define headers
            headers = ['#', 'ID', 'Serial Number', 'Verification Code', 'DevUID', 'QR Code', 'Created At']
            
            # Style for headers
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            # Write headers
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            # Set column widths
            column_widths = [5, 8, 20, 18, 20, 25, 22]
            for col, width in enumerate(column_widths, 1):
                ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = width
            
            # Write data and embed QR codes
            for row_idx, record in enumerate(records, 2):
                # Write sequential number and data
                ws.cell(row=row_idx, column=1, value=row_idx - 1)  # Sequential number (#)
                ws.cell(row=row_idx, column=2, value=record[0])  # ID
                ws.cell(row=row_idx, column=3, value=record[1])  # Serial Number
                ws.cell(row=row_idx, column=4, value=record[2])  # Verification Code
                ws.cell(row=row_idx, column=5, value=record[3])  # DevUID
                
                # Format created_at
                created_at = datetime.fromisoformat(record[5]).strftime("%Y-%m-%d %H:%M:%S")
                ws.cell(row=row_idx, column=7, value=created_at)  # Created At
                
                # Add QR code image if file exists
                qr_filename = record[4]
                if os.path.exists(qr_filename):
                    try:
                        # Insert image into Excel directly
                        img_excel = OpenpyxlImage(qr_filename)
                        
                        # Resize the image in Excel (width and height in points)
                        img_excel.width = 120  # approximately 150 pixels
                        img_excel.height = 120  # approximately 150 pixels
                        
                        # Position the image in the QR Code column (column F)
                        img_excel.anchor = f"F{row_idx}"
                        ws.add_image(img_excel)
                        
                        # Set row height to accommodate image (in points)
                        ws.row_dimensions[row_idx].height = 90
                        
                    except Exception as e:
                        ws.cell(row=row_idx, column=6, value=f"Error loading: {qr_filename}")
                        print(f"Warning: Could not load QR code image {qr_filename}: {e}")
                else:
                    ws.cell(row=row_idx, column=6, value=f"File not found: {qr_filename}")
            
            # Use fixed filename that gets overwritten
            excel_filename = "qr_records.xlsx"
            
            # Save workbook
            wb.save(excel_filename)
            
            # Automatically open the Excel file
            try:
                import subprocess
                import sys
                
                if sys.platform == "darwin":  # macOS
                    subprocess.run(["open", excel_filename])
                elif sys.platform == "win32":  # Windows
                    subprocess.run(["start", excel_filename], shell=True)
                else:  # Linux
                    subprocess.run(["xdg-open", excel_filename])
                    
                print(f"📂 Opened {excel_filename} with default application")
            except Exception as e:
                print(f"⚠️  Could not auto-open file: {e}")
            
            messagebox.showinfo(
                "Export Successful", 
                f"Excel export completed successfully!\n\n"
                f"📁 File: {excel_filename}\n"
                f"📊 Records: {len(records)} exported with QR code images\n"
                f"📂 File opened automatically\n"
                f"📝 Note: File will be overwritten on next export"
            )
            
        except ImportError:
            messagebox.showerror(
                "Missing Dependency", 
                "openpyxl package is required for Excel export.\n\n"
                "Please install it with:\npip install openpyxl"
            )
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export to Excel: {str(e)}")
    
    def export_to_excel_silent(self):
        """Export all records to Excel silently (no dialog boxes)"""
        try:
            from openpyxl import Workbook
            from openpyxl.drawing.image import Image as OpenpyxlImage
            from openpyxl.styles import Font, Alignment, PatternFill
            
            # Fetch all records from database
            self.cursor.execute('''
                SELECT id, serial_number, verification_code, dev_uid, qr_filename, created_at
                FROM qr_records
                ORDER BY created_at ASC
            ''')
            records = self.cursor.fetchall()
            
            if not records:
                return
            
            # Create workbook and worksheet
            wb = Workbook()
            ws = wb.active
            ws.title = "QR Code Records"
            
            # Define headers
            headers = ['#', 'ID', 'Serial Number', 'Verification Code', 'DevUID', 'QR Code', 'Created At']
            
            # Style for headers
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            # Write headers
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=1, column=col, value=header)
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            # Set column widths
            column_widths = [5, 8, 20, 18, 20, 25, 22]
            for col, width in enumerate(column_widths, 1):
                ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = width
            
            # Write data and embed QR codes
            for row_idx, record in enumerate(records, 2):
                # Write sequential number and data
                ws.cell(row=row_idx, column=1, value=row_idx - 1)  # Sequential number (#)
                ws.cell(row=row_idx, column=2, value=record[0])  # ID
                ws.cell(row=row_idx, column=3, value=record[1])  # Serial Number
                ws.cell(row=row_idx, column=4, value=record[2])  # Verification Code
                ws.cell(row=row_idx, column=5, value=record[3])  # DevUID
                
                # Format created_at
                created_at = datetime.fromisoformat(record[5]).strftime("%Y-%m-%d %H:%M:%S")
                ws.cell(row=row_idx, column=7, value=created_at)  # Created At
                
                # Add QR code image if file exists
                qr_filename = record[4]
                if os.path.exists(qr_filename):
                    try:
                        # Insert image into Excel directly
                        img_excel = OpenpyxlImage(qr_filename)
                        
                        # Resize the image in Excel (width and height in points)
                        img_excel.width = 120  # approximately 150 pixels
                        img_excel.height = 120  # approximately 150 pixels
                        
                        # Position the image in the QR Code column (column F)
                        img_excel.anchor = f"F{row_idx}"
                        ws.add_image(img_excel)
                        
                        # Set row height to accommodate image (in points)
                        ws.row_dimensions[row_idx].height = 90
                        
                    except Exception as e:
                        ws.cell(row=row_idx, column=6, value=f"Error loading: {qr_filename}")
                else:
                    ws.cell(row=row_idx, column=6, value=f"File not found: {qr_filename}")
            
            # Use fixed filename that gets overwritten
            excel_filename = "qr_records.xlsx"
            
            # Save workbook
            wb.save(excel_filename)
            print(f"📊 Excel file updated: {excel_filename}")
            
        except ImportError:
            pass  # Silent fail if openpyxl not available
        except Exception as e:
            print(f"Warning: Silent Excel export failed: {e}")
    
    def view_records(self):
        """Open a new window to view all records"""
        records_window = tk.Toplevel(self.root)
        records_window.title("All Records")
        records_window.geometry("900x500")
        
        # Create treeview for all records
        columns = ('ID', 'Serial Number', 'Verification Code', 'DevUID', 'QR Filename', 'Created At')
        records_tree = ttk.Treeview(records_window, columns=columns, show='headings')
        
        # Define headings
        for col in columns:
            records_tree.heading(col, text=col)
            records_tree.column(col, width=140)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(records_window, orient=tk.VERTICAL, command=records_tree.yview)
        h_scrollbar = ttk.Scrollbar(records_window, orient=tk.HORIZONTAL, command=records_tree.xview)
        records_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack widgets
        records_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load all records
        try:
            self.cursor.execute('''
                SELECT id, serial_number, verification_code, dev_uid, qr_filename, created_at
                FROM qr_records
                ORDER BY created_at DESC
            ''')
            all_records = self.cursor.fetchall()
            
            for record in all_records:
                created_at = datetime.fromisoformat(record[5]).strftime("%Y-%m-%d %H:%M:%S")
                records_tree.insert('', 'end', values=(record[0], record[1], record[2], record[3], record[4], created_at))
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load all records: {str(e)}")
    
    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = tk.Tk()
    app = QRGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 