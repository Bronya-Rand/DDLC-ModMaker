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
    import zipfile, shutil, os
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
        except:
            if renpy.macintosh:
                interface.error(_("Cannot locate 'ddlc-mac.zip' in [persistent.zip_directory!q]."), _("Make sure you have DDLC downloaded from 'https://ddlc.moe' and check if it exists.")) 
            else:
                interface.error(_("Cannot locate 'ddlc-win.zip' in [persistent.zip_directory!q]."), _("Make sure you have DDLC downloaded from 'https://ddlc.moe' and check if it exists."))
        try:
            shutil.move(ddlc, persistent.project_dir)
        except:
            shutil.rmtree(persistent.projects_directory + '/temp')
            if renpy.macintosh:
                interface.error(_("The `ddlc-mac.zip` file extracted is zipped improperly or corrupted."), _("Please re-download the ZIP from 'https://ddlc.moe'"))
            else:
                interface.error(_("The `ddlc-win.zip` file extracted is zipped improperly or corrupted."), _("Please re-download the ZIP from 'https://ddlc.moe'"))
        #if renpy.macintosh:
            #os.remove(persistent.project_dir + '/DDLC.app/Contents/Resources/autorun/game/scripts.rpa')
        #else:
            #os.remove(persistent.project_dir + '/game/scripts.rpa')
    def ddlc_copy():
        try:
            shutil.copytree(persistent.zip_directory + "/ddlc-mac", persistent.project_dir)
        except:
            interface.error(_("Cannot find DDLC.app."). _("Please make sure your OS and ZIP Directory are set correctly."))
        #os.remove(persistent.project_dir + '/DDLC.app/Contents/Resources/autorun/game/scripts.rpa')
    def template_extract():
        if renpy.macintosh:
            try:
                with zipfile.ZipFile(config.basedir + "/templates/DDLCModTemplate-2.4.3.zip", "r") as z:
                    z.extractall(persistent.project_dir + '/DDLC.app/Contents/Resources/autorun')
            except:
                shutil.rmtree(persistent.project_dir)
                interface.error(_("Template ZIP file missing, or corrupt."), _("Check if the ZIP exists or re-download the tool."))
        else:
            try:
                with zipfile.ZipFile(config.basedir + "/templates/DDLCModTemplate-2.4.3.zip", "r") as z:
                    z.extractall(persistent.project_dir)
            except:
                shutil.rmtree(persistent.project_dir)
                interface.error(_("Template ZIP file missing, or corrupt."), _("Check if the ZIP exists or re-download the tool."))
    def cc_extract():
        with zipfile.ZipFile(persistent.zip_directory + '/ddcc-master.zip', "r") as z:
            z.extractall(persistent.projects_directory + "/temp")
            ddcc = persistent.projects_directory + '/temp/ddcc-master'
        shutil.rmtree(persistent.project_dir + '/game/python-packages')
        files = os.listdir(ddcc)
        for f in files:
            shutil.move(ddcc+'/'+f, persistent.project_dir + '/game')
    def cc_copy():
        ddcc = persistent.zip_directory + '/ddcc-master'
        shutil.copytree(ddcc, persistent.project_dir + '/temp/ddcc-master')
        shutil.rmtree(persistent.project_dir + '/DDLC.app/Contents/Resources/autorun/game/python-packages')
        files = os.listdir(ddcc)
        for f in files:
            shutil.move(ddcc+'/'+f, persistent.project_dir + '/DDLC.app/Contents/Resources/autorun/game')

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
        call ddlc_zip
    if persistent.zip_directory is None:
        $ interface.error(_("The DDLC ZIP directory could not be set. Giving up."))
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
            if project_name == "launcher":
                interface.error(_("'launcher' is a reserved project name. Please chose an different project name."))
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
            f = open(persistent.project_dir + '/renpy-version.txt','w+')
            f.write("6")
            persistent.project_dir = None
            interface.info(_('A file named `renpy-version.txt` has been created in the base directory.'), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))
            project.manager.scan()
            break
    return

label ddcc:

    python:
        interface.info(_("Making a Comedy Club Skit requires you to download the Comedy Club ZIP from https://github.com/logokas/ddcc."), _("Select Clone and Download and Download ZIP to your DDLC ZIP Directory."),)

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
            if project_name == "launcher":
                interface.error(_("'launcher' is a reserved project name. Please choose an different project name."))
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
            interface.interaction(_("Copying Template Files"), _("Copying DDCC Skit Template. Please wait..."),)
            if renpy.macintosh and persistent.safari == True:
                cc_copy()
            else:
                cc_extract()
            f = open(persistent.project_dir + '/renpy-version.txt','w+')
            f.write("6")
            interface.info(_("Please read ddcc_submission_guidelines.txt in the game folder on the DDCC Submission Guidelines you should follow."),)
            interface.info(_('A file named `renpy-version.txt` has been created in the base directory.'), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))
            project.manager.scan()
            break
    jump front_page
