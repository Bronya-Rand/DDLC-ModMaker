
from zipfile import ZipFile
import tempfile
import os
import shutil
import sys

class Extractor:
    '''
    This class is responsible for the extraction of
    zip files for DDLC mods.
    '''

    def __init__(self):
        self.renpy_script_contents = ('.rpa', '.rpyc', '.rpy')
        self.renpy_folder_contents = ('audio', 'images', 'gui', 'bgm', 'sfx', 
                                    'mod_assets', 'videos', 'fonts')
        self.renpy_base_contents = ('game', 'lib', 'renpy')
        self.renpy_executables = ('.exe', '.sh', '.py', '.app')

    def valid_zip(self, filePath):
        '''
        This define checks if the ZIP is a valid DDLC mod.
        archive.
        '''

        contents = []

        with ZipFile(filePath, "r") as z:
            contents = z.namelist()

        for x in contents:
            if x.endswith((self.renpy_script_contents)):
                contents = []
                return True
                
        return False

    def game_installation(self, filePath, modFolder, tool=False, copy=False):
        '''
        This define extracts the game/tool archive to the temp folder.

        filePath - The given game zip package.\n
        modFolder - The mod folder inside the mod install folder.\n
        tool - Makes sure this is a tool ZIP or folder we are working with.
        copy - Makes sure this is a copy or a ZIP we are working with.
        '''

        if not tool:
            os.makedirs(modFolder)

        if not copy:
            td = tempfile.mkdtemp(prefix="NewDDML_",suffix="_TempGame")

            with ZipFile(filePath, "r") as z:
                z.extractall(td)

            if sys.platform == "darwin":
                game_dir = td
            else:
                game_dir = os.path.join(td, os.listdir(td)[-1])
        else:
            game_dir = filePath

        for contents in os.listdir(game_dir):

            if os.path.isdir(os.path.join(game_dir, contents)):

                shutil.copytree(os.path.join(game_dir, contents), 
                                os.path.join(modFolder, contents))

            else:

                shutil.copy2(os.path.join(game_dir, contents), 
                            os.path.join(modFolder, contents))

        if not copy:
            shutil.rmtree(td)
            
    def installation(self, filePath, modFolder, copy = False):
        '''
        This define extracts the mod archive to the temp folder and installs it
        to the mod folder.
        
        filepath - The given mod zip package.\n
        modFolder - The mod folder inside the mod install folder.
        copy - Makes sure this is a copy or a ZIP we are working with.
        '''

        if not copy:
            td = tempfile.mkdtemp(prefix="NewDDML_",suffix="_TempArchive")

            with ZipFile(filePath, "r") as z:
                z.extractall(td)
        else:
            td = filePath
        
        if len(os.listdir(td)) > 1 or "game" in os.listdir(td):
            os.makedirs(os.path.join(td, "ImproperMod"))

            for x in os.listdir(td):

                if x != "ImproperMod":

                    if (not x.endswith(self.renpy_executables) and not x in self.renpy_base_contents 
                        or x in self.renpy_folder_contents):

                        if not os.path.exists(os.path.join(td, "ImproperMod", "game")):
                            os.makedirs(os.path.join(td, "ImproperMod", "game"))

                        shutil.move(os.path.join(td, x), os.path.join(td, "ImproperMod", "game", x))

                    else:

                        if x == "game" and os.path.exists(os.path.join(td, "ImproperMod", "game")):

                            for y in os.listdir(os.path.join(td, "game")):
                                if os.path.isdir(os.path.join(td, "game", y)):
                                    shutil.move(os.path.join(td, "game", y), 
                                                os.path.join(td, "ImproperMod", "game", y))
                                else:
                                    shutil.copy2(os.path.join(td, "game", y), 
                                                os.path.join(td, "ImproperMod", "game", y))

                            shutil.rmtree(os.path.join(td, "game"))
                        else:
                            shutil.move(os.path.join(td, x), os.path.join(td, "ImproperMod", x))

        mod_dir = os.path.join(td, os.listdir(td)[-1])

        if sys.platform == "darwin":
            for x in os.listdir(modFolder):
                if x.endswith(".app"):
                    modFolder = os.path.join(modFolder, x, 
                                "Contents/Resources/autorun")

        for contents in os.listdir(mod_dir):

            if contents == "game":

                for x in os.listdir(os.path.join(mod_dir, contents)):

                    if os.path.isdir(os.path.join(mod_dir, contents, x)):

                        if os.path.exists(os.path.join(modFolder, contents, x)):
                            shutil.rmtree(os.path.join(modFolder, contents, x))

                        shutil.copytree(os.path.join(mod_dir, contents, x), 
                                        os.path.join(modFolder, contents, x))
                    else:

                        if os.path.exists(os.path.join(modFolder, contents, x)):
                            os.remove(os.path.join(modFolder, contents, x))

                        shutil.copy2(os.path.join(mod_dir, contents, x), 
                                    os.path.join(modFolder, contents, x))

            elif os.path.isdir(os.path.join(mod_dir, contents)):

                if os.path.exists(os.path.join(modFolder, contents)):
                    shutil.rmtree(os.path.join(modFolder, contents))

                shutil.copytree(os.path.join(mod_dir, contents), 
                                os.path.join(modFolder, contents))

            else:

                if os.path.exists(os.path.join(modFolder, contents)):
                    os.remove(os.path.join(modFolder, contents))

                shutil.copy2(os.path.join(mod_dir, contents), os.path.join(modFolder, contents))

        if not copy:
            shutil.rmtree(td)
