﻿# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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
    import zipfile
    import shutil
    import os
    def zip_extract():
        try:
            if renpy.macintosh:
                zip = "/ddlc-mac.zip"
            else:
                zip = "/ddlc-win.zip"
            with zipfile.ZipFile(persistent.zip_directory + zip, "r") as z:
                z.extractall(persistent.projects_directory + "/temp")
                if renpy.macintosh:
                    ddlc = persistent.projects_directory + '/temp'
                else:
                    ddlc = persistent.projects_directory + '/temp/DDLC-1.1.1-pc'
            shutil.move(ddlc, persistent.project_dir)
        except:
            if renpy.macintosh:
                interface.error(_("Cannot Locate 'ddlc-mac.zip' in [persistent.zip_directory!q]."), _("Make sure you have DDLC downloaded from 'https://ddlc.moe' and check if it exists."),) 
            else:
                interface.error(_("Cannot Locate 'ddlc-win.zip' in [persistent.zip_directory!q]."), _("Make sure you have DDLC downloaded from 'https://ddlc.moe' and check if it exists."),)
        os.remove(persistent.project_dir + '/game/scripts.rpa')
    def ddlc_copy():
        try:
            shutil.copytree(persistent.zip_directory + "/ddlc-mac", persistent.project_dir)
        except:
            interface.error(_("Cannot find DDLC.app."). _("Please make sure your OS and ZIP Directory are set correctly."),)
        os.remove(persistent.project_dir + '/DDLC.app/Contents/Resources/autorun/game/scripts.rpa')
    def template_extract():
        try:
            with zipfile.ZipFile(config.basedir + "/templates/DDLCModTemplate-2.2.4-Standard.zip", "r") as z:
                z.extractall(persistent.project_dir)
        except:
            shutil.rmtree(persistent.project_dir)
            interface.error(_("Template ZIP file missing, or corrupt."), _("Check if the ZIP exists or re-download the tool."))

label new_project:
    if persistent.projects_directory is None:
        call choose_projects_directory
    if persistent.projects_directory is None:
        $ interface.error(_("The projects directory could not be set. Giving up."))
    if persistent.zip_directory is None:
        call ddlc_zip
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC ZIP directory could not be set. Giving up."))
    python:
        project_name = ""
        while True:
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

            persistent.project_dir = os.path.join(persistent.projects_directory, project_name)

            if project.manager.get(project_name) is not None:
                interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name, label=None)
            if os.path.exists(persistent.project_dir):
                interface.error(_("[persistent.project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
            if persistent.safari == True and renpy.macintosh:
                interface.interaction(_("Making a DDLC Folder"), _("Copying DDLC. Please wait..."),)
                ddlc_copy()
            else:
                interface.interaction(_("Making a DDLC Folder"), _("Extracting DDLC. Please wait..."),)
                zip_extract()
            interface.interaction(_("Copying Template Files"), _("Extracting DDLC Mod Template. Please wait..."),)
            template_extract()
            persistent.project_dir = None
            break
    return