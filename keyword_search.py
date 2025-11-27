from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton

class KeywordSearch(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search by Keyword")
        self.setFixedSize(300, 50)

        # Setup the Dialog for searching by keyword.
        layout = QHBoxLayout()
        label_msg = QLabel("CVE Keyword: ")
        self.keyword = QLineEdit()
        self.keyword.setPlaceholderText("Microsoft")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_btn_clicked)
        
        layout.addWidget(label_msg)
        layout.addWidget(self.keyword)
        layout.addWidget(search_btn)
        self.setLayout(layout)

    def search_btn_clicked(self):
        # Accept the dialog, this will return 1 from exec().
        self.accept()
        self.close()

    def get_keyword_results(self):
        """Return the CVEs matching the keyword(s)."""
        return self.keyword.text()