default persistent.theme = 'light'

init python:
    if persistent.theme == 'dark':
        # The color of non-interactive text.
        TEXT = "#F5F5F5" #545454

        # Colors for buttons in various states.
        IDLE = "#d1d1d1" #42637b
        HOVER = "#78a5c5" #d86b45
        DISABLED = "#6b6b6b" #808080

        # Colors for reversed text buttons (selected list entries).
        REVERSE_IDLE = "#d1d1d1" #78a5c5
        REVERSE_HOVER = "#909090" #d86b45
        REVERSE_TEXT = "#111" #ffffff

        # Colors for the scrollbar thumb.
        SCROLLBAR_IDLE = "#5c6e91" #dfdfdf
        SCROLLBAR_HOVER = "#31326f" #d86b45
        # An image used as a separator pattern.
        PATTERN = "images/pattern.png"

        # A displayable used for the background of everything.
        BACKGROUND = Solid('#393e46')

        # A displayable used for the background of windows
        # containing commands, preferences, and navigation info.
        WINDOW = Frame("window_dark.png", 0, 0, tile=True) #ffffff80

        # A displayable used for the background of the projects list.
        PROJECTS_WINDOW = Null()

        # A displayable used the background of information boxes.
        INFO_WINDOW = "#393e46" #f9f9f9c0

        # Colors for the titles of information boxes.
        ERROR_COLOR = "#f05454" #d15353
        INFO_COLOR = "#34626c" #545454
        INTERACTION_COLOR = "#9E9E9E" #d19753
        QUESTION_COLOR = "#f5b461" #d19753

        # The color of input text.
        INPUT_COLOR = "#FAFAFA" #d86b45