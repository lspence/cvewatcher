from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QComboBox, QPushButton

class CvssseveritySearch(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search by CVSS Severity [PAST 3 MONTHS]")
        self.setFixedSize(300, 50)

        # Setup the Dialog for searching by CVSS Severity.
        layout = QHBoxLayout()
        label_msg = QLabel("CVSS Severity: ")
        self.cvss_severity = QComboBox()
        self.cvss_severity.addItems(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_btn_clicked)
        
        layout.addWidget(label_msg)
        layout.addWidget(self.cvss_severity)
        layout.addWidget(search_btn)
        self.setLayout(layout)

    def search_btn_clicked(self):
        # Accept the dialog, this will return 1 from exec().
        self.accept()
        self.close()

    def get_cvss_severity(self):
        """Return the CVSS Severity text."""
        return self.cvss_severity.currentText()