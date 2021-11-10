
import os
import shutil
import sys

class ModManagement:
    '''
    This class manages what the user can do to a mod in the mod launcher.
    '''

    def delete_mod(self, modFolder, modName):
        '''
        This define deletes a mod folder from the mod install folder if
        confirmed by the user.
        '''

        shutil.rmtree(os.path.join(modFolder, modName))

    def move_mod_folder(self, modFolder, newModFolder):
        '''
        This define moves the contents of the old mod install folder to the new
        mod install folder.
        '''

        for x in os.listdir(modFolder):
            if os.path.isdir(os.path.join(modFolder, x)):
                shutil.move(os.path.join(modFolder, x), 
                            os.path.join(newModFolder, x))
            else:
                shutil.copy2(os.path.join(modFolder, x), 
                            os.path.join(newModFolder, x))

    def delete_rpa(self, modFolder, rpaName):
        '''
        This define deletes a RPA from the mod folder if confirmed by the user.
        '''

        if sys.platform == "darwin":
            for x in os.listdir(modFolder):
                if x.endswith(".app"):
                    modFolder = os.path.join(modFolder, x, 
                                "Contents/Resources/autorun/game")
        else:
            modFolder = os.path.join(modFolder, "game")

        os.remove(os.path.join(modFolder, rpaName))
