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
            sha = 'abc3d2fee9433ad454decd15d6cfd75634283c17aa3a6ac321952c601f7700ec'
        else:
            sha = '2a3dd7969a06729a32ace0a6ece5f2327e29bdf460b8b39e6a8b0875e545632e'
        
        path = open(persistent.zip_directory, 'rb')
        if hashlib.sha256(path.read()).hexdigest() != sha:
            interface.error(_("The DDLC ZIP file chosen is not official. Download a official DDLC ZIP file from {a=https://ddlc.moe}DDLC's website{/a}, select it in Settings, and try again."))
        path.close() # JIC
        
        with zipfile.ZipFile(persistent.zip_directory, "r") as z:
            z.extractall(persistent.projects_directory + "/temp")
            if renpy.macintosh:
                ddlc = persistent.projects_directory + '/temp/DDLC.app/Contents/Resources/autorun/game'
            else:
                ddlc = persistent.projects_directory + '/temp/DDLC-1.1.1-pc/game'

        shutil.move(ddlc, project_dir + '/game')
        shutil.rmtree(persistent.projects_directory + '/temp')

    def ddlc_copy():
        if not glob.glob(persistent.zip_directory + "/ddlc-mac/DDLC.app"):
            interface.error(_("Cannot find DDLC.app."), _("Please make sure that your OS and ZIP Directory settings are set correctly."))
        
        shutil.copytree(persistent.zip_directory + "/ddlc-mac/DDLC.app/Contents/Resources/autorun/game", project_dir + '/game')

    def template_extract():
        try:
            with zipfile.ZipFile(config.basedir + "/templates/DDLCModTemplate-2.4.7.zip", "r") as z:
                z.extractall(project_dir)
        except:
            shutil.rmtree(project_dir)
            interface.error(_("The mod emplate ZIP file is either missing or corrupt."), _("Check if the ZIP exists in the 'templates' folder or re-download the tool."))
    
    def mpt_extract():
        if glob.glob(config.basedir + '/templates/DDLC_MPT-*-unpacked.*'):
            mptzip = glob.glob(config.basedir + '/templates/DDLC_MPT-*')
            mptver = 1
        elif glob.glob(config.basedir + '/templates/DDLC_MPT-*_unpacked.*'):
            mptzip = glob.glob(config.basedir + '/templates/DDLC_MPT-[0-9].*_unpacked.*')
            mptver = 2
        else:
            mptzip = glob.glob(config.basedir + '/templates/MPT v*')
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
        os.mkdir(project_dir + '/game/mod_assets/MPT')
        for f in files:
            if mptver >= 2:
                shutil.move(ddlc[0]+'/'+f, project_dir + '/game/mod_assets/MPT')
            else:
                shutil.move(ddlc+'/'+f, project_dir + '/game/mod_assets/MPT')
        if mptver == 2:
            ddlc = glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/NOT DEFINED WARNING.png')
            shutil.move(ddlc[0], project_dir + '/game/mod_assets')
        else:
            if mptver == 3:
                pass
            else:
                shutil.move(persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/NOT DEFINED WARNING.png', project_dir + '/game/mod_assets')

    def mpt_copy():
        if glob.glob(config.basedir + '/templates/DDLC_Mood_Posing_Tool/game/mod_assets/MPT'):
            ddlc = config.basedir + '/templates/DDLC_Mood_Posing_Tool'
            mptver = 1
        elif glob.glob(config.basedir + '/templates/DDLC_MPT_v*'):
            ddlc = glob.glob(config.basedir + '/templates/DDLC_MPT_v*')
            mptver = 2
        else:
            ddlc = glob.glob(config.basedir + '/templates/MPT v*')
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
        os.mkdir(project_dir + '/game/mod_assets/MPT')
        for f in files:
            if mptver >= 2:
                shutil.move(ddlc[0]+'/'+f, project_dir + '/game/mod_assets/MPT')
            else:
                shutil.move(ddlc+'/'+f, project_dir + '/game/mod_assets/MPT')
        if mptver == 2:
            ddlc = glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/NOT DEFINED WARNING.png')
            shutil.move(ddlc[0], project_dir + '/game/mod_assets')
        else:
            if mptver == 3:
                pass
            else:
                shutil.move(persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/NOT DEFINED WARNING.png', project_dir + '/game/mod_assets')

    def mpt_extract_beta(mpt_path):
        with zipfile.ZipFile(mpt_path, "r") as z:
            z.extractall(persistent.projects_directory + "/temp")
            if glob.glob(persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/MPT'):
                ddlc = persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/MPT'
                mptver = 1
            elif glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/MPT'):
                ddlc = glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/MPT')[0]
                mptver = 2
            else:
                ddlc = persistent.projects_directory + '/temp/game/mod_assets/MPT'
                mptver = 3

        files = os.listdir(ddlc)
        os.mkdir(project_dir + '/game/mod_assets/MPT')
        for f in files:
            shutil.move(ddlc+'/'+f, project_dir + '/game/mod_assets/MPT')
        if glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/NOT DEFINED WARNING.png'):
            ddlc = glob.glob(persistent.projects_directory + '/temp/DDLC_MPT_v*/game/mod_assets/NOT DEFINED WARNING.png')[0]
            shutil.move(ddlc, project_dir + '/game/mod_assets')
        else:
            if mptver == 1:
                shutil.move(persistent.projects_directory + '/temp/DDLC_Mood_Posing_Tool/game/mod_assets/NOT DEFINED WARNING.png', project_dir + '/game/mod_assets')
            else:
                pass

    def mpt_copy_beta(mpt_path):
        files = os.listdir(mpt_path)
        for f in files:
            shutil.copytree(mpt_path+'/'+f, project_dir + '/game/mod_assets/MPT')
        ddlc = persistent.projects_directory + '/temp/MPT/game/mod_assets/MPT'
        files = os.listdir(ddlc)
        os.mkdir(project_dir + '/game/mod_assets/MPT')
        for f in files:
            shutil.move(ddlc+'/'+f, project_dir + '/game/mod_assets/MPT')
        if glob.glob(persistent.projects_directory + '/temp/MPT/game/mod_assets/NOT DEFINED WARNING.png'):
            ddlc = persistent.projects_directory + '/temp/MPT/game/mod_assets/NOT DEFINED WARNING.png'
            shutil.move(ddlc, project_dir + '/game/mod_assets')

label new_project_choice:

    python:

        project_choice = interface.choice(
            _("What kind of mod project do you want to make?"),
            [ ( 'new_project', _("Standard Mod Project") ), ( 'mpt', _("Mod Project with MPT")), ( 'mpt_beta', _("(BETA) Mod Project with MPT via File Selection") )],
            "new_project",
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
        if renpy.macintosh and persistent.safari:
            interface.info(_("Installing MPT requires you to download the {i}unpacked{/i} ZIP from it's original source."), _("Download MPT's ZIP file and place it in the 'templates' folder."),)
        else:
            interface.info(_("Installing MPT requires you to download the {i}unpacked{/i} ZIP from it's original source."), _("Download MPT's ZIP file and place it in the 'templates' folder."),)
        
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

            if renpy.macintosh and persistent.safari:
                pass
            else:
                if not glob.glob(config.basedir + '/templates/MPT v*') and not glob.glob(config.basedir + '/templates/DDLC_MPT-*_unpacked.*') and not glob.glob(config.basedir + '/templates/DDLC_MPT-*-unpacked.*'):
                    interface.error(_("MPT ZIP file cannot be found by glob."), _("Check if the ZIP exists or re-download the tool."))
                    break

            mptzipcount = 0
            if glob.glob(config.basedir + '/templates/DDLC_MPT-*-unpacked.*'):
                mptzipcount += 1
            if glob.glob(config.basedir + '/templates/DDLC_MPT-*_unpacked.*'):
                mptzipcount += 1
            if glob.glob(config.basedir + '/templates/MPT v*'):
                mptzipcount += 1

            if mptzipcount > 1:
                interface.error(_("Multiple MPT ZIP files are located in the templates directory."), _("Please remove older ZIP versions of MPT and try again."))
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

    return

default mpt_directory = None

label mpt_beta:
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
        interface.info(_("This feature is currently in beta and may have errors."), _("Report any errors to the Github Issues page if you encounter any here."),)
        if renpy.macintosh and persistent.safari:
            interface.info(_("Installing MPT requires you to download the {i}unpacked{/i} ZIP from it's original source."), _("Download MPT's ZIP file and prepare to select it."),)
        else:
            interface.info(_("Installing MPT requires you to download the {i}unpacked{/i} ZIP from it's original source."), _("Download MPT's ZIP file and prepare to select it."),)
        
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

            if project.manager.get(project_name) is not None:
                interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name, label=None)
                continue
            if os.path.exists(project_dir):
                interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir, label=None)
                continue

            if renpy.macintosh and persistent.safari:
                interface.interaction(_("MPT Folder"), _("Please choose the MPT Folder using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"),)

                mpt_path, is_default = choose_directory(mpt_directory)

                if is_default:
                    interface.error(_("Cancelled the Mod Making Process."),)

                mpt_directory = mpt_path

                if not "DDLC_Mood_Posing_Tool" in mpt_path and not "DDLC_MPT_v" in mpt_path and not "MPT v" in mpt_path:
                    interface.error(_("The ZIP file you chosen is not a MPT ZIP File. Please choose a valid MPT ZIP File."),)
                    continue

            else:
                interface.interaction(_("MPT ZIP"), _("Please choose the MPT ZIP File using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"),)

                mpt_path, is_default = choose_file(mpt_directory)

                if is_default:
                    interface.error(_("Cancelled the Mod Making Process."),)

                mpt_directory = mpt_path

                if not "DDLC_MPT-" in mpt_path and not "MPT v" in mpt_path:
                    interface.error(_("The ZIP file you chosen is not a MPT ZIP File. Please choose a valid MPT ZIP File."),)
                    continue

            if persistent.safari == True and renpy.macintosh:
                interface.interaction(_("Making a DDLC Folder"), _("Copying DDLC. Please wait..."))
                ddlc_copy()
            else:
                interface.interaction(_("Making a DDLC Folder"), _("Extracting DDLC. Please wait..."))
                zip_extract()

            interface.interaction(_("Installing Mod Template"), _("Please wait..."))
            template_extract()
            
            interface.interaction(_("Installing MPT"), _("Please wait..."))
            if renpy.macintosh and persistent.safari == True:
                mpt_copy_beta(mpt_path)
            else:
                mpt_extract_beta(mpt_path)
            
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