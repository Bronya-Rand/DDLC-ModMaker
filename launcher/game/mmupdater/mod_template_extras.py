from . import MMakerGithubTool
import requests
from zipfile import ZipFile
from renpy import PY2

class ModTool(MMakerGithubTool):

    def __init__(self):
        super().__init__(
                        github_name="GanstaKingofSA/DDLCModTemplate2.0", 
                        github_branch="python-2",
                        name="DDLC Mod Template 2.0 - Extras",
                        acronym="DDMT-Extras",
                        desc="An extension to the DDLC Mod Template 2.0 that adds additional features to the mod template. {u}This is the Python 3 Edition of the mod template extras and is not compatible with DDMM 6-7/Ren'Py 6-7{/u}.", 
                        package_name="DDLCModTemplate-Py3Extras" if not PY2 else "DDLCModTemplate-Py2Extras",
                        restart=False, extra=True
                        )

    def update(self):
        git_ver = self.get_remote_tool_version()
        if PY2:
            pkg_url = self.package_url + "{}/DDLCModTemplate-{}-Extras.zip".format(git_ver, git_ver)
        else:
            pkg_url = self.package_url + "{}/DDLCModTemplate-{}-Py3Extras.zip".format(git_ver, git_ver)

        zipContent = requests.get(pkg_url)
        filepath = "{}/{}.zip".format(self.install_dir, self.package_file)

        with open(filepath, "wb") as newTemplate:
            newTemplate.write(zipContent.content)

    def install_package(self):
        self.update()

    def install(self, mod_folder):
        if not self.check_if_installed():
            self.install_package()

        filepath = "{}/{}.zip".format(self.install_dir, self.package_file)

        with ZipFile(filepath, "r") as z:
            z.extractall(mod_folder)
    