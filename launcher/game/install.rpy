# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init python:
    import fnmatch
    import re
    import zipfile
    import glob

    def install_from_zip(name, zipglob, patterns, tool=False):

        # Determine the filename matching the zipglob, and put it into filename.
        filenames = [ i for i in os.listdir(config.renpy_base + "/templates") if fnmatch.fnmatch(i.lower(), zipglob.lower()) ]

        if not filenames:
            interface.error(
                _("Could not install [name!t], as a file matching [zipglob] was not found in the Ren'Py SDK directory."),
                label="install",
                name=name,
                zipglob=zipglob,
            )

        filenames.sort(key=lambda a : a.lower())
        filename = filenames[-1]

        # The zipfile.
        zf = zipfile.ZipFile(os.path.join(config.renpy_base, "templates", filename))

        for fn in zf.namelist():
            matchfn = fn.replace("\\", "/")
            dstfn = None

            renpy.write_log(fn)

            for src, dst in patterns:
                if re.match(src, matchfn):
                    #print("SRC: " + str(src) + " | DST: " + str(dst) + " : " + str(re.sub(src, dst, matchfn)))
                    dstfn = re.sub(src, dst, matchfn)
                    break

            if not dstfn:
                continue
            
            if not tool:
                dstfn = os.path.join(config.renpy_base, dstfn)
            else:
                dstfn = os.path.join(persistent.projects_directory, project.current.name, dstfn)
                #print(dstfn)

            if not os.path.exists(os.path.dirname(dstfn)):
                try:
                    os.makedirs(os.path.dirname(dstfn))
                except:
                    pass

            renpy.write_log(fn + " -> " + dstfn)

            data = zf.read(fn)
            with open(dstfn, "wb") as f:
                f.write(data)

            try:
                os.chmod(dstfn, 0o755)
            except:
                pass

        
        interface.info(_("Successfully installed [name!t]."), name=name)


label install_live2d:
    python hide:

        patterns = [
            (r".*/Core/dll/linux/x86_64/(libLive2DCubismCore.so)", r"lib/linux-x86_64/\1"),
            (r".*/Core/dll/windows/x86_64/(Live2DCubismCore.dll)", r"lib/windows-x86_64/\1"),
            (r".*/Core/dll/windows/x86/(Live2DCubismCore.dll)", r"lib/windows-i686/\1"),
            (r".*/Core/dll/macos/(libLive2DCubismCore.dylib)", r"lib/mac-x86_64/\1"),
            (r".*/Core/dll/experimental/rpi/(libLive2DCubismCore.so)", r"lib/linux-armv7l/\1"),

            (r".*/Core/dll/android/(armeabi-v7a/libLive2DCubismCore.so)", r"rapt/prototype/renpyandroid/src/main/jniLibs/\1"),
            (r".*/Core/dll/android/(arm64-v8a/libLive2DCubismCore.so)", r"rapt/prototype/renpyandroid/src/main/jniLibs/\1"),

            # This doesn't exist yet.
            # (r".*/Core/dll/android/(x86_64/libLive2DCubismCore.so)", r"rapt/prototype/renpyandroid/src/main/jniLibs/\1"),
        ]

        install_from_zip("Live2D Cubism SDK for Native", "CubismSdkForNative-4-*.zip", patterns)

    jump front_page


label install_ostplayer:
    python hide:
        
        patterns = [
            (r"(.*.rpy)", r"game/\1"),     
            (r"(.*.png)", r"game/\1"),
            (r"(.*.txt)", r"game/\1"),
            (r"(.*.py)", r"game/\1"),
            (r"(.*.ttf)", r"game/\1"),     
            (r"(.*.otf)", r"game/\1"),
            (r"(.*.ogg)", r"game/\1"),
        ]

        install_from_zip("DDLC OST-Player", "DDLC-OSTPlayer-*.zip", patterns, True)
        try: os.makedirs(os.path.join(persistent.projects_directory, project.current.name, "game/track"))
        except: pass
        p = open(os.path.join(persistent.projects_directory, project.current.name, "game/track/Place Music Files Here"), "w")
        p.close()
        interface.info(_("DDLC OST-Player requires you to manually modify `screens.rpy` in order for it to work.\nRefer to `install.txt` file in your projects' game folder order to setup DDLC OST-Player."))
    
    jump front_page
    
label install_mpt:
    python hide:
        
        if glob.glob(config.renpy_base + '/templates/DDLC_MPT-*-unpacked.*'):
            mptzip = glob.glob(config.renpy_base + '/templates/DDLC_MPT-*')[0]
        elif glob.glob(config.renpy_base + '/templates/DDLC_MPT-*_unpacked.*'):
            mptzip = glob.glob(config.renpy_base + '/templates/DDLC_MPT-[0-9].*_unpacked.*')[0]
        elif glob.glob(config.renpy_base + '/templates/MPT v*'):
            mptzip = glob.glob(config.renpy_base + '/templates/MPT v*')[0]
        else:
            interface.error(_("Cannot find the MPT ZIP file.\nRename the ZIP to DDLC_MPT-ZIP or make sure the ZIP is in the 'templates' folder."))
            renpy.jump("install")
            
        patterns = [
            (r"(.*.rpy)", r"\1"),     
            (r"(.*.png)", r"\1"),
            (r"(.*.txt)", r"\1")
        ]

        install_from_zip("Mood Pose Tool (MPT)", mptzip.replace(config.renpy_base + '/', "").replace("\\", "/").replace("templates/", ""), patterns, True)

    jump front_page 

screen install():

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Install Tools")

            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    viewport:
                        scrollbars "vertical"
                        mousewheel True

                        has vbox

                        text _("This menu allows you to install libraries that can't be distributed with DDMM. Some of these libraries may require you to agree to a third-party license before being used or distributed.")

                        add HALF_SPACER

                        add SPACER

                        textbutton _("Install Live2D Cubism SDK for Native"):
                            action Jump("install_live2d")

                        add HALF_SPACER

                        frame:
                            style "l_indent"
                            has vbox

                            text _("The {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} adds support for displaying Live2D models. Place CubismSdkForNative-4-{i}version{/i}.zip in the templates folder, and then click Install Live2D Cubism for Native. Distributing a game with Live2D requires you to accept a license from Live2D, Inc.")

                            add SPACER

                            text _("Live2D in Ren'Py doesn't support the Web, Android x86_64 (including emulators and Chrome OS), and must be added to iOS projects manually. Live2D must be reinstalled after upgrading DDMM or installing Android support.")
                        
                        add HALF_SPACER
                        
                        textbutton _("Install DDLC OST-Player"):
                            action Jump("install_ostplayer")
                        
                        add HALF_SPACER

                        frame:
                            style "l_indent"
                            has vbox

                            text _("{a=https://github.com/GanstaKingofSA/DDLC-OSTPlayer/releases/latest}DDLC OST-Player{/a} is addon tool for DDLC that adds a music player to your mod for players to enjoy your mod's soundtrack along with their own music. Place DDLC-OSTPlayer-X.X.zip in the templates folder and then click Install DDLC OST-Player. Distributing a mod with DDLC OST-Player requires you to credit the author in your credits file/scene.")
                            
                        add HALF_SPACER
                        
                        textbutton _("Install Mood Pose Tool (MPT)"):
                            action Jump("install_mpt")
                        
                        add HALF_SPACER

                        frame:
                            style "l_indent"
                            has vbox

                            text _("Mood Pose Tool (MPT) is addon tool for DDLC that allows you to easily generate and use an expanded set of expressions for each base-game character. Place MPT's ZIP file in the templates folder and click Install Mood Pose Tool (MPT). Distributing a mod with MPT requires you to credit the authors in accordance to their requirements under 'Usage.txt'.")


    textbutton _("Cancel") action Return(False) style "l_left_button"
    textbutton _("Open Templates Directory") action OpenDirectory(config.renpy_base + "/templates", absolute=True) style "l_right_button"

    timer 2.0 action renpy.restart_interaction repeat True

label install:
    call screen install
    jump front_page
