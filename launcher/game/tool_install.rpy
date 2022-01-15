
init python:
    import sys
    import glob
    from zipfile import ZipFile
    import tempfile

label tool_install:

    python hide:
        gamedir = False

        if renpy.macintosh:
            project_dir = os.path.join(persistent.projects_directory, project.current.name, "DDLC.app/Contents/Resources/autorun")
        else:
            project_dir = os.path.join(persistent.projects_directory, project.current.name)

        interface.info("This installer is in beta. Not all mod tools will install properly.", "Make sure to backup your project if anything fails.")

        if renpy.macintosh and persistent.safari:
            interface.interaction(_("Tool Folder"), _("Please select the tool folder you wish to install."),)

            path, is_default = choose_directory(None, True)
        else:
            interface.interaction(_("Tool ZIP File"), _("Please select the tool ZIP file you wish to install."),)

            path, is_default = choose_file(None, True)

        if is_default:
            interface.error(_("The operation has been cancelled."))
            renpy.jump("front_page")

        if not path.endswith(".zip"):
            interface.error(_("The tool you are trying to install is not in a ZIP file."), "Make sure it is a valid ZIP or convert it to a ZIP file.")
            renpy.jump("front_page")
            
        response = interface.choice("Are you sure you want to install " + path.replace("\\", "/").split("/")[-1].replace(".zip", "") + " to [project.current.name]?\nThis action cannot be reversed.",
                        [ ('yes', "Yes"), ('no', "No") ],
                        "no",
                        cancel=Jump("front_page")
                    )
        
        if response != "yes":
            interface.error(_("The operation has been cancelled."))
            renpy.jump("front_page")
        else:
            interface.processing("Installing Tool. Please wait...")
            
            with interface.error_handling("installing user tool"):
                if renpy.macintosh and persistent.safari:
                    tool_dir = path
                else:
                    td = tempfile.mkdtemp(prefix="DDMM_",suffix="_TempTool")
                    with ZipFile(path, "r") as z:
                        z.extractall(td)
                        
                if glob.glob(td + "/game"):
                    tool_dir = td
                elif glob.glob(td + "/*/game"):
                    tool_dir = td + "/" + glob.glob(td + "/*/game")[0].replace("\\", "/").split("/")[-2]
                else:
                    tool_dir = td
                    gamedir = True
                
        for tool_src, dirs, files in os.walk(tool_dir):
            if gamedir:
                dst_dir = tool_src.replace(tool_dir, project_dir + "/game")
            else:
                dst_dir = tool_src.replace(tool_dir, project_dir)
            
            for d in dirs:
                if not os.path.exists(os.path.join(dst_dir, d)):
                    os.makedirs(os.path.join(dst_dir, d))
        
            for f in files:
                temp_file = os.path.join(tool_src, f)
                dst_file = os.path.join(dst_dir, f)
                
                if os.path.exists(dst_file):
                    if os.path.samefile(temp_file, dst_file):
                        continue

                    os.remove(dst_file)

                shutil.move(temp_file, dst_file)

        if not renpy.macintosh and not persistent.safari:
            shutil.rmtree(td)
                
        interface.info("DDMM/DDMMaker successfully installed the selected tool to [project.current.name].")
    
    jump front_page