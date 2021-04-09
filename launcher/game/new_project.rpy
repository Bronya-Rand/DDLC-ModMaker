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
    import zipfile, shutil, os, hashlib

    def zip_extract():
        if renpy.macintosh:
            sha = 'abc3d2fee9433ad454decd15d6cfd75634283c17aa3a6ac321952c601f7700ec'
        else:
            sha = '2a3dd7969a06729a32ace0a6ece5f2327e29bdf460b8b39e6a8b0875e545632e'
        
        if not glob.glob(persistent.zip_directory):
            interface.error(_("DDLC's ZIP file cannot be found in the ZIP Directory."), _("Check if the ZIP file exists or if it is pointed to the right directory."))
        
        path = open(persistent.zip_directory, 'rb')
        if hashlib.sha256(path.read()).hexdigest() != sha:
            interface.error(_("The DDLC ZIP file chosen is not official. Download a official DDLC ZIP file from {a=https://ddlc.moe}DDLC's website{/a}, select it in Settings, and try again."))
        path.close() # JIC

        with zipfile.ZipFile(persistent.zip_directory, "r") as z:
            z.extractall(persistent.projects_directory + "/temp")
            if renpy.macintosh:
                ddlc = persistent.projects_directory + '/temp'
            else:
                ddlc = persistent.projects_directory + '/temp/DDLC-1.1.1-pc'
        
        shutil.move(ddlc, persistent.project_dir)

    def ddlc_copy():
        if not glob.glob(persistent.zip_directory + "/ddlc-mac/DDLC.app"):
            interface.error(_("Cannot find DDLC.app."), _("Please make sure that your OS and ZIP Directory settings are set up correctly."))
        
        # sha = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        # path = open(persistent.zip_directory + "/ddlc-mac/DDLC.app", 'rb')
        # if hashlib.sha256(path.read()).hexdigest() != sha:
        #     interface.error(_("The DDLC.app file downloaded is not official. Download a official DDLC ZIP file from {a=https://ddlc.moe}DDLC's website{/a} and try again."))
        # path.close()

        shutil.copytree(persistent.zip_directory + "/ddlc-mac", persistent.project_dir)

    def template_extract():
        try:
            with zipfile.ZipFile(config.basedir + "/templates/DDLCModTemplate-2.4.4.zip", "r") as z:
                if renpy.macintosh:
                    z.extractall(persistent.project_dir + '/DDLC.app/Contents/Resources/autorun')
                else:
                    z.extractall(persistent.project_dir)
        except:
            shutil.rmtree(persistent.project_dir)
            interface.error(_("The mod emplate ZIP file is either missing or corrupt."), _("Check if the ZIP exists in the 'templates' folder or re-download the tool."))

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
                continue
            if project_name == "launcher":
                interface.error(_("'launcher' is a reserved project name. Please chose an different project name."), label=None)
                continue

            persistent.project_dir = os.path.join(persistent.projects_directory, project_name)

            if project.manager.get(project_name) is not None:
                interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name, label=None)
                continue
            if os.path.exists(persistent.project_dir):
                interface.error(_("[persistent.project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue
            
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
                continue
            if project_name == "launcher":
                interface.error(_("'launcher' is a reserved project name. Please choose an different project name."), label=None)
                continue

            persistent.project_dir = os.path.join(persistent.projects_directory, project_name)
            
            if project.manager.get(project_name) is not None:
                interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name, label=None)
                continue
            if os.path.exists(persistent.project_dir):
                interface.error(_("[persistent.project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue
            
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
    return
