import requests
import resource_rc

from PySide6.QtCore import Qt, QTimer, QRect, QUrl, QEvent
from PySide6.QtGui import QIcon, QColor, QFont, QPainter, QDesktopServices
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QTableView, QHeaderView, QFileDialog, QMessageBox, QApplication

from ui_mainwindow import Ui_MainWindow
from cveid_search import CveidSearch
from cvss_severity_search import CvssseveritySearch
from keyword_search import KeywordSearch

from datetime import datetime, timedelta, timezone
from functools import wraps

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(':/icon/cve-watcher.ico'))
        self.setFixedSize(1024, 768)
        self.app = app

        # Initialize current_refresh_hours.
        self.current_refresh_hours = None

        self.cve_id_font = QFont("Arial", 10, QFont.Weight.Normal, True)
        self.bold_font = QFont()
        self.bold_font.setBold(True)

        # Cache PDF fonts.
        self.pdf_fonts = {
            'normal': QFont("Arial", 9),
            'bold': QFont("Arial", 9),
            'underline': QFont("Arial", 9),
            'header': QFont("Arial", 10),
            'title': QFont("Arial", 26),
            'subtitle': QFont("Arial", 14),
            'page_number': QFont("Arial", 12)
        }

        self.pdf_fonts['bold'].setBold(True)
        self.pdf_fonts['underline'].setUnderline(True)
        self.pdf_fonts['header'].setBold(True)
        self.pdf_fonts['title'].setBold(True)

        # Cache severity colors used for the display and PDF.
        self.pdf_severity_colors = {
            "CRITICAL": QColor(196, 51, 51),
            "HIGH": QColor(242, 154, 21),
            "MEDIUM": QColor(107, 107, 99),
            "LOW": QColor(21, 39, 189),
            "N/A": QColor(0, 0, 0)
        }

        self.severity_colors = {
            "CRITICAL": QColor.fromRgb(196, 51, 51),
            "HIGH": QColor.fromRgb(242, 154, 21),
            "MEDIUM": QColor.fromRgb(107, 107, 99),
            "LOW": QColor.fromRgb(21, 39, 189),
            "N/A": QColor.fromRgb(0, 0, 0)
        }

        # Setup table columns.
        self.tableWidget.setColumnWidth(0, 40)
        self.tableWidget.setColumnWidth(1, 60)
        self.tableWidget.setColumnWidth(2, 125)
        self.tableWidget.setColumnWidth(3, 550)
        self.tableWidget.setColumnWidth(4, 75)
        self.tableWidget.setColumnWidth(5, 175)

        # Hide the first column of the table.
        self.tableWidget.verticalHeader().hide()

        # Prevent the columns from being resized.
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        # Setup default column sorting order.
        self.current_sort_column = -1
        self.current_sort_order = Qt.SortOrder.AscendingOrder

        self.setup_table_appearance()
        self.setup_sorting()
        
        # Initial data load.
        self.load_data(None, None, None)
        
        # Setup timer for data refresh.
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.load_data(None, None, None))

        # Setup up menu options.
        self.actionExport_to_Pdf.triggered.connect(self.export_to_pdf)
        self.actionQuit.triggered.connect(self.quit)
        self.actionCVE_Id.triggered.connect(self.search_by_cveid)
        self.actionCVSS_Severity.triggered.connect(self.search_by_cvss_severity)
        self.actionKeyword_Search.triggered.connect(self.search_by_keyword)
        self.actionReload_Last_24_Hours.triggered.connect(self.reload_last_24_hours)
        self.action1Hour.triggered.connect(self.interval_1_Hour)
        self.action4Hours.triggered.connect(self.interval_4_Hours)
        self.action8Hours.triggered.connect(self.interval_8_Hours)
        self.action24Hours.triggered.connect(self.interval_24_Hours)
        self.actionAbout.triggered.connect(self.about)

        # Connect item clicked signal.
        self.tableWidget.itemClicked.connect(self.handle_item_clicked)

        # Set cursor for CVE ID column.
        self.tableWidget.viewport().installEventFilter(self)

    def setup_table_appearance(self):
        self.tableWidget.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #e4f0e8;
                background-color: #c4e6c1;
                gridline-color: #d0d0d0;
            }
            QTableWidget::item:selected {
                background-color: #bfbfBd;
                color: #000000;
            }
            QTableWidget::item:hover {
                background-color: #f7f7c1;  
            }
        """)
        self.tableWidget.setSortingEnabled(False)
    
    def setup_sorting(self):
        self.sortable_columns = [1, 2, 4, 5]  # Base Score, CVE ID, Base Severity, Publish Date.
        
        header = self.tableWidget.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(-1, Qt.SortOrder.AscendingOrder)
        header.sectionClicked.connect(lambda col: self.handle_column_sort(col, self.sortable_columns))
    
    def handle_request_exceptions(func):
        """Decorator to handle HTTP request exceptions with error messages."""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except requests.exceptions.HTTPError as http_error:
                response = http_error.response
                status_code = response.status_code
                error_messages = {
                    400: "Bad http request made!",
                    401: "Unauthorized: Invalid API key!",
                    403: "Forbidden: Access denied!",
                    404: "Invalid url data not found!",
                    500: "Status code 500: Internal server error!",
                    502: "Bad gateway: Invalid response from server!",
                    503: "Service unavailable!",
                    504: "Gateway timeout: No response from server!"
                }

                message = error_messages.get(status_code, f"HTTP error occurred.\n{http_error}")
                self.display_error(message)
                return None
                
            except requests.exceptions.ConnectionError:
                self.display_error("Connection error: No internet access!")
                return None
                
            except requests.exceptions.Timeout:
                self.display_error("Timeout error: Request timed out.")
                return None
                
            except requests.exceptions.TooManyRedirects:
                self.display_error("Too many redirects: Verify url.")
                return None
                
            except requests.exceptions.RequestException as req_error:
                self.display_error(f"Request error:\n{req_error}.")
                return None
        
        return wrapper
    
    def extract_base_score(self, metrics):
        """Extract base score from metrics, trying different CVSS versions."""
        for version in ['cvssMetricV40', 'cvssMetricV31', 'cvssMetricV30', 'cvssMetricV2']:
            if version in metrics and len(metrics[version]) > 0:
                try:
                    return metrics[version][0]['cvssData']['baseScore']
                except (KeyError, IndexError):
                    continue
        return "N/A"

    def extract_base_severity(self, metrics):
        """Extract base severity from metrics, trying different CVSS versions."""
        for version in ['cvssMetricV40', 'cvssMetricV31', 'cvssMetricV30', 'cvssMetricV2']:
            if version in metrics and len(metrics[version]) > 0:
                try:
                    return metrics[version][0]['cvssData']['baseSeverity']
                except (KeyError, IndexError):
                    continue
        return "N/A"    
    
    def create_table_item(self, value, alignment=Qt.AlignmentFlag.AlignCenter):
        """Create a table item with alignment."""
        item = QTableWidgetItem(str(value))
        item.setTextAlignment(alignment)
        return item
    
    def filter_by_severity(self, vulnerabilities, target_severity):
        """Filter vulnerabilities to only include exact severity matches."""
        filtered = []

        for vuln in vulnerabilities:
            cve_info = vuln.get('cve', {})
            metrics = cve_info.get('metrics', {})
            severity = self.extract_base_severity(metrics)
            
            if severity.upper() == target_severity.upper():
                filtered.append(vuln)
        
        return filtered

    def load_data(self, cveid, cvss_severity, keyword):
        """Load CVE data and populate the table."""
        if cveid is None and cvss_severity is None and keyword is None:
            cve_data = self.get_data()
        elif cveid is not None and cvss_severity is None and keyword is None:
            cve_data = self.get_cve_by_id(cveid)
        elif cveid is None and cvss_severity is not None and keyword is None:
            cve_data = self.get_cvss_by_severity(cvss_severity)
        else:
            cve_data = self.get_by_keyword(keyword)
    
        if cve_data is None:
            self.display_error("Failed to retrieve CVE data.")
            return
        
        self.tableWidget.clearContents()
        self.tableWidget.clearSelection()
        
        vulnerabilities = cve_data.get('vulnerabilities', [])
        
        # Filter by severity if searching by severity.
        if cvss_severity:
            vulnerabilities = self.filter_by_severity(vulnerabilities, cvss_severity)
            
            if not vulnerabilities:
                self.display_error(f"No CVEs found with exact {cvss_severity} severity.")
                self.tableWidget.setRowCount(0)
                return
            
            self.statusBar().showMessage(
                f"Displaying {len(vulnerabilities)} {cvss_severity} CVEs", 
                5000
            )
        
        self.tableWidget.setUpdatesEnabled(False)
        
        try:
            self.tableWidget.setRowCount(len(vulnerabilities))
            
            for row, cve in enumerate(vulnerabilities):
                cve_info = cve.get('cve', {})
                
                self.tableWidget.setItem(row, 0, self.create_table_item(row))
                
                metrics = cve_info.get('metrics', {})
                base_score = self.extract_base_score(metrics)
                
                item = QTableWidgetItem()

                if base_score != "N/A":
                    item.setData(Qt.ItemDataRole.DisplayRole, float(base_score))
                else:
                    item.setData(Qt.ItemDataRole.DisplayRole, base_score)

                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(row, 1, item)
                
                cve_id = cve_info.get('id', '')
                item = self.create_table_item(cve_id)
                item.setForeground(QColor(0, 0, 255))
                item.setFont(self.cve_id_font)  
                self.tableWidget.setItem(row, 2, item)
                
                descriptions = cve_info.get('descriptions', [])
                description = descriptions[0]['value'] if descriptions else "No description available."
                self.tableWidget.setItem(row, 3, self.create_table_item(description, Qt.AlignmentFlag.AlignLeft))
                
                base_severity = self.extract_base_severity(metrics)
                item = QTableWidgetItem(str(base_severity))
                item.setForeground(self.severity_colors.get(base_severity, self.severity_colors["N/A"]))
                item.setFont(self.bold_font)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(row, 4, item)
                
                published = cve_info.get('published', '')
                formatted_date = published[:10] if len(published) >= 10 else "N/A"
                self.tableWidget.setItem(row, 5, self.create_table_item(formatted_date))
                
                self.tableWidget.setRowHeight(row, 100)
        finally:
            self.tableWidget.setUpdatesEnabled(True)
    
    def display_error(self, message):
        """Display error message in status bar for 15 seconds."""
        self.statusBar().showMessage(message, 15000)

        # Restore refresh interval message after error clears.
        if self.current_refresh_hours is not None:
            QTimer.singleShot(15100, lambda: self.statusBar().showMessage(f"Auto-refresh: Every {self.current_refresh_hours} hour(s)"))
    
    def handle_column_sort(self, column, sortable_columns):
        """Custom handler to only allow sorting on specific columns."""
        if column not in sortable_columns:
            header = self.tableWidget.horizontalHeader()
            header.setSortIndicator(-1, Qt.SortOrder.AscendingOrder)
            return
        
        # Toggle sort order.
        if self.current_sort_column == column:
            new_order = (Qt.SortOrder.DescendingOrder if self.current_sort_order == Qt.SortOrder.AscendingOrder 
                        else Qt.SortOrder.AscendingOrder)
        else:
            new_order = Qt.SortOrder.AscendingOrder
        
        # Sort the table.
        self.tableWidget.sortItems(column, new_order)
        
        # Update state.
        self.current_sort_column = column
        self.current_sort_order = new_order
        
        # Update indicator.
        self.tableWidget.horizontalHeader().setSortIndicator(column, new_order)

    def eventFilter(self, obj, event):
        """Filter events to change cursor on CVE ID column."""
        if obj == self.tableWidget.viewport():
            if event.type() == QEvent.Type.MouseMove:
                index = self.tableWidget.indexAt(event.pos())
                if index.column() == 2:  # CVE ID column.
                    self.tableWidget.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
                else:
                    self.tableWidget.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        
        return super().eventFilter(obj, event)

    def handle_item_clicked(self, item):
        """Handle clicks on table items."""
        if item.column() == 2:  # CVE ID column.
            cve_id = item.text()
            if cve_id and cve_id.startswith('CVE-'):
                url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
                QDesktopServices.openUrl(QUrl(url))
                self.statusBar().showMessage(f"Opening {cve_id} in browser...", 3000)
    
    def quit(self):
        """Quit the application."""
        self.timer.stop()
        self.app.quit()

    def set_refresh_interval(self, hours):
        """Set the refresh interval in hours."""
        self.current_refresh_hours = hours
        milliseconds = hours * 60 * 60 * 1000
        self.timer.stop()
        self.timer.setInterval(milliseconds)
        self.timer.start()
        self.load_data(None, None, None)
        self.statusBar().showMessage(f"Auto-refresh: Every {hours} hour(s)")
    
    def print_widget(self, widget, filename):
        """Render ALL tableWidget contents to PDF by painting each cell."""
        try:
            # Add early exit for empty table.
            if widget.rowCount() == 0:
                self.display_error("No data to export.")
                return False
        
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)
            
            QApplication.processEvents()

            painter = QPainter()

            if not painter.begin(printer):
                return False
        
            page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
            page_width = int(page_rect.width())
            page_height = int(page_rect.height())
            
            margin = int(page_width * 0.02)
            row_height = int(page_height * 0.085)  
            header_height = int(page_height * 0.035)  
            available_width = page_width - (2.5 * margin)
        
            col_widths = [
                int(available_width * 0.03),   # Column 0: # (3%).
                int(available_width * 0.06),   # Column 1: Score (6%).
                int(available_width * 0.14),   # Column 2: CVE ID (14%).
                int(available_width * 0.550),  # Column 3: Description (55.0%).
                int(available_width * 0.09),   # Column 4: Severity (9%).
                int(available_width * 0.14),   # Column 5: Date Published (14%).
            ]
        
            # Draw.
            painter.setFont(self.pdf_fonts['title'])
            painter.setPen(QColor(0, 0, 0))
            
            title_y = int(page_height * 0.013)
            title_height = int(page_height * 0.03)
            title_rect = QRect(margin, title_y, page_width - (2 * margin), title_height)
            painter.drawText(title_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, "CVE Watcher Report")
            
            # Subtitle.
            painter.setFont(self.pdf_fonts['subtitle'])
        
            subtitle_y = title_y + title_height + int(page_height * 0.003)
            subtitle_height = int(page_height * 0.025)
            subtitle_rect = QRect(margin, subtitle_y, page_width - (2 * margin), subtitle_height)
            painter.drawText(subtitle_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, 
                            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total: {widget.rowCount()} CVEs")
        
            # Helper function to draw header.
            def draw_header(y_position):
                header_x = margin
                painter.setPen(QColor(0, 0, 0))
                painter.setFont(self.pdf_fonts['header'])
                
                for col in range(widget.columnCount()):
                    header_rect = QRect(header_x, y_position, col_widths[col], header_height)
                    painter.fillRect(header_rect, QColor(180, 180, 180))
                    painter.setPen(QColor(100, 100, 100))
                    painter.drawRect(header_rect)
                    painter.setPen(QColor(0, 0, 0))
                    
                    header_text = widget.horizontalHeaderItem(col).text() if widget.horizontalHeaderItem(col) else ""

                    # Better padding for header text to prevent cutoff.
                    text_rect = header_rect.adjusted(12, 12, -12, -12)
                    painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, header_text)
                    
                    header_x += col_widths[col]
                
                return y_position + header_height
        
            # Start drawing table.
            current_y = subtitle_y + subtitle_height + int(page_height * 0.025)
            current_y = draw_header(current_y)
            
            page_num = 1
        
            # Draw each.
            for row in range(widget.rowCount()):
                # Check if we need a new page.
                space_needed = row_height + int(margin * 1.5)
                space_available = page_height - current_y
                
                if space_available < space_needed:
                    if not printer.newPage():
                        break
                    
                    page_num += 1
                    current_y = margin
                    
                    # Page number - positioned higher and further from right edge.
                    painter.setFont(self.pdf_fonts['page_number'])
                    painter.setPen(QColor(100, 100, 100))
                    
                    # Position page number with proper margins.
                    page_num_x = int(page_width * 0.70)
                    page_num_y = current_y + int(page_height * 0.01)
                    page_num_width = int(page_width * 0.25)
                    page_num_height = int(page_height * 0.05)
                    
                    painter.drawText(page_num_x, page_num_y, page_num_width, page_num_height,
                                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop, 
                                f"Page {page_num}")
                    
                    current_y += page_num_height + int(page_height * 0.02)
                    
                    # Draw header on new page.
                    current_y = draw_header(current_y)
                
                # Draw cells in this row.
                cell_x = margin
                
                # Alternate row colors.
                row_bg_color = QColor(228, 240, 232) if row % 2 == 0 else QColor(196, 230, 193)
                
                for col in range(widget.columnCount()):
                    cell_rect = QRect(cell_x, current_y, col_widths[col], row_height)
                    
                    # Fill background.
                    painter.fillRect(cell_rect, row_bg_color)
                    
                    # Draw border.
                    painter.setPen(QColor(208, 208, 208))
                    painter.drawRect(cell_rect)
                    
                    # Get cell item.
                    item = widget.item(row, col)
                    if item:
                        text = item.text()
                        
                        # Set text color and font based on column.
                        if col == 4:  # Severity column.
                            painter.setPen(self.pdf_severity_colors.get(text, QColor(0, 0, 0)))
                            painter.setFont(self.pdf_fonts['bold'])
                        elif col == 2:  # CVE ID column.
                            painter.setPen(QColor(0, 0, 255))
                            painter.setFont(self.pdf_fonts['underline'])
                        else:
                            painter.setPen(QColor(0, 0, 0))
                            painter.setFont(self.pdf_fonts['normal'])
                        
                        # Better padding to prevent cutoff.
                        if col == 3:  # Description.
                            text_rect = cell_rect.adjusted(20, 15, -20, -15)
                        elif col == 0:  
                            text_rect = cell_rect.adjusted(8, 10, -8, -10)
                        else:  # Score, CVE ID, Severity, Date.
                            text_rect = cell_rect.adjusted(12, 10, -12, -10)
                        
                        # Draw text.
                        if col == 3:  # Description - word wrap.
                            painter.drawText(text_rect, 
                                        Qt.TextFlag.TextWordWrap | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, 
                                        text)
                        else:
                            painter.drawText(text_rect, 
                                        Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, 
                                        text)
                    
                    cell_x += col_widths[col]
                
                current_y += row_height
            
            painter.end()
            
            return True
        except Exception as e:
            self.display_error(f"PDF generation error: {str(e)}")
            return False
    
    def pdf_export(self, widget):
        """Show the save dialog and export widget to PDF."""
        fn, _ = QFileDialog.getSaveFileName(
            self, 
            "Export PDF", 
            "CVE_Report.pdf", 
            "PDF files (*.pdf);;All Files (*)"
        )

        if fn:
            if not fn.endswith('.pdf'):
                fn += '.pdf'

            try:
                success = self.print_widget(widget, fn)

                if success:
                    self.statusBar().showMessage(f"Exported to {fn}", 5000)
                else:
                    self.statusBar().showMessage("Export failed.", 5000)
            except Exception as e:
                self.statusBar().showMessage(f"Export failed: {str(e)}", 5000)
    
    def export_to_pdf(self):
        self.pdf_export(self.tableWidget)
    
    def search_by_cveid(self):
        dlg = CveidSearch()
        
        if dlg.exec():
            cveid = dlg.get_cveid().strip()

            if cveid:
                self.statusBar().showMessage(f"Searching for {cveid}...", 3000)
                self.load_data(cveid, None, None) 
            else:
                self.statusBar().showMessage("Please enter a CVE ID", 3000)
    
    def search_by_cvss_severity(self):
        dlg = CvssseveritySearch()
        
        if dlg.exec():
            cvss_severity_level = dlg.get_cvss_severity().strip()

            if cvss_severity_level:
                self.statusBar().showMessage(f"Searching for {cvss_severity_level} severity CVEs...", 3000)
                self.load_data(None, cvss_severity_level, None)
            else:
                self.statusBar().showMessage("Please select a CVSS Severity", 3000)
    
    def search_by_keyword(self):
        dlg = KeywordSearch()

        if dlg.exec():
            cve_keyword_result = dlg.get_keyword_results().strip()

            if cve_keyword_result:
                self.statusBar().showMessage(f"Searching for cves containing {cve_keyword_result}...", 3000)
                self.load_data(None, None, cve_keyword_result) 
            else:
                self.statusBar().showMessage("Please enter a keyword (e.g. Microsoft)", 3000)

    def reload_last_24_hours(self):
        self.load_data(None, None, None)
    
    @handle_request_exceptions
    def get_data(self):
        """Get CVEs published within the last 24 hours."""
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=1)

        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate={start_date.strftime('%Y-%m-%dT%H:%M:%S.000')}&pubEndDate={end_date.strftime('%Y-%m-%dT%H:%M:%S.000')}&resultsPerPage=100&startIndex=0"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    @handle_request_exceptions
    def get_cve_by_id(self, cve_id):
        """Get details for a specific CVE."""
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    @handle_request_exceptions
    def get_cvss_by_severity(self, cvss_severity):
        """Get CVEs by CVSS severity level."""
        # Map user input to API parameter.
        severity_map = {
            "LOW": "LOW",
            "MEDIUM": "MEDIUM", 
            "HIGH": "HIGH",
            "CRITICAL": "CRITICAL"
        }
        
        severity = severity_map.get(cvss_severity.upper())
        
        if not severity:
            self.display_error(f"Invalid severity: {cvss_severity}.")
            return None
        
        # Get CVEs from last 120 days with specified severity.
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=120)
        
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0/?cvssV3Severity={severity}&pubStartDate={start_date.strftime('%Y-%m-%dT%H:%M:%S.000')}&pubEndDate={end_date.strftime('%Y-%m-%dT%H:%M:%S.000')}&resultsPerPage=100&startIndex=0"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    @handle_request_exceptions
    def get_by_keyword(self, keyword):
        """Get details for the specific keyword(s) and limit results to 100."""
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=100&startIndex=0"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def interval_1_Hour(self):
        self.set_refresh_interval(1)

    def interval_4_Hours(self):
        self.set_refresh_interval(4)

    def interval_8_Hours(self):
        self.set_refresh_interval(8)

    def interval_24_Hours(self):
        self.set_refresh_interval(24)
    
    def about(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("CVE Watcher v1.0.0")
        msg_box.setTextFormat(Qt.TextFormat.RichText)
        msg_box.setText("This product uses data from the NVD API but is not endorsed or certified by the NVD.\n\n" \
                        "Data source and more information is available at <a href=\"https://nvd.nist.gov\" target=\"_blank\">https://nvd.nist.gov.</a>"
                        )
        msg_box.exec()
