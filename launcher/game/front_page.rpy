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

define PROJECT_ADJUSTMENT = ui.adjustment()

init python:

    import os
    import subprocess
    import shutil

    class OpenDirectory(Action):
        """
        Opens `directory` in a file browser. `directory` is relative to
        the project root.
        """

        alt = _("Open [text] directory.")

        def __init__(self, directory, absolute=False):
            if absolute:
                self.directory = directory
            else:
                self.directory = os.path.join(project.current.path, directory)

        def get_sensitive(self):
            return os.path.exists(self.directory)

        def __call__(self):

            try:
                directory = renpy.fsencode(self.directory)

                if renpy.windows:
                    os.startfile(directory)
                elif renpy.macintosh:
                    subprocess.Popen([ "open", directory ])
                else:
                    subprocess.Popen([ "xdg-open", directory ])

            except:
                pass

    # Used for testing.
    def Relaunch():
        renpy.quit(relaunch=True)

    def readVersion():
        old_txt_path = os.path.join(project.current.path, 'renpy-version.txt').replace("\\", "/")
        new_txt_path = os.path.join(project.current.path, 'game/renpy-version.txt').replace("\\", "/")

        if os.path.exists(old_txt_path):
            shutil.move(old_txt_path, new_txt_path)

        try:
            with open(new_txt_path) as f:
                file_ver = int(f.readline().strip())

            if file_ver >= 6 and file_ver <= 8:
                return file_ver
            else:
                return -1
        except IOError:
            return None
        except ValueError:
            return -1

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
                
        if launch == 7:
            textbutton _("DDMM 7+ Needed") action NullAction() style "l_unavail_button"
        elif launch == 8:
            textbutton _("DDMM 8+ Needed") action NullAction() style "l_unavail_button"
        elif launch == 6 or project.current.name == "launcher":
            textbutton _("Launch Mod") action project.Launch() style "l_right_button"
            key "K_F5" action project.Launch()
        else:
            textbutton _("Cannot Determine Version") action Jump('version_error') style "l_unavail_button"

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
    $ version = renpy.version()

    window:

        has vbox

        frame style "l_label":
            has hbox xfill True
            text "[p.name!q]" style "l_label_text"
            label _("Selected Mod") style "l_alternate"

        grid 2 1:
            xfill True
            spacing HALF_INDENT

            vbox:

                label _("Open Folder") style "l_label_small"

                frame style "l_indent":
                    has vbox

                    textbutton _("game") action OpenDirectory(os.path.join(p.path, "game"))
                    textbutton _("base") action OpenDirectory(os.path.join(p.path, "."))
                    textbutton _("mod_assets") action OpenDirectory(os.path.join(p.path, "game/mod_assets"))
                    textbutton _("mod_extras") action OpenDirectory(os.path.join(p.path, "game/mod_extras"))
                    #textbutton _("gui") action OpenDirectory(os.path.join(p.path, "game/gui"))

            vbox:
                if persistent.show_edit_funcs:

                    label _("Edit File") style "l_label_small"

                    frame style "l_indent":
                        has vbox

                        textbutton "script.rpy" action editor.Edit("game/script.rpy", check=True)
                        textbutton "options.rpy" action editor.Edit("game/options.rpy", check=True)
                        textbutton "definitions.rpy" action editor.Edit("game/definitions.rpy", check=True)
                        textbutton "gui.rpy" action editor.Edit("game/gui.rpy", check=True)
                        textbutton "screens.rpy" action editor.Edit("game/screens.rpy", check=True)

                        textbutton _("All script files") action editor.EditAll()

        add SPACER

        label _("Options") style "l_label_small"

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
                        if persistent.projects_directory:
                            launch = readVersion()
                        else:
                            launch = None
                            
                    if launch == 6:
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

define renpy_depreciation_reminder = False

label front_page:
    if persistent.zip_directory is not None:
        if persistent.zip_directory.endswith("ddlc-mac") or persistent.zip_directory.endswith("ddlc-mac.zip"):
            $ persistent.zip_directory = None

    python:
        if not os.path.exists(os.path.join(config.basedir, "templates")):
            os.makedirs(os.path.join(config.basedir, "templates"))

    python hide:
        if not renpy_depreciation_reminder:
            global renpy_depreciation_reminder

            renpy_depreciation_reminder = True
            interface.info(_("DDMM 6 may be depreciated in the near future."), _("It is recommended that you upgrade to DDMM 7 or DDMM 8 for future mod development.\nSee {a=https://www.reddit.com/r/DDLCMods/wiki/notices/#wiki_why_are_some_guides_not_applicable_to_the_4.1.0_release_of_the_mod_template.3F}here{/a} for more information."))
    
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

label version_error:
    python:
        interface.info(_("This project cannot launch in DDMM as this is either a non-DDLC mod or is missing 'renpy-version.txt'"), _("Please check if 'renpy-version.txt' exists."),)
        renpy.jump('front_page')
        
label no_android:
    python:
        interface.info(_("This project cannot be built for Android as either the version of it is set to Ren'Py 6 or the project is missing 'renpy-version.txt'"), _("Please check if 'renpy-version.txt' exists or change the version of your project."),)
        renpy.jump('front_page')

label set_version:
    python:
        x = readVersion()
        if x is None:
            try:
                ver_path = os.path.join(persistent.projects_directory, project.current.name, "game/renpy-version.txt")
                if not os.path.exists(ver_path):
                    ver_path = os.path.join(config.basedir, project.current.name, "game/renpy-version.txt")
            except TypeError:
                ver_path = os.path.join(config.basedir, project.current.name, "game/renpy-version.txt")
            with open(ver_path, "w") as f:
                f.write("6") 
            interface.info(_("A file named `renpy-version.txt` has been created in your projects' game directory."), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))
            renpy.jump("front_page")
            
        prompt = False
        if x > 6:
            prompt = True

        if prompt:
            delete_response = interface.yesno(
                label=_("Warning"),
                message=_("This mod is set to Ren'Py 7/8 Mode. If you change this, it may result in a unloadable mod. Are you sure you want to proceed? Type either Yes or No."),
                yes=SetScreenVariable(confirm_delete, True),
                no=Return(),
                cancel=Jump("front_page"))

            if not confirm_delete:
                renpy.jump("front_page")
            else:
                with open(os.path.join(persistent.projects_directory, project.current.name, "game/renpy-version.txt"), "w") as f:
                    f.write("6") 
                interface.info(_("Set the Ren'Py mode version to Ren'Py 6."))
        else:
            interface.info(_("The Ren'Py mode version is already set to Ren'Py 6."))

    return
