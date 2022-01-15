﻿# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init python:

    def directory_is_writable(path):
        test = os.path.join(path, "renpy test do not use")

        try:
            if os.path.isdir(test):
                os.rmdir(test)

            os.mkdir(test)
            os.rmdir(test)

            return True

        except:
            return False

    def choose_directory(path):
        """
        Pops up a directory chooser.

        `path`
            The directory that is selected by default. If None, config.renpy_base
            is selected.

        Returns a (path, is_default) tuple, where path is the chosen directory,
        and is_default is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if path:
            default_path = path
        else:
            try:
                default_path = os.path.dirname(os.path.abspath(config.renpy_base))
            except:
                default_path = os.path.abspath(config.renpy_base)

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_path, wanted=unicode)

            if choice is not None:
                path = choice
            else:
                path = None

        else:

            try:

                if renpy.macintosh:
                    # tkinter is broken on Python 3, so use it as a last resort - maybe apple fixed it?
                    system_pythons = [ "/usr/bin/python2", "/usr/bin/python"]
                else:
                    system_pythons = [ "/usr/bin/python2", "/usr/bin/python" ]

                for system_python in system_pythons:
                    if os.path.exists(system_python):
                        break
                else:
                    system_python = system_pythons[0]

                cmd = [ system_python, os.path.join(config.gamedir, "tkaskdir.py"), renpy.fsencode(default_path) ]

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                choice = p.stdout.read()
                code = p.wait()

            except:
                import traceback
                traceback.print_exc()

                code = 0
                choice = ""
                path = None

                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            if code:
                interface.error(_("Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."), label=None)

            elif choice:
                path = choice.decode("utf-8")

        is_default = False

        if path is None:
            path = default_path
            is_default = True

        path = renpy.fsdecode(path)

        if (not os.path.isdir(path)) or (not directory_is_writable(path)):
            interface.error(_("The selected projects directory is not writable."))
            path = default_path
            is_default = True

        if is_default and (not directory_is_writable(path)):
            path = os.path.expanduser("~")

        return path, is_default

    def choose_file(path, mod=False):
        """
        Pops up a directory chooser.

        `path`
            The directory that is selected by default. If None, config.renpy_base
            is selected.

        Returns a (path, is_default) tuple, where path is the chosen directory,
        and is_default is true if and only if it was chosen by default mechanism
        rather than user choice.
        """

        if path:
            default_path = path
        else:
            try:
                default_path = os.path.dirname(os.path.abspath(config.renpy_base))
            except:
                default_path = os.path.abspath(config.renpy_base)

        if EasyDialogs:

            if not mod:
                choice = EasyDialogs.AskFileForOpen(typeList=[('DDLC ZIP File', '*.zip')], defaultLocation=default_path, windowTitle="Select DDLC ZIP File", wanted=unicode)
            else:
                choice = EasyDialogs.AskFileForOpen(typeList=[('DDLC Mod File', '*.zip')], defaultLocation=default_path, windowTitle="Select Mod ZIP File", wanted=unicode)

            if choice is not None:
                path = choice
            else:
                path = None

        else:

            try:

                if renpy.macintosh:
                    # tkinter is broken on Python 3, so use it as a last resort - maybe apple fixed it?
                    system_pythons = [ "/usr/bin/python2", "/usr/bin/python"]
                else:
                    system_pythons = [ "/usr/bin/python2", "/usr/bin/python" ]

                for system_python in system_pythons:
                    if os.path.exists(system_python):
                        break
                else:
                    system_python = system_pythons[0]
                    
                cmd = [ system_python, os.path.join(config.gamedir, "tkaskfile.py"), renpy.fsencode(default_path) ]

                p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                choice = p.stdout.read()
                code = p.wait()

            except:
                import traceback
                traceback.print_exc()

                code = 0
                choice = ""
                path = None

                interface.error(_("Ren'Py was unable to run python with tkinter to choose the file. Please install python and either the python-tk or tkinter package."), label=None)

            if code:
                interface.error(_("Ren'Py was unable to run python with tkinter to choose the file. Please install python and either the python-tk or tkinter package."), label=None)

            elif choice:
                path = choice.decode("utf-8")

        is_default = False

        if path is None:
            path = default_path
            is_default = True

        path = renpy.fsdecode(path)

        return path, is_default
