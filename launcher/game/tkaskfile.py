import sys

# Gtk generally has better support than TKinter on various Linux distributions
def gtk_select_file(title):
    dialog = Gtk.FileChooserNative(title=title,
                                   action=Gtk.FileChooserAction.OPEN)

    dialog.run()

    return dialog.get_filename()

# Fall back to TKinter if Gtk isn't available
def tk_select_file(initialdir, title):
    root = Tk()
    root.withdraw()

    return askopenfilename(initialdir=initialdir, parent=root, title=title, filetypes=(("DDLC ZIP File", "ddlc-win.zip")))

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk

    def select_file(title):
        result = gtk_select_file(title)

        return result if result else ''

except:
# Python3 and Python2-style imports.
    try:
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename
    except ImportError:
        from Tkinter import Tk
        from tkFileDialog import askopenfilename

    def select_file(title):
        return tk_select_file(title, sys.argv[1])

if __name__ == '__main__':
    directory = select_file('Select File')

    sys.stdout.write(directory)
