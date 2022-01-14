
import os

class ModManagement:
    '''
    This class manages what the user can do to a mod in the mod launcher.
    '''

    def delete_mod(self, modFolder, modName):
        '''
        This define deletes a mod folder from the mod install folder if
        confirmed by the user.
        '''

        for mod_src, dirs, files in os.walk(os.path.join(modFolder, modName)):
            for f in files:
                os.remove(os.path.join(mod_src, f))
            
            for d in dirs:
                os.remove(os.path.join(mod_src, d))

        os.remove(os.path.join(modFolder, modName))
