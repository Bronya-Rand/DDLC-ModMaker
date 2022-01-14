
init python:
    import requests
    import glob
    import os
    import zipfile
    import json

    TEMPLATE_URL = "https://api.github.com/repos/GanstaKingofSA/DDLCModTemplate2.0/releases/latest"
    DDMM_URL = "https://api.github.com/repos/GanstaKingofSA/DDLC-ModMaker/releases/latest"
    TEMPLATE_JSON_PATH = config.basedir + "/update/template_current.json"
    DDMM_JSON_PATH = config.basedir + "/update/mmaker_current.json"
    
default persistent.update_available = False

label mmupdater(silent=False):

    python hide:
        template_update = False
        mmaker_update = False

        if not silent:
            interface.processing("Checking for updates...")

        try:
            requests.get("https://github.com")
            if datetime.date.today() > persistent.last_update_check or (not os.path.exists(TEMPLATE_JSON_PATH) or not DDMM_JSON_PATH):
                template_json = requests.get(TEMPLATE_URL).json()
                mmaker_json = requests.get(DDMM_URL).json()

                try:
                    template_json["documentation_url"] or mmaker_json["documentation_url"]
                    
                    if not silent:
                        interface.error("A Github server issue has occured.", "Please try updating later.")
                        renpy.jump("front_page")
                    else:
                        return
                except: pass
                
                if not os.path.exists(config.basedir + "/update"):
                    os.makedirs(config.basedir + "/update")

                with open(TEMPLATE_JSON_PATH, "w") as template_json_file:
                    json.dump(template_json, template_json_file)

                with open(DDMM_JSON_PATH, "w") as mmaker_json_file:
                    json.dump(mmaker_json, mmaker_json_file)
        except requests.exceptions.ConnectionError:
            if not silent:
                interface.error("You are either not connected to the internet or Github is currently down.", "Check your internet connection or try again later.")

        try:
            with open(TEMPLATE_JSON_PATH, "r") as tf:
                template_json = json.load(tf)
            with open(DDMM_JSON_PATH, "r") as mf:
                mmaker_json = json.load(mf)
        except:
            if not silent:
                interface.error("Unable to obtain update information from Github.", "Please try again later.")
                renpy.jump("front_page")
            else:
                return

        try:
            template_ver = tuple(int(num) for num in glob.glob("templates/DDLCModTemplate-*.zip")[-1].replace(".zip", "").split("-")[-1].split("."))
        except:
            template_ver = "null"

        if template_ver == "null" or template_ver < tuple(int(num) for num in template_json["tag_name"].split(".")):
            template_update = True

        for x in range(len(mmaker_json["assets"])):
            if tuple(int(num) for num in config.version.split(".")) < tuple(int(num) for num in mmaker_json["tag_name"].split(".")) and build.directory_name.split("-")[0] == mmaker_json["assets"][x]["name"].split("-")[0]:
                mmaker_update = True

        if template_update or mmaker_update:
            if silent:
                persistent.update_available = True
                return
            elif template_update and mmaker_update:
                update_text = "Updates are available. Do you wish to install these updates?\n{a=" + template_json["html_url"] + "}What's new for the DDLC Mod Template{/a}\n{a=" + mmaker_json["html_url"] + "}What's new for DDMM/DDMMaker{/a}"
            elif template_update:
                update_text = "A DDLC Mod Template update is available. Do you wish to install this update?\n{a=" + template_json["html_url"] + "}What's new for the DDLC Mod Template{/a}"
            elif mmaker_update:
                update_text = "A DDMM/DDMMaker update is available. Do you wish to install this update?\n{a=" + mmaker_json["html_url"] + "}What's new for DDMM/DDMMaker{/a}"

            update_response = interface.choice(update_text, 
                [ ( 'yes', _("Yes") ), ( 'no', _("No")) ],
                "yes",
                cancel=Jump("front_page"),
            )
            
            if update_response == "yes":
                renpy.call("mmupdate", template_update, mmaker_update)

        else:
            if persistent.update_available:
                persistent.update_available = False
            if not silent:
                interface.info("Everything is up to date.", "Current Versions:\n" + template_json["name"] + "\n" + mmaker_json["name"])
                
    if silent:
        return
    else:            
        jump front_page

label mmupdate(template_update, mmaker_update):

    python hide:

        if template_update:

            with interface.error_handling("Updating the DDLC Mod Template"):
                interface.processing("Updating the DDLC Mod Template. Please wait...")

                zipContent = requests.get("https://github.com/GanstaKingofSA/DDLCModTemplate2.0/releases/download/" + ver + "/DDLCModTemplate-" + ver + ".zip")
                filename = "DDLCModTemplate-" + ver + ".zip"

                try: os.remove(glob.glob("templates/DDLCModTemplate-*.zip")[-1])
                except: pass

                with open(config.basedir + "/templates/" + filename, "wb") as newTemplate:
                    newTemplate.write(zipContent.content) 
        
        if mmaker_update:

            with interface.error_handling("Updating DDMM/DDMMaker"):
                interface.processing("Updating DDMM/DDMMaker. Please wait...")

                zipContent = requests.get("https://github.com/GanstaKingofSA/DDLC-ModMaker/releases/download/" + ver + "/" + build.directory_name.split("-")[0] + "-" + ver + "-sdk.zip")
                filename = build.directory_name.split("-")[0] + "-" + ver + "-sdk.zip"

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
                            if os.path.samefile(update_file, dst_file):
                                continue

                            os.remove(dst_file)

                        shutil.move(update_file, dst_file)

                shutil.rmtree(filename.replace(".zip", ""))
                os.remove(filename)

        persistent.update_available = False

        if template_update and mmaker_update:
            interface.info("The updates has been complete. DDMM/DDMMaker will now restart.")
            renpy.quit(True)
        elif mmaker_update:
            interface.info("The update has been complete. DDMM/DDMMaker will now restart.")
            renpy.quit(True)
        else:
            interface.info("The update has been complete.")

    jump front_page
