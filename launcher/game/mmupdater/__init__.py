import abc
import datetime
import importlib
import os
import requests
import json
from renpy import config, store

class MMakerTool(abc.ABC):
    def __init__(self, name: str, acronym: str, creator: str, desc: str, restart=False, tool=True):
        for x in (name, acronym, creator, desc):
            if not isinstance(x, str):
                raise Exception("A argurment provided is not type string")

        self.name = name
        self.acronym = acronym
        self.creator = creator
        self.desc = desc
        self.restart = restart
        self.install_dir = config.gamedir + "/mmupdater/data/{}".format(acronym)
        self.tool = tool

        os.makedirs(config.gamedir + "/mmupdater/data/{}".format(acronym), exist_ok=True)
        
    @abc.abstractmethod
    def install(self, mod_folder):
        """Installs the tool."""
        pass

    @abc.abstractmethod
    def get_updates(self):
        """Gets the updates for the tool."""
        pass

    @abc.abstractmethod
    def update(self, *args):
        """Updates the tool to the latest version."""
        pass

    @abc.abstractmethod
    def check_for_updates(self) -> bool:
        """Checks for updates for the tool."""
        pass

    def check_if_installed(self) -> bool:
        """Checks if the tool is installed on the system."""
        return os.path.exists(self.install_dir)
    
    def get_local_tool_version(self):
        version = None

        for x in ("first_party", "third_party"):
            with open(config.basedir + "/update/{}.json".format(x)) as v:
                pkgs = json.load(v)
                try:
                    version = pkgs[self.acronym]['version']
                except KeyError:
                    pass

        return version
    
    @abc.abstractmethod
    def get_remote_tool_version(self):
        pass

    @abc.abstractmethod
    def install_package(self):
        pass

class MMakerGithubTool(MMakerTool):
    def __init__(self, github_name: str, github_branch: str, package_name: str, name: str = None, acronym: str = None, creator: str = None, desc: str = None, restart=False, tool=True, extra=False):
        if not isinstance(github_name, str):
            raise Exception("Github Repo Name must be provided.")

        if len(github_name.split("/")) != 2:
            raise Exception("Github Repo Name must begin with 'GithubUsername/GithubRepo' e.g. 'bronya_rand/a-ddlc-repo'.")
        if github_branch is None:
            raise Exception("Github Branch Name must be provided.")
        if extra and (name is None or acronym is None or desc is None):
            raise Exception("Name/Acronym/Description of Extra must be provided if this is a Github Extra Mod Package.")
        if not isinstance(package_name, str):
            raise Exception("package name is not a type string.")
        
        self.github_name = github_name

        gh_json = requests.get("https://raw.githubusercontent.com/{}/{}/ddmm_metadata.json".format(github_name, github_branch))
        if gh_json.status_code in (400, 404):
            super().__init__(name, acronym, creator, desc, restart, tool)
        else:
            try:
                gh_data = gh_json.json()
            except json.JSONDecodeError:
                raise Exception(gh_json.status_code)
            if extra:
                super().__init__(name, acronym, gh_data["creator"], desc, gh_data['restart'], tool)
            else:
                super().__init__(gh_data['name'], gh_data['acronym'], gh_data["creator"], gh_data["description"], gh_data['restart'], tool)

        self.package_url = "https://github.com/{}/releases/download/".format(github_name)
        self.package_file = package_name

    def check_if_installed(self) -> bool:
        return os.path.exists(self.install_dir + "/{}.zip".format(self.package_file))

    def get_updates(self):
        package_update_data = requests.get("https://api.github.com/repos/{}/releases/latest".format(self.github_name)).json()
        with open(self.install_dir + "/update.json", "w") as pud:
            json.dump(package_update_data, pud)
    
    def get_remote_tool_version(self):
        with open(self.install_dir + "/update.json", "r") as pud:
            temp = json.load(pud)
            return temp["tag_name"]
        
    def check_for_updates(self) -> bool:
        if not self.check_if_installed():
            return False
        
        if store.persistent.daily_update_check and ((not store.persistent.last_update_check) or (datetime.date.today() > store.persistent.last_update_check)):
            self.get_updates()
            store.persistent.last_update_check = datetime.date.today()
        
        local_ver = self.get_local_tool_version()
        if local_ver is None:
            return True
        local_ver_tuple = tuple(int(num) for num in local_ver.split("."))

        remote_ver = self.get_remote_tool_version()
        remote_ver_tuple = tuple(int(num) for num in remote_ver.split("."))
        
        if local_ver_tuple < remote_ver_tuple:
            return True
        
        return False

class MMakerUpdater(object):
    def __init__(self):
        self.all_modules = {}
        directory = "{}/{}".format(config.gamedir, "mmupdater")
        # Import all Python files in the directory
        i = 0

        for filename in os.listdir(directory):
            if "__init__" in filename:
                continue

            if filename.endswith(".py"):
                module_name = filename[:-3]
                full_module_name = "mmupdater.{}".format(module_name)
                
                importlib.import_module(full_module_name)
                self.all_modules[i] = full_module_name
                i += 1