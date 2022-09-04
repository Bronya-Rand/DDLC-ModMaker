# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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

    if not glob.glob(config.basedir + "/templates/DDLCModTemplate-*-Py3.zip"):
        $ interface.error(_("The DDLC Mod Template ZIP file is missing in the templates folder. Check for updates, add the template to the templates folder, or reinstall DDMM."))

    $ template = glob.glob(config.basedir + "/templates/DDLCModTemplate-*-Py3.zip")[-1]
    
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

            interface.processing(_("Installing Template Files..."))
            with interface.error_handling(_("Extracting the DDLC Mod Template...")):
                extract.installation(template, project_dir)

            interface.processing(_("Installing DDLC..."))
            if persistent.safari == True and renpy.macintosh:
                with interface.error_handling(_("Copying DDLC...")):
                    extract.game_installation(persistent.zip_directory, project_dir, True)
            else:
                with interface.error_handling(_("Extracting DDLC...")):
                    extract.game_installation(persistent.zip_directory, project_dir)

            with open(project_dir + '/game/renpy-version.txt', 'w') as f:
                f.write("8")

            interface.info(_("A file named `renpy-version.txt` has been created in your projects' game directory."), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))

            interface.info(_("DDMM has successfuly created your project with no errors."), _("To install tools like Mood Pose Tool or DDLC OST-Player, see `Install a Tool` under your projects' mod options."))
                
            project.manager.scan()
            break

    return

screen select_template:

    default result = project.manager.get("english")

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Choose Project Template")

            hbox:

                frame:
                    style "l_indent"
                    xmaximum ONETHIRD

                    viewport:
                        scrollbars "vertical"
                        vbox:
                            for p in project.manager.templates:
                                textbutton "[p.name!q]" action SetScreenVariable("result", p) style "l_list"

                frame:
                    style "l_indent"
                    xmaximum TWOTHIRDS

                    text _("Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'.")


    textbutton _("Return") action Jump("front_page") style "l_left_button"
    textbutton _("Continue") action Return(result) style "l_right_button"


label new_theme_project:

    python hide:
        if len(project.manager.templates) == 1:
            template = project.manager.templates[0]
        else:
            template = renpy.call_screen("select_template")

        template_path = template.path

        with interface.error_handling(_("creating a new project")):
            shutil.copytree(template_path, project_dir, symlinks=False)

            # Delete the tmp directory, if it exists.
            if os.path.isdir(os.path.join(project_dir, "tmp")):
                shutil.rmtree(os.path.join(project_dir, "tmp"))

            # Delete project.json, which must exist.
            os.unlink(os.path.join(project_dir, "project.json"))

            # Change the save directory in options.rpy
            fn = os.path.join(project_dir, "game/options.rpy")
            with open(fn, "rb") as f:
                options = f.read().decode("utf-8")

            options = options.replace("PROJECT_NAME", project_name)
            options = options.replace("UNIQUE", str(int(time.time())))

            with open(fn, "wb") as f:
                f.write(options.encode("utf-8"))

            font = template.data.get("font", None)
            if font is not None:
                src = os.path.join(config.gamedir, "fonts", font)
                dst = os.path.join(project_dir, "game", "tl", "None", font)
                shutil.copy(src, dst)

        # Activate the project.
        with interface.error_handling(_("activating the new project")):
            project.manager.scan()
            project.Select(project.manager.get(project_name))()

    call choose_theme_callable

    jump front_page
