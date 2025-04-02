import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget,
    QLineEdit, QInputDialog, QMessageBox, QHBoxLayout, QDateEdit, QTimeEdit
)
from PyQt6.QtCore import QDate, QTime
from db import add_task, get_tasks, update_task, delete_task


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To-Do App")
        self.setGeometry(200, 200, 500, 400)

        self.layout = QVBoxLayout()

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter a new task")
        self.layout.addWidget(self.task_input)

        # Layout for Date and Time
        self.datetime_layout = QHBoxLayout()

        # Date Picker (Calendar)
        self.date_picker = QDateEdit(self)
        self.date_picker.setCalendarPopup(True)  # Show full calendar
        self.date_picker.setDate(QDate.currentDate())  # Default to today
        self.datetime_layout.addWidget(self.date_picker)

        # Time Picker (Digital Clock)
        self.time_picker = QTimeEdit(self)
        self.time_picker.setTime(QTime.currentTime())  # Default to now
        self.datetime_layout.addWidget(self.time_picker)

        self.layout.addLayout(self.datetime_layout)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_button)

        self.task_list = QListWidget()
        self.task_list.itemDoubleClicked.connect(self.edit_task)  # Double-click to edit
        self.layout.addWidget(self.task_list)

        self.delete_button = QPushButton("Delete Task")
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

        self.load_tasks()
        self.setLayout(self.layout)

    def add_task(self):
        task = self.task_input.text()
        if task:
            due_date = self.date_picker.date().toString("yyyy-MM-dd")
            due_time = self.time_picker.time().toString("hh:mm AP")
            due_datetime = f"{due_date} at {due_time}"

            add_task(task, due_datetime)
            self.task_list.addItem(f"{task} - Due: {due_datetime}")
            self.task_input.clear()

    def load_tasks(self):
        self.task_list.clear()
        tasks = get_tasks()
        for task in tasks:
            self.task_list.addItem(f"{task[1]} - Due: {task[2]}")

    def edit_task(self, item):
        old_task = item.text().split(" - Due: ")[0]
        new_task, ok = QInputDialog.getText(self, "Edit Task", "Modify your task:", text=old_task)
        if ok and new_task:
            update_task(old_task, new_task)
            self.load_tasks()

    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_text = selected_item.text().split(" - Due: ")[0]
            reply = QMessageBox.question(self, "Delete Task", f"Are you sure you want to delete '{task_text}'?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                delete_task(task_text)
                self.load_tasks()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())
