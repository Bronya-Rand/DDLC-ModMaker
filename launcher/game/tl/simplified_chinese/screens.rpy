﻿
translate simplified_chinese strings:

    # screens.rpy:9
    old "## Styles"
    new "## 样式"

    # screens.rpy:81
    old "## In-game screens"
    new "## 游戏内界面"

    # screens.rpy:85
    old "## Say screen"
    new "## 对话界面"

    # screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## 对话界面用于向玩家显示对话。它需要两个参数，“who”和“what”，分别是叙述人的名称和所叙述的内容。（如果没有名称，参数“who”可以是“None”。）"

    # screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## 此界面必须创建一个 id 为“what”的文本可视控件，因为 Ren'Py 使用它来管理文本显示。它还可以创建 id 为“who”和 id 为“window”的可视控件来应用样式属性。"

    # screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.cn/doc/screen_special.html#say"

    # screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## 如果有对话框头像，会将其显示在文本之上。请不要在手机界面下显示这个，因为没有空间。"

    # screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## 通过 Character 对象使名称框可用于样式化。"

    # screens.rpy:164
    old "## Input screen"
    new "## 输入界面"

    # screens.rpy:166
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## 此界面用于显示 renpy.input。“prompt”参数用于传递文本提示。"

    # screens.rpy:169
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## 此界面必须创建一个 id 为“input”的输入可视控件来接受各种输入参数。"

    # screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.cn/doc/screen_special.html#input"

    # screens.rpy:199
    old "## Choice screen"
    new "## 选择界面"

    # screens.rpy:201
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## 此界面用于显示由“menu”语句生成的游戏内选项。参数“items”是一个对象列表，每个对象都有标题和操作字段。"

    # screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.cn/doc/screen_special.html#choice"

    # screens.rpy:215
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## 若为 True，菜单内的叙述会使用旁白角色。若为 False，叙述会显示为菜单内的文字说明。"

    # screens.rpy:238
    old "## Quick Menu screen"
    new "## 快捷菜单界面"

    # screens.rpy:240
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## 快捷菜单显示于游戏内，以便于访问游戏外的菜单。"

    # screens.rpy:245
    old "## Ensure this appears on top of other screens."
    new "## 确保该菜单出现在其他界面之上，"

    # screens.rpy:256
    old "Back"
    new "回退"

    # screens.rpy:257
    old "History"
    new "历史"

    # screens.rpy:258
    old "Skip"
    new "快进"

    # screens.rpy:259
    old "Auto"
    new "自动"

    # screens.rpy:260
    old "Save"
    new "保存"

    # screens.rpy:261
    old "Q.Save"
    new "快存"

    # screens.rpy:262
    old "Q.Load"
    new "快读"

    # screens.rpy:263
    old "Prefs"
    new "设置"

    # screens.rpy:266
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## 此语句确保只要玩家没有明确隐藏界面，就会在游戏中显示“quick_menu”界面。"

    # screens.rpy:284
    old "## Main and Game Menu Screens"
    new "## 标题和游戏菜单界面"

    # screens.rpy:287
    old "## Navigation screen"
    new "## 导航界面"

    # screens.rpy:289
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## 该界面包含在标题菜单和游戏菜单中，并提供导航到其他菜单，以及启动游戏。"

    # screens.rpy:304
    old "Start"
    new "开始游戏"

    # screens.rpy:312
    old "Load"
    new "读取游戏"

    # screens.rpy:314
    old "Preferences"
    new "设置"

    # screens.rpy:318
    old "End Replay"
    new "结束回放"

    # screens.rpy:322
    old "Main Menu"
    new "标题界面"

    # screens.rpy:324
    old "About"
    new "关于"

    # screens.rpy:328
    old "## Help isn't necessary or relevant to mobile devices."
    new "## “帮助”对移动设备来说并非必需或相关。"

    # screens.rpy:329
    old "Help"
    new "帮助"

    # screens.rpy:333
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## “退出”按钮在 iOS 上被禁止设置，在安卓和网页上也不是必需的。"

    # screens.rpy:334
    old "Quit"
    new "退出"

    # screens.rpy:348
    old "## Main Menu screen"
    new "## 标题菜单界面"

    # screens.rpy:350
    old "## Used to display the main menu when Ren'Py starts."
    new "## 用于在 Ren'Py 启动时显示标题菜单。"

    # screens.rpy:352
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.cn/doc/screen_special.html#main-menu"

    # screens.rpy:356
    old "## This ensures that any other menu screen is replaced."
    new "## 此语句可确保替换掉任何其他菜单界面。"

    # screens.rpy:363
    old "## This empty frame darkens the main menu."
    new "## 此空框可使标题菜单变暗。"

    # screens.rpy:367
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## “use”语句将其他的界面包含进此界面。标题界面的实际内容在导航界面中。"

    # screens.rpy:410
    old "## Game Menu screen"
    new "## 游戏菜单界面"

    # screens.rpy:412
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## 此界面列出了游戏菜单的基本共同结构。可使用界面标题调用，并显示背景、标题和导航菜单。"

    # screens.rpy:415
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". When this screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## “scroll”参数可以是“None”，也可以是“viewport”或“vpgrid”。当此界面与一个或多个子菜单同时使用时，这些子菜单将被转移（放置）在其中。"

    # screens.rpy:433
    old "## Reserve space for the navigation section."
    new "## 导航部分的预留空间。"

    # screens.rpy:475
    old "Return"
    new "返回"

    # screens.rpy:538
    old "## About screen"
    new "## 关于界面"

    # screens.rpy:540
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## 此界面提供有关游戏和 Ren'Py 的制作人员和版权信息。"

    # screens.rpy:543
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## 此界面没有什么特别之处，因此它也是如何制作自定义界面的一个例子。"

    # screens.rpy:550
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## 此“use”语句将包含“game_menu”界面到此处。子级“vbox”将包含在“game_menu”界面的“viewport”内。"

    # screens.rpy:560
    old "Version [config.version!t]\n"
    new "版本 [config.version!t]\n"

    # screens.rpy:562
    old "## gui.about is usually set in options.rpy."
    new "## “gui.about”通常在 options.rpy 中设置。"

    # screens.rpy:566
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "引擎：{a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only]\n\n[renpy.license!t]"

    # screens.rpy:569
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## 此变量在 options.rpy 中重新定义，来添加文本到关于界面。"

    # screens.rpy:581
    old "## Load and Save screens"
    new "## 读取和保存界面"

    # screens.rpy:583
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## 这些界面负责让玩家保存游戏并能够再次读取。由于它们几乎完全一样，因此它们都是以第三方界面“file_slots”来实现的。"

    # screens.rpy:587
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.cn/doc/screen_special.html#save https://www.renpy.cn/doc/screen_special.html#load"

    # screens.rpy:606
    old "Page {}"
    new "第 {} 页"

    # screens.rpy:606
    old "Automatic saves"
    new "自动存档"

    # screens.rpy:606
    old "Quick saves"
    new "快速存档"

    # screens.rpy:612
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## 此语句确保输入控件在任意按钮执行前可以获取“enter”事件。"

    # screens.rpy:616
    old "## The page name, which can be edited by clicking on a button."
    new "## 页面名称，可以通过单击按钮进行编辑。"

    # screens.rpy:628
    old "## The grid of file slots."
    new "## 存档位网格。"

    # screens.rpy:648
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%Y-%m-%d %H:%M"

    # screens.rpy:648
    old "empty slot"
    new "空存档位"

    # screens.rpy:656
    old "## Buttons to access other pages."
    new "## 用于访问其他页面的按钮。"

    # screens.rpy:665
    old "<"
    new "<"

    # screens.rpy:668
    old "{#auto_page}A"
    new "{#auto_page}A"

    # screens.rpy:671
    old "{#quick_page}Q"
    new "{#quick_page}Q"

    # screens.rpy:673
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## “range(1, 10)”给出 1 到 9 之间的数字。"

    # screens.rpy:677
    old ">"
    new ">"

    # screens.rpy:712
    old "## Preferences screen"
    new "## 设置界面"

    # screens.rpy:714
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## 设置界面允许玩家配置游戏以更好地适应自己的习惯。"

    # screens.rpy:717
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.cn/doc/screen_special.html#preferences"

    # screens.rpy:734
    old "Display"
    new "显示"

    # screens.rpy:735
    old "Window"
    new "窗口"

    # screens.rpy:736
    old "Fullscreen"
    new "全屏"

    # screens.rpy:740
    old "Rollback Side"
    new "回退操作区"

    # screens.rpy:741
    old "Disable"
    new "禁用"

    # screens.rpy:742
    old "Left"
    new "屏幕左侧"

    # screens.rpy:743
    old "Right"
    new "屏幕右侧"

    # screens.rpy:748
    old "Unseen Text"
    new "未读文本"

    # screens.rpy:749
    old "After Choices"
    new "选项后继续"

    # screens.rpy:750
    old "Transitions"
    new "忽略转场"

    # screens.rpy:752
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## 可以在此处添加类型为“radio_pref”或“check_pref”的其他“vbox”，以添加其他创建者定义的首选项设置。"

    # screens.rpy:763
    old "Text Speed"
    new "文字速度"

    # screens.rpy:767
    old "Auto-Forward Time"
    new "自动前进时间"

    # screens.rpy:774
    old "Music Volume"
    new "音乐音量"

    # screens.rpy:781
    old "Sound Volume"
    new "音效音量"

    # screens.rpy:787
    old "Test"
    new "测试"

    # screens.rpy:791
    old "Voice Volume"
    new "语音音量"

    # screens.rpy:802
    old "Mute All"
    new "全部静音"

    # screens.rpy:878
    old "## History screen"
    new "## 历史界面"

    # screens.rpy:880
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## 这是一个向玩家显示对话历史的界面。虽然此界面没有任何特殊之处，但它必须访问储存在“_history_list”中的对话历史记录。"

    # screens.rpy:884
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.cn/doc/history.html"

    # screens.rpy:890
    old "## Avoid predicting this screen, as it can be very large."
    new "## 避免预缓存此界面，因为它可能非常大。"

    # screens.rpy:901
    old "## This lays things out properly if history_height is None."
    new "## 此语句可确保如果“history_height”为“None”的话仍可正常显示条目。"

    # screens.rpy:911
    old "## Take the color of the who text from the Character, if set."
    new "## 若角色颜色已设置，则从“Character”对象中读取颜色到叙述人文本中。"

    # screens.rpy:920
    old "The dialogue history is empty."
    new "尚无对话历史记录。"

    # screens.rpy:923
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## 此语句决定了允许在历史记录界面上显示哪些标签。"

    # screens.rpy:970
    old "## Help screen"
    new "## 帮助界面"

    # screens.rpy:972
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## 提供有关键盘和鼠标映射信息的界面。它使用其它界面（“keyboard_help”，“mouse_help“和”gamepad_help“）来显示实际的帮助内容。"

    # screens.rpy:991
    old "Keyboard"
    new "键盘"

    # screens.rpy:992
    old "Mouse"
    new "鼠标"

    # screens.rpy:995
    old "Gamepad"
    new "手柄"

    # screens.rpy:1008
    old "Enter"
    new "回车"

    # screens.rpy:1009
    old "Advances dialogue and activates the interface."
    new "推进对话并激活界面。"

    # screens.rpy:1012
    old "Space"
    new "空格"

    # screens.rpy:1013
    old "Advances dialogue without selecting choices."
    new "推进对话但不激活选项。"

    # screens.rpy:1016
    old "Arrow Keys"
    new "方向键"

    # screens.rpy:1017
    old "Navigate the interface."
    new "导航界面。"

    # screens.rpy:1020
    old "Escape"
    new "Esc"

    # screens.rpy:1021
    old "Accesses the game menu."
    new "访问游戏菜单。"

    # screens.rpy:1024
    old "Ctrl"
    new "Ctrl"

    # screens.rpy:1025
    old "Skips dialogue while held down."
    new "按住时快进对话。"

    # screens.rpy:1028
    old "Tab"
    new "Tab"

    # screens.rpy:1029
    old "Toggles dialogue skipping."
    new "切换对话快进。"

    # screens.rpy:1032
    old "Page Up"
    new "Page Up"

    # screens.rpy:1033
    old "Rolls back to earlier dialogue."
    new "回退至先前的对话。"

    # screens.rpy:1036
    old "Page Down"
    new "Page Down"

    # screens.rpy:1037
    old "Rolls forward to later dialogue."
    new "向前至之后的对话。"

    # screens.rpy:1041
    old "Hides the user interface."
    new "隐藏用户界面。"

    # screens.rpy:1045
    old "Takes a screenshot."
    new "截图。"

    # screens.rpy:1049
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "切换辅助{a=https://www.renpy.org/l/voicing}自动朗读{/a}。"

    # screens.rpy:1055
    old "Left Click"
    new "左键点击"

    # screens.rpy:1059
    old "Middle Click"
    new "中键点击"

    # screens.rpy:1063
    old "Right Click"
    new "右键点击"

    # screens.rpy:1067
    old "Mouse Wheel Up\nClick Rollback Side"
    new "鼠标滚轮上\n点击回退操作区"

    # screens.rpy:1071
    old "Mouse Wheel Down"
    new "鼠标滚轮下"

    # screens.rpy:1078
    old "Right Trigger\nA/Bottom Button"
    new "右扳机键\nA/底键"

    # screens.rpy:1082
    old "Left Trigger\nLeft Shoulder"
    new "左扳机键\n左肩键"

    # screens.rpy:1086
    old "Right Shoulder"
    new "右肩键"

    # screens.rpy:1091
    old "D-Pad, Sticks"
    new "十字键，摇杆"

    # screens.rpy:1095
    old "Start, Guide"
    new "开始，向导"

    # screens.rpy:1099
    old "Y/Top Button"
    new "Y/顶键"

    # screens.rpy:1102
    old "Calibrate"
    new "校准"

    # screens.rpy:1130
    old "## Additional screens"
    new "## 其他界面"

    # screens.rpy:1134
    old "## Confirm screen"
    new "## 确认界面"

    # screens.rpy:1136
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## 当 Ren'Py 需要询问玩家有关确定或取消的问题时，会调用确认界面。"

    # screens.rpy:1139
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.cn/doc/screen_special.html#confirm"

    # screens.rpy:1143
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## 显示此界面时，确保其他界面无法输入。"

    # screens.rpy:1167
    old "Yes"
    new "确定"

    # screens.rpy:1168
    old "No"
    new "取消"

    # screens.rpy:1170
    old "## Right-click and escape answer \"no\"."
    new "## 右键点击退出并答复“no”（取消）。"

    # screens.rpy:1197
    old "## Skip indicator screen"
    new "## 快进指示界面"

    # screens.rpy:1199
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## “skip_indicator”界面用于指示快进正在进行中。"

    # screens.rpy:1202
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.cn/doc/screen_special.html#skip-indicator"

    # screens.rpy:1214
    old "Skipping"
    new "正在快进"

    # screens.rpy:1221
    old "## This transform is used to blink the arrows one after another."
    new "## 此变换用于一个接一个地闪烁箭头。"

    # screens.rpy:1248
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## 我们必须使用包含“BLACK RIGHT-POINTING SMALL TRIANGLE”字形的字体。"

    # screens.rpy:1253
    old "## Notify screen"
    new "## 通知界面"

    # screens.rpy:1255
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## 通知界面用于向玩家显示消息。（例如，当游戏快速保存或已截屏时。）"

    # screens.rpy:1258
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.cn/doc/screen_special.html#notify-screen"

    # screens.rpy:1292
    old "## NVL screen"
    new "## NVL 模式界面"

    # screens.rpy:1294
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## 此界面用于 NVL 模式的对话和菜单。"

    # screens.rpy:1296
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.cn/doc/screen_special.html#nvl"

    # screens.rpy:1307
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## 在“vpgrid”或“vbox”中显示对话框。"

    # screens.rpy:1320
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new "## 如果给定，则显示“menu”。 如果“config.narrator_menu”设置为“True”，则“menu”可能显示不正确，如前述。"

    # screens.rpy:1350
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## 此语句控制一次可以显示的 NVL 模式条目的最大数量。"

    # screens.rpy:1412
    old "## Mobile Variants"
    new "## 移动设备界面"

    # screens.rpy:1419
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## 由于鼠标可能不存在，我们将快捷菜单替换为更容易触摸且按钮更少更大的版本。"

    # screens.rpy:1437
    old "Menu"
    new "菜单"
