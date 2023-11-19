
init python:
    import sys
    import glob
    from zipfile import ZipFile
    import tempfile

screen mmtoolinstaller():

    default tools = {}
    default have_third_party = False

    frame:
        style_group "l"
        style "l_root"

        window:

            has viewport:
                scrollbars "vertical"
                mousewheel True

            has vbox

            label _("DDMM Tool Installer")
                
            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    has vbox

                    text _("Installing to: {}".format(project.current.name)) size 15

                    add SPACER

                    python:
                        with open(config.basedir + '/update/first_party.json') as fp:
                            first_party_json = json.load(fp)

                        if os.path.exists(config.basedir + '/update/third_party.json'):
                            with open(config.basedir + '/update/third_party.json') as tp:
                                third_party_json = json.load(tp)

                        for i, cls in mmupdate.all_modules.items():
                            module_name = eval(cls)
                            acronym = module_name.ModTool().acronym
                            if module_name.ModTool().tool:
                                tools[acronym] = {}
                                tools[acronym]['cls'] = module_name.ModTool()

                                try:
                                    first_party_json[acronym]
                                    tools[acronym]['third_party'] = False
                                except KeyError:
                                    have_third_party = True
                                    tools[acronym]['third_party'] = True

                    text "First Party" size 18

                    add SPACER

                    for acc, tool in tools.items():
                        if not tool['third_party']:

                            textbutton tool['cls'].name action Call("install_script", tool['cls'], project.current.path)
                            text "Creator: {}".format(tool['cls'].creator) size 14
                            text "Identifier: {} | Downloaded: {}".format(acc, "Yes" if tool['cls'].check_if_installed() else "No") size 14
                            text "\n" + tool['cls'].desc size 14

                            add SPACER

                    add SEPARATOR
                    add SPACER

                    text "Third Party" size 18

                    add SPACER

                    if have_third_party:
                        for acc, tool in tools.items():
                            if tool['third_party']:

                                textbutton tool['cls'].name action Call("install_script", tool['cls'], project.current.path)
                                text "Creator: {}".format(tool['cls'].creator) size 14
                                text "Identifier: {} | Downloaded: {}".format(acc, "Yes" if tool['cls'].check_if_installed else "No") size 14
                                text "\n" + tool['cls'].desc size 14

                                add SPACER
                    else:

                        text "No third-party tools available."

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label install_script(pkg, directory):
    python:
        with interface.error_handling(_("Installing " + pkg.name)):
            interface.processing(_("Installing " + pkg.name + ". Please wait..."))
            pkg.install(directory)

        interface.info(_(pkg.name + " has been successfully installed onto your mod."))
        renpy.jump("mmtoolinstaller")

label mmtoolinstaller:
    call screen mmtoolinstaller
    jump front_page