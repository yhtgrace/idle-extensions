""" idle extension to run pep8 style-check from menu"""

from idlelib.OutputWindow import OutputWindow
import subprocess as sub


class StyleCheck:   # must be the same name as the file for EditorWindow.py
                    # to load it.

    menudefs = [
        ('run', [
            ('!Style Check', '<<style-check>>'),
        ])
    ]

    def __init__(self, editwin):
        self.editwin = editwin      # reference to the editor window
        self.text = self.editwin.text
        self.text.bind("<<style-check>>", self.check_style)

    def check_style(self, ev=None):
        """ Runs pep8 stylecheck, captures output and prints to new
            output window."""

        filename = self.editwin.io.filename

        if not filename:
            output_short = 'Save your module first!\n' \
                           'Or, you could be running this' \
                           ' style check in the wrong window.'
        elif filename[-2:] != 'py':
            output_short = "This is not a python file."
        else:
            try:
                p = sub.Popen(['blah', filename],
                              stdout=sub.PIPE, stderr=sub.PIPE)
                output, errors = p.communicate()

                if output.strip():
                    output_short = '\n'.join(
                        [line.split('/')[-1]
                         for line in output.split('\n')[:-1]])
                    # shorten pathname in each line of output
                else:
                    output_short = "Passed all checks!"
            except OSError:
                output_short = "Please install pep8."

        win = OutputWindow(self.editwin.flist)
        win.write(output_short)


# for compatiblity with IdleX
config_extension_def = """
[StyleCheck]
enable=1
enable_editor=1
enable_shell=0
"""
