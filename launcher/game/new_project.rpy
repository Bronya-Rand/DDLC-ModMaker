# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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
    import os
    import glob
    from extractor import Extractor

    extract = Extractor()

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
    if not glob.glob(config.basedir + "/templates/DDLCModTemplate-*.*.*.zip"):
        $ interface.error(_("The DDLC Mod Template ZIP file is missing in the templates folder. Add the template to the templates folder or reinstall DDMM."))
    
    $ template = glob.glob(config.basedir + "/templates/DDLCModTemplate-*.*.*.zip")[-1]

    python:
        project_name = ""
        while True:
            project_name = interface.input(
                _("Project Name"),
                _("Please enter the name of your project:"),
                filename=True,
                cancel=Jump("front_page"),
            )

            project_name = project_name.strip()

            if not project_name:
                interface.error(_("The project name may not be empty."), label=None)
                continue
            if project_name == "launcher":
                interface.error(_("'launcher' is a reserved project name. Please chose an different project name."), label=None)
                continue

            project_dir = os.path.join(persistent.projects_directory, project_name)

            if project.manager.get(project_name) is not None:
                interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name, label=None)
                continue
            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue
            
            interface.processing(_("Installing DDLC..."))
            if persistent.safari == True and renpy.macintosh:
                with interface.error_handling(_("Copying DDLC...")):
                    extract.game_installation(persistent.zip_directory, project_dir, True)
            else:
                with interface.error_handling(_("Extracting DDLC...")):
                    extract.game_installation(persistent.zip_directory, project_dir)
            
            interface.processing(_("Installing Template Files..."))
            with interface.error_handling(_("Extracting the DDLC Mod Template...")):
                extract.installation(template, project_dir)
            
            with open(project_dir + '/game/renpy-version.txt', 'w') as f:
                f.write("6")

            interface.info(_("A file named `renpy-version.txt` has been created in your projects' game directory."), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))

            interface.info(_("DDMM has successfuly created your project with no errors."), _("To install tools like DDLC OST-Player, see `Install a Tool` under your projects' mod options."))
            
            project.manager.scan()
            break
    return
