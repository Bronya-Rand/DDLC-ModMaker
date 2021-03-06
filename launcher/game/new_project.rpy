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
    import zipfile, shutil, os, glob, time, re, hashlib

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
        except:
            pass

        if new and legacy:
            store.language_support = _("Both interfaces have been translated to your language.")
        elif new:
            store.language_support = _("Only the new GUI has been translated to your language.")
        elif legacy:
            store.language_support = _("Only the legacy theme interface has been translated to your language.")
        else:
            store.language_support = _("Neither interface has been translated to your language.")

    def zip_extract():
        if renpy.macintosh:
            zip = "/ddlc-mac.zip"
            sha = 'de8a0ec7bb918615ccda284f9cfb31962bce62f49ff8425e5761d4252e8ae01e'
        else:
            zip = "/ddlc-win.zip"
            sha = 'cfbaa77ad2db0d94b2e6c3646369aea8750a020eaeb3568a26a551f85f534f8b'
        if not glob.glob(persistent.zip_directory + zip):
            interface.error(_("DDLC ZIP file cannot be found in the ZIP Directory."), _("Check if the ZIP file exists or is pointed to the right directory."))
        
        if renpy.macintosh:
            if hashlib.sha256(persistent.zip_directory + zip).hexdigest() != sha:
                interface.error(_("The DDLC ZIP file downloaded is not official. Download a official DDLC ZIP file from 'https://ddlc.moe' and try again."))
        else:
            if hashlib.sha256(persistent.zip_directory + zip).hexdigest() != sha:
                interface.error(_("The DDLC ZIP file downloaded is not official. Download a official DDLC ZIP file from 'https://ddlc.moe' and try again."))
        
        with zipfile.ZipFile(persistent.zip_directory + zip, "r") as z:
            z.extractall(persistent.projects_directory + "/temp")
            if renpy.macintosh:
                ddlc = persistent.projects_directory + '/temp/DDLC.app/Contents/Resources/autorun/game'
            else:
                ddlc = persistent.projects_directory + '/temp/DDLC-1.1.1-pc/game'
        shutil.move(ddlc, project_dir + '/game')
        shutil.rmtree(persistent.projects_directory + '/temp')
    def ddlc_copy():
        if not glob.glob(persistent.zip_directory + "/ddlc-mac/DDLC.app"):
            interface.error(_("Cannot find DDLC.app."), _("Please make sure your OS and ZIP Directory are set correctly."))
        
        sha = '40dc11e88c590a2aab1560e470d8fc4c9d24eefd45cc64f7e610f8b30d9a25a3'
        if hashlib.sha256(persistent.zip_directory + "/ddlc-mac/DDLC.app").hexdigest() != sha:
            interface.error(_("The DDLC.app file downloaded is not official. Download a official DDLC ZIP file from 'https://ddlc.moe' and try again."))

        shutil.copytree(persistent.zip_directory + "/ddlc-mac/DDLC.app/Contents/Resources/autorun/game", persistent.pd + '/game')
    def template_extract():
        # No SHA Check so anyone can dump a updated template here.
        try:
            with zipfile.ZipFile(config.basedir + "/templates/DDLCModTemplate-2.4.4.zip", "r") as z:
                z.extractall(persistent.pd)
        except:
            shutil.rmtree(persistent.pd)
            interface.error(_("Template ZIP file missing, or corrupt."), _("Check if the ZIP exists or re-download the tool."))
    
    def mpt_extract():
        if glob.glob(persistent.zip_directory + '/DDLC_MPT-*-unpacked.*'):
            mptzip = glob.glob(persistent.zip_directory + '/DDLC_MPT-*')
            mptver = 1
        elif glob.glob(persistent.zip_directory + '/DDLC_MPT-*_unpacked.*'):
            mptzip = glob.glob(persistent.zip_directory + '/DDLC_MPT-[0-9].*_unpacked.*')
            mptver = 2
        else:
            mptzip = glob.glob(persistent.zip_directory + '/MPT v*')
            mptver = 3

        with zipfile.ZipFile(mptzip[0], "r") as z:
            z.extractall(persistent.projects_directory + "/temp")
            if glob.glob(persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/MPT'):
                ddlc = persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/MPT'
            elif glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/MPT'):
                ddlc = glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/MPT')
            else:
                ddlc = glob.glob(persistent.projects_directory + '/temp/game/mod_assets/MPT')

        if mptver >= 2:
            files = os.listdir(ddlc[0])
        else:
            files = os.listdir(ddlc)
        os.mkdir(persistent.pd + '/game/mod_assets/MPT')
        for f in files:
            if mptver >= 2:
                shutil.move(ddlc[0]+'/'+f, persistent.pd + '/game/mod_assets/MPT')
            else:
                shutil.move(ddlc+'/'+f, persistent.pd + '/game/mod_assets/MPT')
        if mptver == 2:
            ddlc = glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/NOT DEFINED WARNING.png')
            shutil.move(ddlc[0], persistent.pd + '/game/mod_assets')
        else:
            if mptver == 3:
                pass
            else:
                shutil.move(persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/NOT DEFINED WARNING.png', persistent.pd + '/game/mod_assets')

    def mpt_copy():
        if glob.glob(persistent.zip_directory + '/DDLC_Mood_Posing_Tool/game/mod_assets/MPT'):
            ddlc = persistent.zip_directory + '/DDLC_Mood_Posing_Tool'
            mptver = 1
        elif glob.glob(persistent.zip_directory + '/DDLC_MPT_v*'):
            ddlc = glob.glob(persistent.zip_directory + '/DDLC_MPT_v*')
            mptver = 2
        else:
            ddlc = glob.glob(persistent.zip_directory + '/MPT v*')
            mptver = 3
        
        if mptver == 3:
            files = os.listdir(ddlc[0])
            shutil.copytree(ddlc[0], persistent.projects_directory + '/temp/MPT v*')
            ddlc = glob.glob(persistent.projects_directory + '/temp/MPT v*/game/mod_assets/MPT')
            files = os.listdir(ddlc[0])
        if mptver == 2:
            files = os.listdir(ddlc[0])
            shutil.copytree(ddlc[0], persistent.projects_directory + '/temp/DDLC_MPT_v*')
            ddlc = glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/MPT')
            files = os.listdir(ddlc[0])
        else:
            files = os.listdir(ddlc)
            shutil.copytree(ddlc, persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool')
            ddlc = persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/MPT'
            files = os.listdir(ddlc)
        os.mkdir(persistent.pd + '/game/mod_assets/MPT')
        for f in files:
            if mptver >= 2:
                shutil.move(ddlc[0]+'/'+f, persistent.pd + '/game/mod_assets/MPT')
            else:
                shutil.move(ddlc+'/'+f, persistent.pd + '/game/mod_assets/MPT')
        if mptver == 2:
            ddlc = glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/NOT DEFINED WARNING.png')
            shutil.move(ddlc[0], persistent.pd + '/game/mod_assets')
        else:
            if mptver == 3:
                pass
            else:
                shutil.move(persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/NOT DEFINED WARNING.png', persistent.pd + '/game/mod_assets')

label new_project_choice:

    python:

        project_choice = interface.choice(
            _("What kind of mod project do you want to make?"),
            [ ( 'new_project', _("Standard Mod Project") ), ( 'mpt', _("Standard Mod Project with MPT")) ],
            "safari_download",
            cancel=Jump("front_page"),
            )

        renpy.jump(project_choice)

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
            persistent.pd = project_dir

            if project.manager.get(project_name) is not None:
                interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name, label=None)
                continue
            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue
            if persistent.safari == True and renpy.macintosh:
                interface.interaction(_("Making a DDLC Folder"), _("Copying DDLC. Please wait..."))
                ddlc_copy()
            else:
                interface.interaction(_("Making a DDLC Folder"), _("Extracting DDLC. Please wait..."))
                zip_extract()
            interface.interaction(_("Copying Template Files"), _("Extracting DDLC Mod Template. Please wait..."))
            template_extract()
            f = open(project_dir + '/renpy-version.txt','w+')
            f.write("7")
            interface.info(_('A file named `renpy-version.txt` has been created in the base directory.'), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))
            try:
                shutil.rmtree(persistent.projects_directory + '/temp')
            except:
                pass
            project.manager.scan()
            break
    return

label mpt:
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
        import glob
        if renpy.macintosh:
            interface.info(_("Installing MPT requires you to download the {i}unpacked{/i} ZIP from the original source."), _("Download MPT's ZIP and place it in the directory where {i}ddlc-mac.zip{/i} is located."),)
        else:
            interface.info(_("Installing MPT requires you to download the {i}unpacked{/i} ZIP from the original source."), _("Download MPT's ZIP and place it in the directory where {i}ddlc-win.zip{/i} is located."),)
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
                continue
            if project_name == "launcher":
                interface.error(_("'launcher' is a reserved project name. Please choose a different project name."), label=None)
                continue
            project_dir = os.path.join(persistent.projects_directory, project_name)
            persistent.pd = project_dir
            if renpy.macintosh and persistent.safari == True:
                pass
            else:
                if not glob.glob(persistent.zip_directory + '/MPT v[0-9].*') and not glob.glob(persistent.zip_directory + '/DDLC_MPT-[0-9].*_unpacked.*') and not glob.glob(persistent.zip_directory + '/DDLC_MPT-[0-9].*-unpacked.*'):
                    interface.error(_("MPT ZIP file cannot be found by glob."), _("Check if the ZIP exists or re-download the tool."))
                    break
            mptzipcount = 0
            if glob.glob(persistent.zip_directory + '/DDLC_MPT-[0-9].*-unpacked.*'):
                mptzipcount += 1
            if glob.glob(persistent.zip_directory + '/DDLC_MPT-[0-9].*_unpacked.*'):
                mptzipcount += 1
            if glob.glob(persistent.zip_directory + '/MPT v[0-9].*'):
                mptzipcount += 1
            if mptzipcount > 1:
                interface.error(_("Multiple MPT ZIP files are located in your ZIP Directory"), _("Please remove the older ZIP version of MPT and try again."))
                break
            if project.manager.get(project_name) is not None:
                interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name, label=None)
                continue
            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue
            if persistent.safari == True and renpy.macintosh:
                interface.interaction(_("Making a DDLC Folder"), _("Copying DDLC. Please wait..."))
                ddlc_copy()
            else:
                interface.interaction(_("Making a DDLC Folder"), _("Extracting DDLC. Please wait..."))
                zip_extract()
            import shutil
            interface.interaction(_("Installing Mod Template"), _("Please wait..."))
            template_extract()
            interface.interaction(_("Installing MPT"), _("Please wait..."))
            if renpy.macintosh and persistent.safari == True:
                mpt_copy()
            else:
                mpt_extract()
            f = open(project_dir + '/renpy-version.txt','w+')
            f.write("7")
            interface.info(_('A file named `renpy-version.txt` has been created in the base directory.'), _("Do not delete this file as it is needed to determine which version of Ren'Py it uses for building your mod."))
            try:
                shutil.rmtree(persistent.projects_directory + '/temp')
            except:
                pass
            project.manager.scan()
            break
