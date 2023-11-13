from . import MMakerGithubTool
import requests
from zipfile import ZipFile
from renpy import PY2

class ModTool(MMakerGithubTool):

    def __init__(self):
        super().__init__("GanstaKingofSA/DDLCModTemplate2.0", "python-2", "DDLCModTemplate", tool=False)

    def update(self):
        git_ver = self.get_remote_tool_version()
        if PY2:
            pkg_url = self.package_url + "{}/{}-{}.zip".format(git_ver, self.package_file, git_ver)
        else:
            pkg_url = self.package_url + "{}/{}-{}-Py3.zip".format(git_ver, self.package_file, git_ver)
        
        zipContent = requests.get(pkg_url)
        filepath = "{}/{}.zip".format(self.install_dir, self.package_file)

        with open(filepath, "wb") as newTemplate:
            newTemplate.write(zipContent.content)

            with ZipFile(filepath) as newTemplate:
                newTemplate.extract("Documentation/Android Mod Guide.pdf", self.install_dir)

    def install_package(self):
        self.update()

    def install(self, mod_folder):
        if not self.check_if_installed():
            self.install_package()

        filepath = "{}/{}.zip".format(self.install_dir, self.package_file)

        with ZipFile(filepath, "r") as z:
            z.extractall(mod_folder)
    