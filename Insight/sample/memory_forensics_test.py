import sys
import pytest
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtTest import QTest

from memory_forensics import MemoryForensicsApp

@pytest.fixture
def app(qtbot):
    test_app = QApplication(sys.argv)
    widget = MemoryForensicsApp()
    widget.show()
    qtbot.addWidget(widget)
    return qtbot, test_app, widget

def test_show_running_processes(app):
    qtbot, test_app, widget = app

    # Click the "Show Running Processes" button
    with qtbot.waitSignal(widget.back_button.clicked):
        widget.show_running_processes()

    # Ensure that the process list is not empty
    assert widget.process_list.toPlainText() != ''

def test_analyze_memory_dump_successful(app, monkeypatch):
    qtbot, test_app, widget = app

    # Mock the QFileDialog.getOpenFileName method
    monkeypatch.setattr(QFileDialog, 'getOpenFileName', lambda *args, **kwargs: ('path/to/dump.dmp', ''))

    # Set text in the plugin input field
    QTest.keyClicks(widget.plugin_input, 'pslist')

    # Click the "Analyze Memory Dump" button
    with qtbot.waitSignal(widget.back_button.clicked):
        widget.analyze_memory_dump()

    # Ensure that the process list is not empty
    assert widget.process_list.toPlainText() != ''

def test_analyze_memory_dump_failure(app, monkeypatch):
    qtbot, test_app, widget = app

    # Mock the QFileDialog.getOpenFileName method
    monkeypatch.setattr(QFileDialog, 'getOpenFileName', lambda *args, **kwargs: ('path/to/invalid_dump.txt', ''))

    # Set text in the plugin input field
    QTest.keyClicks(widget.plugin_input, 'pslist')

    # Click the "Analyze Memory Dump" button
    with qtbot.waitSignal(widget.back_button.clicked):
        widget.analyze_memory_dump()

    # Ensure that the process list contains an error message
    assert 'Error' in widget.process_list.toPlainText()

if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "test_memory_forensics_app.py"])
