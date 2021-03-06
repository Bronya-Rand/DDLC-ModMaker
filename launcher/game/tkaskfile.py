import sys

# Python3 and Python2-style imports.
try:
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
except ImportError:
    from Tkinter import Tk
    from tkFileDialog import askopenfilename

# Binary mode stdout for python3.
try:
    sys.stdout = sys.stdout.buffer
except:
    pass

# Create the TK canvas.

if __name__ == "__main__":
    root = Tk()
    root.withdraw()

    result = askopenfilename(initialdir=sys.argv[1], parent=root, title="Select File")

    if result == ():
        result = ""

    sys.stdout.write(result.encode("utf8"))