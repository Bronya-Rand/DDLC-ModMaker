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

    def game_installation(self, filePath, modFolder, copy=False):
        '''
        This define extracts the game/tool archive to the temp folder.

        filePath - The given game zip package.\n
        modFolder - The mod folder inside the mod install folder.\n
        copy - Makes sure this is a copy or a ZIP we are working with.
        '''

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

        for temp_src, dirs, files in os.walk(game_dir):
            dst_dir = temp_src.replace(game_dir, modFolder)
            
            for d in dirs:
                try: os.makedirs(os.path.join(dst_dir, d))
                except OSError: continue
            
            for f in files:
                shutil.move(os.path.join(temp_src, d), os.path.join(dst_dir, f))
        
        if not copy:
            shutil.rmtree(game_dir)

        if sys.platform == "darwin":
            try: os.remove(os.path.join(modFolder, "DDLC.app/Contents/Resources/autorun/game/scripts.rpa"))
            except: pass
        else:
            try: os.remove(os.path.join(modFolder, "game/scripts.rpa"))
            except: pass
            
    def installation(self, filePath, modFolder, copy=False):
        '''
        This define extracts the mod archive to the temp folder and installs it
        to the mod folder.
        
        filepath - The given mod zip package.\n
        modFolder - The mod folder inside the mod install folder.
        copy - Makes sure this is a copy or a ZIP we are working with.
        '''

        if not copy:

            with ZipFile(filePath, "r") as z:
                if sys.platform == "darwin":
                    z.extractall(os.path.join(modFolder, "DDLC.app/Contents/Resources/autorun"))
                else:
                    z.extractall(modFolder)

        else:
            mod_dir = filePath

            modFolder = os.path.join(modFolder, x, "Contents/Resources/autorun")

            for mod_src, dirs, files in os.walk(mod_dir):
                dst_dir = mod_src.replace(mod_dir, modFolder)
                
                for d in dirs:
                    try: os.makedirs(os.path.join(dst_dir, d))
                    except OSError: continue
                
                for f in files:
                    mod_file = os.path.join(mod_src, f)
                    dst_file = os.path.join(dst_dir, f)

                    if os.path.exists(dst_file):
                        if os.path.samefile(mod_file, dst_file):
                            continue

                        os.remove(dst_file)

                    shutil.move(mod_file, dst_file)
