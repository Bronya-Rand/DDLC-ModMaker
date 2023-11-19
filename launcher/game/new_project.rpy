# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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
    import shutil
    import os
    import time
    import re
    from extractor import Extractor
    extract = Extractor()

    def check_language_support():

        language = _preferences.language


        new = False
        legacy = False


        # Check for a translation of the words "New GUI Interface".
        if (language is None) or (__("New GUI Interface") != "New GUI Interface"):
            new = True

        try:
            if (language is None) or os.path.exists(os.path.join(config.renpy_base, "templates", language)):
                legacy = True
        except Exception:
            pass

        if new and legacy:
            store.language_support = _("Both interfaces have been translated to your language.")
        elif new:
            store.language_support = _("Only the new GUI has been translated to your language.")
        elif legacy:
            store.language_support = _("Only the legacy theme interface has been translated to your language.")
        else:
            store.language_support = _("Neither interface has been translated to your language.")


label new_project:

    if persistent.projects_directory is None:
        call choose_projects_directory

    if persistent.projects_directory is None:
        $ interface.error(_("The projects directory could not be set. Giving up."))

    if renpy.macintosh:

        if persistent.safari is None:
            call auto_extract

        if persistent.safari is None:
            $ interface.error(_("Couldn't check if OS auto-extracts ZIPs. Please reconfigure your settings."))

    if persistent.zip_directory is None:
        call ddlc_location

    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC ZIP directory could not be set. Giving up."))

    python:
        try:
            mmupdater.mod_template
        except AttributeError:
            interface.error(_("The DDLC Mod Template 2.0 package is missing on this copy of DDMM. Reinstall it using the Tool Installer and try again."))
    
    python:
        while True:
            project_name = ""
            project_name = interface.input(
            _("Project Name"),
            _("Please enter the name of your project:"),
                allow=interface.PROJECT_LETTERS,
                cancel=Jump("front_page"),
                default=project_name,
            )

            project_name = project_name.strip()

            if not project_name:
                interface.error(_("The project name may not be empty."), label=None)
                continue
            if project_name == "launcher":
                interface.error(_("'launcher' is a reserved project name. Please choose a different project name."), label=None)
                continue

            project_dir = os.path.join(persistent.projects_directory, project_name)

            if project.manager.get(project_name) is not None:
                interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name, label=None)
                continue
            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue

            os.makedirs(project_dir)

            interface.processing(_("Installing Template Files..."))
            with interface.error_handling(_("Extracting the DDLC Mod Template")):
                mmupdater.mod_template.ModTool().install(project_dir)

            interface.processing(_("Installing DDLC..."))
            if persistent.safari == True and renpy.macintosh:
                with interface.error_handling(_("Copying DDLC")):
                    extract.game_installation(persistent.zip_directory, project_dir, True)
            else:
                with interface.error_handling(_("Extracting DDLC")):
                    extract.game_installation(persistent.zip_directory, project_dir)

            with open(project_dir + '/game/renpy-version.txt', 'w') as f:
                f.write("7")

            interface.info(_("A file named `renpy-version.txt` has been created in your projects' game directory."), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))

            interface.info(_("DDMM has successfuly created your project with no errors."), _("To install tools like Mood Pose Tool or DDLC OST-Player, see `Install a Tool` under your projects' mod options."))
                
            project.manager.scan()
            break

    return
