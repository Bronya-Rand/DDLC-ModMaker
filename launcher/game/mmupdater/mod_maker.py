from . import MMakerGithubTool
import requests
import os
from zipfile import ZipFile
from renpy import config
import renpy
import shutil

class ModTool(MMakerGithubTool):

    def __init__(self):
        super(ModTool, self).__init__(github_name="GanstaKingofSA/DDLC-ModMaker",
                        github_branch="mmaker-7.4",
                        package_name="DDMMaker",
                        name="Doki Doki Mod Maker",
                        acronym="DDMM",
                        creator="bronya_rand",
                        desc="DDMM is a Ren'Py SDK Modification that makes DDLC Modding easier and efficient with better wording, auto-tool install, and more! This tool adheres to the Team Salvato IP Guidelines and RenpyTom Guidelines for DDLC and Ren'Py SDK modding.",
                        restart=True, tool=False)

    def update(self):
        git_ver = self.get_remote_tool_version()
        rpy_num = renpy.version_tuple[0] # Easier said than done
        pkg_url = self.package_url + self.package_file + "{}-{}-sdk.zip".format(rpy_num, git_ver)

        zipContent = requests.get(pkg_url)
        filepath = "{}/{}".format(self.install_dir, self.package_file)

        try: 
            os.remove(filepath)
        except: pass

        with open(filepath, "wb") as newTemplate:
            newTemplate.write(zipContent.content)

        with ZipFile(filepath, "r") as z:
            z.extractall("{}".format(self.install_dir))

        ddmm_file = "{}/DDMMaker.zip".format(self.install_dir)

        for update_src, dirs, files in os.walk(ddmm_file):
            dst_dir = update_src.replace(ddmm_file, config.basedir)
            
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
        
        os.remove("{}/temp".format(self.install_dir))
        os.remove("{}/{}".format(self.install_dir, self.package_file))

    def install_package(self):
        # We don't use this for DDMM
        pass

    def install(self, mod_folder):
        # We don't use this for DDMM
        pass
    