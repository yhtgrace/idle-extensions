""" Idle extension to run doctests from menu"""

from idlelib.OutputWindow import OutputWindow
import StringIO
import subprocess as sub
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

        filename = self.editwin.io.filename

        if not filename:
            output = 'Save your module first!\n' \
                     'Or you may be running doctests in the wrong window.'
        elif filename[-2:] != 'py':
                output = 'This is not a python module!'
        else:
                p = sub.Popen(['python', '-m', 'doctest', '-v', filename],
                                stdout=sub.PIPE, stderr=sub.PIPE)
                output, errors = p.communicate()

        win = OutputWindow(self.editwin.flist)
        win.write(output)  # write to output window

# for compatiblity with IdleX
config_extension_def = """
[DocTest]
enable=1
enable_editor=1
enable_shell=0
visible=True
"""
