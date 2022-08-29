
init python:
    import sys
    import glob
    from zipfile import ZipFile
    import tempfile

label tool_install:

    python:
        gamedir = False
        confirm_install = False

        if renpy.macintosh:
            project_dir = os.path.join(persistent.projects_directory, project.current.name, "DDLC.app/Contents/Resources/autorun")
        else:
            project_dir = os.path.join(persistent.projects_directory, project.current.name)

        interface.info("This installer is in beta. Not all mod tools will install properly and may require changes before launch.", "Make sure to backup your project if anything fails.")

        if renpy.macintosh and persistent.safari:
            interface.interaction(_("Tool Folder"), _("Please select the tool folder you wish to install."),)

            path, is_default = choose_directory(None)
        else:
            interface.interaction(_("Tool ZIP File"), _("Please select the tool ZIP file you wish to install."),)

            path, is_default = choose_file(None)

        if is_default:
            interface.error(_("The operation has been cancelled."))
            renpy.jump("front_page")
        
        interface.yesno(
            label=_("Deleting a Project"),
            message=_("Are you sure you want to delete."),
            filename=False,
            yes=[SetVariable("confirm_install", True), Return()],
            no=Return(),
            cancel=Jump("front_page"))
        
        if not confirm_install:
            renpy.jump("front_page")
        else:
            interface.processing("Installing Tool. Please wait...")
            
            with interface.error_handling("extracting user tool"):
                if renpy.macintosh and persistent.safari:
                    td = path
                else:
                    td = tempfile.mkdtemp(prefix="DDMM_",suffix="_TempTool")
                    with ZipFile(path, "r") as z:
                        z.extractall(td)

                tool_dir = None 
                for src, dirs, files in os.walk(td):
                    for d in dirs:
                        if d in ["game", "mod_assets", "python-packages"]:
                            if "game" in d:
                                tool_dir = os.path.join(src, d)
                                gamedir = True
                            else:
                                tool_dir = os.path.join(src, d).replace("\\" + d, "")
                                gamedir = True
                            break
                if tool_dir is None:
                    # Assume the best is the src + subfolder itself
                    tool_dir = os.path.join(td, os.listdir(td)[-1])
                    
            with interface.error_handling("extracting user tool pt2"):      
                for tool_src, dirs, files in os.walk(tool_dir):
                    if gamedir:
                        dst_dir = tool_src.replace(tool_dir, project_dir + "/game")
                    else:
                        dst_dir = tool_src.replace(tool_dir, project_dir  + "/game/mod_assets")
                    
                    for d in dirs:
                        if not os.path.exists(os.path.join(dst_dir, d)):
                            os.makedirs(os.path.join(dst_dir, d))
                
                    for f in files:
                        temp_file = os.path.join(tool_src, f)
                        dst_file = os.path.join(dst_dir, f)
                        
                        if os.path.exists(dst_file):
                            if renpy.windows:
                                if os.stat(temp_file) == os.stat(dst_file):
                                    continue
                            else:
                                if os.path.samefile(temp_file, dst_file):
                                    continue

                            os.remove(dst_file)

                        shutil.move(temp_file, dst_file)

            if not renpy.macintosh and not persistent.safari:
                shutil.rmtree(td)
                
        interface.info("DDMM/DDMMaker successfully installed the selected tool to [project.current.name].")
    
    jump front_page