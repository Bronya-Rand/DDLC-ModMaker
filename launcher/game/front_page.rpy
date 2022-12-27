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

define PROJECT_ADJUSTMENT = ui.adjustment()

init python:

    import datetime
    import shutil

    # Used for testing.
    def Relaunch():
        renpy.quit(relaunch=True)

    def readVersion():
        if persistent.projects_directory is not None:
            # move renpy-version.txt to project game folder for easy transfer
            new_txt_path = os.path.join(persistent.projects_directory, project.current.name, 'game/renpy-version.txt').replace("\\", "/")
            try: 
                old_txt_path = os.path.join(persistent.projects_directory, project.current.name, 'renpy-version.txt').replace("\\", "/")
                renpy.file(old_txt_path)
                shutil.move(old_txt_path, new_txt_path)
            except IOError: pass

            try:
                with open(new_txt_path) as f:
                    file_ver = f.readline().strip()

                int_ver = int(file_ver)
                if int_ver >= 6 and int_ver <= 8:
                    return int_ver
                else:
                    return -1
            except IOError: 
                return None
            except ValueError:
                return -1
        else: return None

    # Adds backwards compat between 4.1.0+ and older templates
    def NewEditorOpen(path):
        base = persistent.projects_directory if persistent.projects_directory is not None else config.basedir
        if os.path.exists(os.path.join(base, project.current.name, path)):
            return editor.Edit(path, check=True)
        else:
            old_path = path.split("/")
            old_path.pop(1)
            return editor.Edit(str(os.path.join(*old_path)).replace("\\", "/"), check=True)

screen front_page:
    frame:
        alt ""

        style_group "l"
        style "l_root"

        has hbox

        # Projects list section - on left.

        frame:
            style "l_projects"
            xmaximum 300
            right_margin 2

            top_padding 20
            bottom_padding 26

            side "t c b":

                window style "l_label":

                    has hbox:
                        xfill True

                    text _("Mod Projects:") style "l_label_text" size 36 yoffset 10

                    textbutton _("refresh"):
                        xalign 1.0
                        yalign 1.0
                        yoffset 5
                        style "l_small_button"
                        action project.Rescan()
                        right_margin HALF_INDENT

                side "c r":

                    viewport:
                        yadjustment PROJECT_ADJUSTMENT
                        mousewheel True
                        use front_page_project_list

                    vbar:
                        style "l_vscrollbar"
                        adjustment PROJECT_ADJUSTMENT

                vbox:
                    add HALF_SPACER
                    add SEPARATOR
                    add HALF_SPACER

                    hbox:
                        xfill True

                        textbutton _("+ Create New Project"):
                            left_margin (HALF_INDENT)
                            action Jump("new_project")

        # Project section - on right.

        if project.current is not None:
            use front_page_project

    if project.current is not None:
        python:
            launch = readVersion()
                
        if launch == 6:
            textbutton _("DDMM 6 Needed") action NullAction() style "l_unavail_button"
        elif launch == 8:
            textbutton _("DDMM 8 Needed") action NullAction() style "l_unavail_button"
        elif launch == 7 or project.current.name == "launcher":
            textbutton _("Launch Mod") action project.Launch() style "l_right_button"
            key "K_F5" action project.Launch()
        elif launch == -1:
            textbutton _("Cannot Determine Version") action Jump('version_incorrect_content') style "l_unavail_button"
        else:
            textbutton _("Cannot Determine Version") action Jump('missing_version') style "l_unavail_button"



# This is used by front_page to display the list of known projects on the screen.
screen front_page_project_list:

    $ projects = project.manager.projects
    $ templates = project.manager.templates

    vbox:

        if templates and persistent.show_templates:

            for p in templates:

                textbutton _("[p.name!q] (template)"):
                    action project.Select(p)
                    alt _("Select project [text].")
                    style "l_list"

            null height 12

        if projects:

            for p in projects:

                textbutton "[p.name!q]":
                    action project.Select(p)
                    alt _("Select project [text].")
                    style "l_list"

            null height 12


# This is used for the right side of the screen, which is where the project-specific
# buttons are.
screen front_page_project:

    $ p = project.current

    window:

        has vbox

        frame style "l_label":
            has hbox xfill True
            text "[p.display_name!q]" style "l_label_text"
            label _("Active Project") style "l_alternate"

        grid 2 1:
            xfill True
            spacing HALF_INDENT

            vbox:

                label _("Open Directory") style "l_label_small"

                frame style "l_indent":
                    has vbox

                    textbutton _("game") action OpenDirectory(os.path.join(p.path, "game"), absolute=True)
                    textbutton _("base") action OpenDirectory(os.path.join(p.path, "."), absolute=True)
                    textbutton _("mod_assets") action OpenDirectory(os.path.join(p.path, "game/mod_assets"), absolute=True)
                    textbutton _("mod_extras") action OpenDirectory(os.path.join(p.path, "game/mod_extras"), absolute=True)
                    #textbutton _("gui") action OpenDirectory(os.path.join(p.path, "game/gui"), absolute=True)

            vbox:
                if persistent.show_edit_funcs:

                    label _("Edit File") style "l_label_small"

                    frame style "l_indent":
                        has vbox

                        textbutton "script.rpy" action editor.Edit("game/script.rpy", check=True)
                        textbutton "options.rpy" action editor.Edit("game/options.rpy", check=True)
                        textbutton "definitions.rpy" action NewEditorOpen("game/definitions/definitions.rpy")
                        textbutton "gui.rpy" action editor.Edit("game/gui.rpy", check=True)
                        textbutton "screens.rpy" action editor.Edit("game/screens.rpy", check=True)

                        if editor.CanEditProject():
                            textbutton _("Open project") action editor.EditProject()
                        else:
                            textbutton _("All script files") action editor.EditAll()

        add SPACER

        label _("Actions") style "l_label_small"

        grid 2 1:
            xfill True
            spacing HALF_INDENT

            frame style "l_indent":
                has vbox

                textbutton _("Navigate Script") action Jump("navigation")
                textbutton _("Check Script for Errors") action Jump("lint")
                textbutton _("Delete Persistent") action Jump("rmpersistent")
                textbutton _("Force Recompile") action Jump("force_recompile")
                if project.current.name != "launcher":
                    textbutton _("Change Version") action Jump("set_version")

                # textbutton "Relaunch" action Relaunch

            frame style "l_indent":
                has vbox

                textbutton _("Install a Tool") action Jump("tool_install")
                if ability.can_distribute:
                    textbutton _("Build Mod") action Jump("build_distributions")

                if project.current.name != "launcher":

                    python:
                        launch = readVersion()
                            
                    if launch == 7:
                        textbutton _("Build Mod for Android") action Jump("android")
                    else:
                        textbutton _("Android Unavailable") action Jump("no_android")

                textbutton _("Generate Translations") action Jump("translate")
                textbutton _("Extract Dialogue") action Jump("extract_dialogue")
                textbutton _("Delete Project") action Jump("delete_folder")

label main_menu:
    return

label start:
    show screen bottom_info
    $ dmgcheck()

    jump expression renpy.session.pop("launcher_start_label", "front_page")

default persistent.has_chosen_language = False

default persistent.has_update = False
define update_notified = False

label front_page:

    if persistent.zip_directory is not None:
        if persistent.zip_directory.endswith("ddlc-mac") or persistent.zip_directory.endswith("ddlc-mac.zip"):
            $ persistent.zip_directory = None

    if (not persistent.has_chosen_language) or ("RENPY_CHOOSE_LANGUAGE" in os.environ):

        if _preferences.language is None:
            hide screen bottom_info
            call choose_language
            show screen bottom_info

        $ persistent.has_chosen_language = True

    if persistent.daily_update_check and ((not persistent.last_update_check) or (datetime.date.today() > persistent.last_update_check)):
        python hide:
            persistent.last_update_check = datetime.date.today()
            persistent.update_available = False
            renpy.invoke_in_thread(fetch_ddmm_updates, update_json=True)
            renpy.invoke_in_thread(fetch_ddmm_updates, mt=True, update_json=True)

    if not update_notified and persistent.update_available:
        $ update_notified = True
        $ renpy.notify("Updates are available.")

    call screen front_page
    jump front_page


label lint:
    python hide:

        interface.processing(_("Checking script for potential problems..."))
        lint_fn = project.current.temp_filename("lint.txt")

        project.current.launch([ 'lint', lint_fn ], wait=True)

        e = renpy.editor.editor
        e.begin(True)
        e.open(lint_fn)
        e.end()

    jump front_page

label rmpersistent:

    python hide:
        interface.processing(_("Deleting persistent data..."))
        project.current.launch([ 'rmpersistent' ], wait=True)

    jump front_page

label force_recompile:

    python hide:
        interface.processing(_("Recompiling all rpy files into rpyc files..."))
        project.current.launch([ 'compile' ], wait=True)

    jump front_page

label missing_version:
    python:
        interface.info(_("This project cannot launch in DDMM as this is either a non-DDLC mod or is missing 'renpy-version.txt'"), _("Please check if 'renpy-version.txt' exists."),)
        renpy.jump('front_page')

label version_incorrect_content:
    python:
        interface.info(_("This project cannot launch in DDMM as 'renpy-version.txt' has unexpected content."), _("Please check if 'renpy-version.txt' contains only a single number with the project's major RenPy version (6, 7, 8)."),)
        renpy.jump('front_page')

label no_android:
    python:
        interface.info(_("This project cannot be built for Android as it's either in Ren'Py 6/8 mode or has a missing/corrupt 'renpy-version.txt'"), _("Please check if 'renpy-version.txt' exists or change the version of your project."),)
        renpy.jump('front_page')

label set_version:
    python:
        x = readVersion()
        if x is None:
            with open(os.path.join(persistent.projects_directory, project.current.name, "game/renpy-version.txt"), "w") as f:
                f.write("7") 
            interface.info(_("A file named `renpy-version.txt` has been created in your projects' game directory."), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))
            renpy.jump("front_page")

        prompt = False    
        if x == 6:
            prompt = True
            response_text = _("This mod is set to Ren'Py 6 Mode. ")
        elif x == 8:
            prompt = True
            response_text = _("This mod is set to Ren'Py 8 Mode. ")
            
        if prompt:
            confirm_delete = False
            delete_response = interface.yesno(
                label=_("Warning"),
                message=response_text + _("If you change this, it may result in a improperly packaged mod.\nAre you sure you want to proceed? Type either Yes or No."),
                yes=SetScreenVariable(confirm_delete, True),
                no=Return(),
                cancel=Jump("front_page"))

            if not confirm_delete:
                renpy.jump("front_page")
            else:
                with open(os.path.join(persistent.projects_directory, project.current.name, "game/renpy-version.txt"), "w") as f:
                    f.write("7") 
                interface.info(_("Set the Ren'Py mode version to Ren'Py 7."))
        else:
            interface.info(_("The Ren'Py mode version is already set to Ren'Py 7."))
    
    jump front_page
