
init python:
    import mmupdater
    mmupdate = mmupdater.MMakerUpdater()

    import os
    import json

label mmupdater:
    python:
        if not os.path.exists(config.basedir + "/update"):
            os.makedirs(config.basedir + "/update")

    call screen new_ddmmupdate

    jump front_page

screen new_ddmmupdate():

    default updates = {}
    default no_updates = {}
    default first_party_json = None
    default third_party_json = None

    frame:
        style_group "l"
        style "l_root"

        window:

            has viewport:
                scrollbars "vertical"
                mousewheel True

            has vbox

            label _("DDMM Updater")

            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    has vbox

                    python:
                        with open(config.basedir + '/update/first_party.json') as fp:
                            first_party_json = json.load(fp)

                        if os.path.exists(config.basedir + '/update/third_party.json'):
                            with open(config.basedir + '/update/third_party.json') as tp:
                                third_party_json = json.load(tp)

                        for i, cls in mmupdate.all_modules.items():
                            module_name = eval(cls)
                            acronym = module_name.ModTool().acronym
                            if module_name.ModTool().check_for_updates():
                                updates[acronym] = {}
                                updates[acronym]['cls'] = module_name.ModTool()

                                try:
                                    first_party_json[acronym]
                                    updates[acronym]['third_party'] = False
                                except KeyError:
                                    updates[acronym]['third_party'] = True
                            else:
                                no_updates[acronym] = {}
                                no_updates[acronym]['cls'] = module_name.ModTool()

                                try:
                                    first_party_json[acronym]
                                    no_updates[acronym]['third_party'] = False
                                except KeyError:
                                    no_updates[acronym]['third_party'] = True

                    text "Pending Updates" size 18

                    add SPACER

                    if updates:
                        for acc, tool in updates.items():
                            python:
                                third_party = False
                                if tool['third_party']:
                                    tool_ver = third_party_json[acc]['version']
                                    third_party = True
                                else:
                                    tool_ver = first_party_json[acc]['version']

                            textbutton tool['cls'].name action Call("update_script", tool['cls'], tool['third_party'])
                            text "Creator: {}".format(tool['cls'].creator) size 14
                            text "Type: {} | Identifier: {} | Version {} -> {}".format("{b}Third Party{/b}" if tool['third_party'] else "{b}First Party{/b}", acc, tool_ver, tool['cls'].get_remote_tool_version()) size 14
                            text "\n" + tool['cls'].desc size 14

                            add SPACER

                    else:
                        
                        text "No updates available."

                        add SPACER

                    add SEPARATOR
                    add SPACER

                    text "Current Updates" size 18

                    add SPACER

                    for acc, tool in no_updates.items():
                        python:
                            if tool['third_party']:
                                tool_ver = third_party_json[acc]['version']
                            else:
                                tool_ver = first_party_json[acc]['version']

                        textbutton tool['cls'].name action NullAction()
                        text "Creator: {}".format(tool['cls'].creator) size 14
                        text "Type: {} | Identifier: {} | Version {}".format("{b}Third Party{/b}" if tool['third_party'] else "{b}First Party{/b}", acc, tool_ver) size 14
                        text "\n" + tool['cls'].desc size 14

                        add SPACER

    textbutton _("Return") action Jump("front_page") style "l_left_button"

label update_script(pkg, third_party):
    python:
        with interface.error_handling(_("Updating " + pkg.name)):
            interface.processing(_("Updating " + pkg.name + ". Please wait..."))
            pkg.update()

        if third_party:
            with open(config.basedir + '/update/third_party.json') as tp:
                json_data = json.load(tp)
            
            json_data[pkg.acronym]['version'] = pkg.get_remote_tool_version()
            
            with open(config.basedir + '/update/third_party.json', "w") as tp:
                json.dump(json_data, tp)
        else:
            with open(config.basedir + '/update/first_party.json') as tp:
                json_data = json.load(tp)
            
            json_data[pkg.acronym]['version'] = pkg.get_remote_tool_version()
            
            with open(config.basedir + '/update/first_party.json', "w") as tp:
                json.dump(json_data, tp)
        
        if not pkg.restart:
            interface.info(_(pkg.name + " has been successfully updated to the latest version."))
            renpy.jump("mmupdater")
        else:
            interface.info(_(pkg.name + " has been successfully updated to the latest version.\nYou must restart DDMM for to apply the update."))
            renpy.quit(True)
