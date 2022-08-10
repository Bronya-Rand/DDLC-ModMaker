
init python:
    import requests
    import glob
    import os
    import zipfile
    import json
    import datetime

    TEMPLATE_URL = "https://api.github.com/repos/GanstaKingofSA/DDLCModTemplate2.0/releases/latest"
    DDMM_URL = "https://api.github.com/repos/GanstaKingofSA/DDLC-ModMaker/releases/latest"
    TEMPLATE_JSON_PATH = config.basedir + "/update/template_current.json"
    DDMM_JSON_PATH = config.basedir + "/update/mmaker_current.json"

    def get_git_template_version(template_json):
        return tuple(int(num) for num in template_json["tag_name"].split("."))

    def get_installed_template_version(string=False):
        if string: 
            num = glob.glob(config.basedir + "/templates/DDLCModTemplate-*.zip")
            return num[-1].replace(".zip", "").split("-")[-1] or "null"
        return tuple(int(num) for num in glob.glob(config.basedir + "/templates/DDLCModTemplate-*.zip")[-1].replace(".zip", "").split("-")[-1].split("."))

    def get_git_ddmm_version(mmaker_json_file):
        return tuple(int(num) for num in mmaker_json_file["tag_name"].split("."))
    
    def get_installed_ddmm_version():
        return tuple(int(num) for num in config.version.split("."))

    def fetch_ddmm_updates(quiet=True, mt=False, update_json=True):
        if not quiet:
            process_text = ""
            if mt:
                process_text += "Mod Template"
            else:
                process_text += "DDMM"
            interface.processing(_("Checking for {} updates").format(process_text))

        if not quiet:
            with interface.error_handling(_("Downloading the latest JSON information")):
                if mt:
                    channels = requests.get(TEMPLATE_URL).json()
                    if update_json or not os.path.exists(TEMPLATE_JSON_PATH):
                        with open(TEMPLATE_JSON_PATH, "w") as template_json_file:
                            json.dump(channels, template_json_file)
                else:
                    channels = requests.get(DDMM_URL).json()
                    if update_json or not os.path.exists(DDMM_JSON_PATH):
                        with open(DDMM_JSON_PATH, "w") as mmaker_json_file:
                            json.dump(channels, mmaker_json_file)
        else:
            if mt:
                channels = requests.get(TEMPLATE_URL).json()
                if update_json or not os.path.exists(TEMPLATE_JSON_PATH):
                    with open(TEMPLATE_JSON_PATH, "w") as template_json_file:
                        json.dump(channels, template_json_file)
            else:
                channels = requests.get(DDMM_URL).json()
                if update_json or not os.path.exists(DDMM_JSON_PATH):
                    with open(DDMM_JSON_PATH, "w") as mmaker_json_file:
                        json.dump(channels, mmaker_json_file)

        if mt:
            persistent.template_update = False
            with open(TEMPLATE_JSON_PATH, "r") as tf:
                template_json = json.load(tf)

            try:
                template_ver = get_installed_template_version()
            except:
                template_ver = "null"

            if template_ver == "null" or template_ver < get_git_template_version(template_json):
                if not persistent.disable_mt_update:
                    persistent.update_available = True
                    persistent.template_update = True
        
        else:
            persistent.mmaker_update = False
            with open(DDMM_JSON_PATH, "r") as mf:
                mmaker_json = json.load(mf)

            if get_installed_ddmm_version() < get_git_ddmm_version(mmaker_json):
                if not persistent.disable_mm_update:
                    persistent.update_available = True
                    persistent.mmaker_update = True

        return channels

label mmupdater:

    $ ddmm_chan = fetch_ddmm_updates(False)
    $ ddmt_chan = fetch_ddmm_updates(False, True)
    call screen ddmmupdate(ddmm_chan, ddmt_chan)

    jump front_page

screen ddmmupdate(ddmm_chan, ddmt_chan):

    frame:
        style_group "l"
        style "l_root"

        window:

            has viewport:
                scrollbars "vertical"
                mousewheel True

            has vbox

            label _("DDMM Updater")

            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    has vbox

                    if persistent.update_available:
                        text _("A update for DDMM or the DDLC Mod Template is now available. Select the update you want to install to proceed.")
                    else:
                        text _("No Updates Are Available.")

                    add SPACER

                    if persistent.mmaker_update:
                        textbutton "Doki Doki Mod Maker (DDMM/DDMMaker) for Ren'Py 7 - Update Available":
                            action [Call("install_ddmm_update_script", ddmm_chan), Jump("mmupdater")]
                    else:
                        if persistent.disable_mm_update:
                            textbutton "Doki Doki Mod Maker (DDMM/DDMMaker) for Ren'Py 7 - Updates Disabled":
                                action NullAction()
                        else:
                            textbutton "Doki Doki Mod Maker (DDMM/DDMMaker) for Ren'Py 7":
                                action NullAction()
                    text "Version Installed: {} | Latest Version: {}".format(config.version, ddmm_chan["tag_name"])
                    text "This is the program you are running to build DDLC mods on! Self-explanatory already."
                    text "{a=" + ddmm_chan["html_url"] + "}What's new for DDMM/DDMMaker?{/a}"

                    add SPACER

                    if persistent.template_update:
                        textbutton "The DDLC Mod Template - Version 2.0 (Python 2 Edition) - Update Available":
                            action [Call("install_ddmt_update_script", ddmt_chan), Jump("mmupdater")]
                    else:
                        if persistent.disable_mt_update:
                            textbutton "The DDLC Mod Template - Version 2.0 (Python 2 Edition) - Updates Disabled":
                                action NullAction()
                        else:
                            textbutton "The DDLC Mod Template - Version 2.0 (Python 2 Edition)":
                                action NullAction()
                    text "Version Installed: {} | Latest Version: {}".format(get_installed_template_version(True), ddmt_chan["tag_name"])
                    text "The DDLC Mod Template - Version 2.0 is the latest template for DDLC that allows modders to easily mod DDLC to their hearts content. {u}This is the Python 2 Edition of the template and is not compatible with DDMM 8/Ren'Py 8{/u}."
                    text "{a=" + ddmt_chan["html_url"] + "}What's new for the DDLC Mod Template - Version 2.0 (Python 2 Edition)?{/a}"

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label install_ddmt_update_script(ddmt_chan):

    python hide:
        with interface.error_handling("Updating the DDLC Mod Template"):
            interface.processing("Updating the DDLC Mod Template. Please wait...")

            zipContent = requests.get("https://github.com/GanstaKingofSA/DDLCModTemplate2.0/releases/download/" + ddmt_chan["tag_name"] + "/DDLCModTemplate-" + ddmt_chan["tag_name"] + ".zip")
            filename = "DDLCModTemplate-" + ddmt_chan["tag_name"] + ".zip"

            try: 
                for x in glob.glob("templates/DDLCModTemplate-*.zip"):
                    os.remove(x)
            except: pass

            with open(config.basedir + "/templates/" + filename, "wb") as newTemplate:
                newTemplate.write(zipContent.content) 

            with zipfile.ZipFile(config.basedir + "/templates/" + filename) as newTemplate:
                newTemplate.extract("guide.pdf", config.basedir + "/templates")

            persistent.update_available = False
            interface.info("The update has been complete.")

    jump mmupdater

label install_ddmm_update_script(ddmm_chan):

    python hide:
        
        with interface.error_handling("Updating DDMM/DDMMaker"):
            interface.processing("Updating DDMM/DDMMaker. Please wait...")

            zipContent = requests.get("https://github.com/GanstaKingofSA/DDLC-ModMaker/releases/download/" + ddmm_chan["tag_name"] + "/" + build.directory_name.split("-")[0] + "-" + ddmm_chan["tag_name"] + "-sdk.zip")
            filename = build.directory_name.split("-")[0] + "-" + ddmm_chan["tag_name"] + "-sdk.zip"

            with open(config.basedir + "/" + filename, "wb") as newMMaker:
                newMMaker.write(zipContent.content) 
            
            with zipfile.ZipFile(filename, "r") as z:
                z.extractall(config.basedir)

            for update_src, dirs, files in os.walk(config.basedir + "/" + filename.replace(".zip", "")):
                dst_dir = update_src.replace(config.basedir + "/" + filename.replace(".zip", ""), config.basedir)
                
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                
                for f in files:
                    update_file = os.path.join(update_src, f)
                    dst_file = os.path.join(dst_dir, f)

                    if os.path.exists(dst_file):
                        if renpy.windows:
                            if os.stat(update_file) == os.stat(dst_file):
                                continue
                        else:
                            if os.path.samefile(update_file, dst_file):
                                continue

                        os.remove(dst_file)

                    shutil.move(update_file, dst_file)

            shutil.rmtree(filename.replace(".zip", ""))
            os.remove(filename)

            persistent.update_available = False

            interface.info("The update has been complete. DDMM/DDMMaker will now restart.")
            renpy.quit(True)

    jump mmupdater
