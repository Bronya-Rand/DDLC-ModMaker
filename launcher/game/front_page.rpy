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

define PROJECT_ADJUSTMENT = ui.adjustment()

init python:

    import datetime
    import shutil
    import re

    # Used for testing.
    def Relaunch():
        renpy.quit(relaunch=True)

    def read_version(d):
        mod_ver_file = os.path.join(d, "game/renpy-version.txt")

        try:
            with open(mod_ver_file, "r") as f:
                version_line = f.readline()
        except IOError:
            return None

        match = re.match(r"^\d$", version_line)
        if match:
            return int(match.group(0))
        else:
            return None

    def renpy_version_compatible(d):
        mod_version = read_version(d)

        check_result = {
            "compatible": None,
            "version": None,
            "missing": False,
            "range": False,
            "incorrect": False,
        }

        check_result["version"] = mod_version

        if mod_version is None:
            check_result["compatible"] = False
            check_result["missing"] = True
        elif mod_version < 6 or mod_version > 8:
            check_result["compatible"] = False
            check_result["range"] = True
        elif mod_version != renpy.version_tuple[0]:
            check_result["compatible"] = False
            check_result["incorrect"] = True
        else:
            check_result["compatible"] = True

        return check_result

    # Adds backwards compat between 4.1.0+ and older templates
    def NewEditorOpen(path):
        if os.path.exists(os.path.join(project.current.path, path)):
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
            checks = renpy_version_compatible(project.current.path)

        if project.current.name != "launcher":
            if not checks["compatible"]:
                if checks["missing"]:
                    textbutton _("Missing Version Data") action NullAction() style "l_unavail_button"
                elif checks["range"]:
                    textbutton _("Invalid Ren'Py Version") action NullAction() style "l_unavail_button"
                elif checks["incorrect"]:
                    textbutton _("Incorrect DDMM SDK Version") action NullAction() style "l_unavail_button"
            else:
                textbutton _("Launch Mod") action project.Launch() style "l_right_button"
                key "K_F5" action project.Launch()

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

                python:
                    mod_version = renpy_version_compatible(p.path)
                    mod_text_ver = mod_version["version"]
                    if mod_text_ver is None or mod_version["range"]:
                        mod_text_ver = "Unknown"
                button:
                    action project.Select(p)
                    style "l_list"

                    vbox:
                        text "[p.name!q]" style "l_list_text"
                        text "(Ren'Py [mod_text_ver] Mod)" style "l_list_text" size 12 xpos 5

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

                textbutton _("Tool Installer") action Jump("mmtoolinstaller")
                if ability.can_distribute:
                    textbutton _("Build Mod") action Jump("build_distributions")

                if project.current.name != "launcher":

                    python:
                        checks = renpy_version_compatible(project.current.path)
                            
                    if checks["compatible"]:
                        textbutton _("Build Mod for Android") action Jump("android")
                    else:
                        textbutton _("Android Unavailable") action Jump("no_android")

                textbutton _("Generate Translations") action Jump("translate")
                #textbutton _("Extract Dialogue") action Jump("extract_dialogue")
                textbutton _("Delete Project") action Jump("delete_folder")

label main_menu:
    return

label start:
    show screen bottom_info
    $ dmgcheck()

    jump expression renpy.session.pop("launcher_start_label", "front_page")

default persistent.has_chosen_language = False

default persistent.has_update = False

label front_page:

    if (not persistent.has_chosen_language) or ("RENPY_CHOOSE_LANGUAGE" in os.environ):

        if (_preferences.language is None) or ("RENPY_CHOOSE_LANGUAGE" in os.environ):
            hide screen bottom_info
            call choose_language
            show screen bottom_info

        $ persistent.has_chosen_language = True

    if not os.path.exists(config.basedir + "/update/third_party.json"):
        python:
            f = open(config.basedir + "/update/third_party.json", "w")
            f.write("{}")
            f.close()

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

label set_version:
    python:
        mod_version = renpy_version_compatible(project.current.path)
        if mod_version["missing"]:
            ver_path = os.path.join(project.current.gamedir, "renpy-version.txt")
            with open(ver_path, "w") as f:
                f.write(str(renpy.version_tuple[0])) 
            interface.info(_("A file named `renpy-version.txt` has been created in your projects' game directory."), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))
            renpy.jump("front_page")
            
        if mod_version["incorrect"]:
            edit_response = interface.yesno(
                label=_("Warning"),
                message=_("This mod is set to Ren'Py ") + str(mod_version["version"]) + _(" Mode. If you change this, it may result in a improperly packaged mod.\nAre you sure you want to proceed? Type either Yes or No."),
                no=Jump("front_page"))

            with open(os.path.join(project.current.gamedir, "renpy-version.txt"), "w") as f:
                f.write(str(renpy.version_tuple[0])) 
            interface.info(_("Set the Ren'Py mode version to Ren'Py {}.".format(str(renpy.version_tuple[0]))))
        else:
            interface.info(_("The Ren'Py mode version is already set to Ren'Py {}.".format(str(renpy.version_tuple[0]))))
    
    jump front_page