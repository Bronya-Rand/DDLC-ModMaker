## Doki Doki Mod Maker (DDMMaker)

Doki Doki Mod Maker is a mod maker for the visual novel "Doki Doki Literature Club" that allows modders to make their mods easier and simpler with a re-written Ren'Py Source Distribution Kit (SDK).
> This project is unafilliated with either Team Salvato or RenpyTom. See the [disclaimer](../information/disclaimer/disclaimer.md) page for more information.

## Features
- Support for Ren'Py 7.4.4 Mod Making
- Automatic DDLC Mod Template Installation
- Automatic Mood Pose Tool (MPT) Installation
  > MPT is a tool made by `chronoshag` and is unaffiliated with DDMMaker or it's development. DDMMaker itself does not provide any MPT files and requires that you download it from it's source before using the Auto-MPT Installation feature.
- Atom Support for Ren'Py 6.99.12.4.
- Dark Mode based off One UI from "True Reality".
- SHA256 Checking for DDLC ZIP files and folders to verify authenticity.
- Android Build Support Compliant with Team Salvato's Guidelines
- Java Heap Size Adjustment

## Screenshots

![DDMMaker Screenshot 1](../assets/ddmmaker/screenshot0003E.png)
![DDMMaker Screenshot 2](../assets/ddmmaker/screenshot0002E.png)
![DDMMaker Screenshot 3](../assets/ddmmaker/screenshot0004E.png)
![DDMMaker Screenshot 4](../assets/ddmmaker/screenshot0001E.png)

## Changes

Version 1.2.6 - The Better "Pot of Gold" **(Current)**
- Updated SDK to 7.4.4
- Add Head Size Adjustment to fix `java.lang.OutOfMemory` errors when building mods greater than 500 MB (DDMMaker 7)
  > Heap Size Adjustment is only needed on DDMMaker 7 due to Gradle. Apache Ant on DDMMaker 6 seems to be running bigger APK sized mods just fine. If you get any error with Apache Ant, please forward it to the [issue](https://github.com/GanstaKingofSA/DDLC-ModMaker/issues) tracker to address it.
- Updated Atom Link (DDMMaker 6)
- Minor bug fixes

Version 1.2.5 **(Last Version)**
- Updated SDK to 7.4.3
- Fixed a bug that prevent users to select ddlc-win/ddlc-mac.zip files when making a project. (All DDMMaker Versions except depreciated ones).

For other version changes, refer to the [release](https://github.com/GanstaKingofSA/DDLC-ModMaker/releases) section of the DDMMaker Github repository.
