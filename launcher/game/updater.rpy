# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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
    # This can be one of None, "available", "not-available", or "error".
    #
    # It must be None for a release.
    UPDATE_SIMULATE = None

    PUBLIC_KEY = "renpy_public.pem"

    CHANNELS_URL = "https://www.renpy.org/channels.json"

    version_tuple = renpy.version(tuple=True)

    def check_dlc(name):
        """
        Returns true if the named dlc package is present.
        """

        return name in updater.get_installed_packages()

    def add_dlc(name, restart=False):
        """
        Adds the DLC package, if it doesn't already exist.

        Returns True if the DLC is installed, False otherwise.
        """

        dlc_url = "http://update.renpy.org/7.4.4/updates.json"

        return renpy.invoke_in_new_context(updater.update, dlc_url, add=[name], public_key=PUBLIC_KEY, simulate=UPDATE_SIMULATE, restart=restart)

    def add_rapt(name, restart=False):
        """
        Adds RAPT for 6.99, if it doesn't already exist.

        Returns True if the DLC is installed, False otherwise.
        """

        dlc_url = "http://update.renpy.org/6.99.12.4/updates.json"

        return renpy.invoke_in_new_context(updater.update, dlc_url, add=[name], public_key=PUBLIC_KEY, simulate=UPDATE_SIMULATE, restart=restart)

# This should NEVER Happen
screen update_channel:

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Select Update Channel")

            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    has vbox

                    text _("Updating this launcher is currently unavailable.") style "l_small_text"

                    # Release
                    add SPACER

                    textbutton _("Return") action Jump('front_page')

label update_preference:
    call screen update_channel
    return

screen updater:

    frame:
        style "l_root"

        frame:
            style_group "l_info"

            has vbox

            if u.state == u.ERROR:
                text _("An error has occured:")
            elif u.state == u.CHECKING:
                text _("Checking for updates.")
            elif u.state == u.UPDATE_NOT_AVAILABLE:
                text _("Ren'Py is up to date.")
            elif u.state == u.UPDATE_AVAILABLE:
                text _("[u.version] is now available. Do you want to install it?")
            elif u.state == u.PREPARING:
                text _("Preparing to download the update.")
            elif u.state == u.DOWNLOADING:
                text _("Downloading the update.")
            elif u.state == u.UNPACKING:
                text _("Unpacking the update.")
            elif u.state == u.FINISHING:
                text _("Finishing up.")
            elif u.state == u.DONE:
                text _("The update has been installed. Ren'Py will restart.")
            elif u.state == u.DONE_NO_RESTART:
                text _("The update has been installed.")
            elif u.state == u.CANCELLED:
                text _("The update was cancelled.")

            if u.message is not None:
                add SPACER
                text "[u.message!q]"

            if u.progress is not None:
                add SPACER

                frame:
                    style "l_progress_frame"

                    bar:
                        range 1.0
                        value u.progress
                        style "l_progress_bar"

        label _("Ren'Py Update") style "l_info_label"

    if u.can_cancel:
        textbutton _("Cancel") action u.cancel style "l_left_button"

    if u.can_proceed:
        textbutton _("Proceed") action u.proceed style "l_right_button"

label update:

    python:
        updater.update(UPDATE_URLS[persistent.update_channel], simulate=UPDATE_SIMULATE, public_key=PUBLIC_KEY)

    # This should never happen.
    jump front_page

