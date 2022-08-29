from zipfile import ZipFile
import tempfile
import os
import shutil
import sys


class Extractor:
    """
    This class is responsible for the extraction of
    zip files for DDLC mods.
    """

    def __init__(self):
        self.renpy_script_contents = (".rpa", ".rpyc", ".rpy")

    def valid_zip(self, filePath):
        """
        This define checks if the ZIP is a valid DDLC mod.
        archive.
        """

        contents = []

        with ZipFile(filePath, "r") as z:
            contents = z.namelist()

        for x in contents:
            if x.endswith((self.renpy_script_contents)):
                contents = []
                return True

        return False

    def game_installation(self, filePath, modFolder, copy=False):
        if not copy:
            td = tempfile.mkdtemp(prefix="NewDDML_", suffix="_TempGame")

            with ZipFile(filePath, "r") as z:
                z.extractall(td)

            if sys.platform == "darwin":
                game_dir = td
            else:
                game_dir = os.path.join(td, os.listdir(td)[-1])
        else:
            game_dir = filePath

        for temp_src, dirs, files in os.walk(game_dir + "/game"):
            for f in files:
                base, ext = os.path.splitext(f)

                if not (ext in self.renpy_script_contents):
                    continue

                if base != "scripts":
                    src_dir = os.path.join(temp_src, f)
                    dst_dir = src_dir.replace(temp_src, os.path.join(modFolder, "game"))
                    shutil.move(src_dir, dst_dir)

        if not copy:
            shutil.rmtree(game_dir)

    def installation(self, filePath, modFolder):
        os.makedirs(modFolder)

        with ZipFile(filePath, "r") as z:
            z.extractall(modFolder)
