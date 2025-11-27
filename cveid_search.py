from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton

class CveidSearch(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search by CVE ID")
        self.setFixedSize(300, 50)

        # Setup the Dialog for searching by CVEID.
        layout = QHBoxLayout()
        label_msg = QLabel("CVE ID: ")
        self.cveid = QLineEdit()
        self.cveid.setPlaceholderText("CVE-2002-1492")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_btn_clicked)
        
        layout.addWidget(label_msg)
        layout.addWidget(self.cveid)
        layout.addWidget(search_btn)
        self.setLayout(layout)

    def search_btn_clicked(self):
        # Accept the dialog, this will return 1 from exec().
        self.accept()
        self.close()

    def get_cveid(self):
        """Return the CVE ID text."""
        return self.cveid.text().upper()
    