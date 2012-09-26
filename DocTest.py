""" Idle extension to run doctests from menu"""

from idlelib.OutputWindow import OutputWindow
import StringIO
import doctest
import sys


class DocTest:      # must be the same name as the file for EditorWindow.py
                    # to load it.

    menudefs = [
        ('run', [
            ('Doc Test', '<<doc-test>>'),
        ])
    ]

    def __init__(self, editwin):
        self.editwin = editwin      # reference to the editor window
        self.text = self.editwin.text
        self.text.bind("<<doc-test>>", self.doc_test)

    def doc_test(self, ev=None):
        """ Run doctests on the current module"""

        sys.stdout = capture = StringIO.StringIO()  # capture verbose report

        filename = self.editwin.io.filename
        if filename:
            failure_count, test_count = doctest.testfile(filename,
                                                         module_relative=False,
                                                         verbose=True,
                                                         report=True)
            output = capture.getvalue()
        else:
            output = 'Save your module first!\n' \
                     'Or you may be running doctests in the wrong window.'

        win = OutputWindow(self.editwin.flist)
        win.write(output)  # and write to new output window instead


# for compatiblity with IdleX
config_extension_def = """
[DocTest]
enable=1
enable_editor=1
enable_shell=0
visible=True
"""
