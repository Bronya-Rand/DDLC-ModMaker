
init python:
    def mpt_extract():
        import zipfile
        try:
            with zipfile.ZipFile(config.basedir + "/templates/NAME OF THE ARCHIVE.FILE EXTENSION", "r") as z:
                z.extractall(persistent.project_dir + '/game/mod_assets')
        except:
            interface.error(_("Mood Pose Tool ZIP file missing, or corrupt."), _("Check if the ZIP exists or re-download the ZIP."))

screen advanced:

    frame:
        style_group "l"
        style "l_root"
        alt "Advanced Mode"

        window:

            has vbox

            label _("Advanced Mode")

            hbox:
                frame:
                    style "l_indent"
                    xmaximum ONETHIRD
                    xfill True

                    has vbox

                    frame:
                        style "l_indent"
                        yminimum 75
                        has vbox
                        textbutton _("Install 'Mood Pose Tool (MPT) [BETA]'") action Jump("mpt") alt _("Install 'Mood Pose Tool (MPT) [BETA]'")

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label advanced:
    call screen advanced
    jump advanced

label mpt:
    python:
        interface.info(_("Mood Pose Tool (MPT) is currently in development."), ("This feature will become available when the developer releases it."),)
    jump advanced