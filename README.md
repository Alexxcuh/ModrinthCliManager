# Modrinth Cli Mod Manager
## !!! NOTICE !!!
**Upon usage the script will delete all .jar files in the mods directory and then replace them with the mods in the settings.yaml file, it's not recursive, thus you can put a mod you dont want it to delete in a subfolder in the mods folder.**

Also, don't confuse the mod name with the project id, they are 2 separate things, for example, ``https://modrinth.com/mod/gamma-utils``, the mod name is ``Gamma Utils (Fullbright)``, and the project id is ``gamma-utils``, don't confuse one another or the script won't work correctly.  
## Usage
you put into the mods.txt file the project ids of the modrinth mods, you can find them in the link of the site, eg: ``https://modrinth.com/mod/lithium/``, the project id would be ``lithium``

**the mods.txt file must be in the same directory as the script or it wont work.**
## -I , --install
``version``: the default minecraft version the script will go to is the latest minecraft version there is. (optional)

``loader``: the default loader choosen by the script is fabric. (optional)

``mod directory``: the default mod directory it chooses is the default mod dir of your operating system, if you're not using **Linux**, **Windows** or **MacOS** you'll have to input the mod directory manually. (optional)

**Note**: the default paramaters for --install can be changed in settings.yaml
```yaml
loader: fabric
mods:
- Put your mods in here
path: /home/user/.minecraft/mods
version: 1.21.8
```
## -H , --help
shows the help screen where you can see this in a short form.
## -U , --update
updates the script to the latest version of the script there is.
## -S , --search
``query``: the mod you want to search on modrinth, this is a required paramater.

``limit``: how many mods it can show at once, the default chosen is 15. (optional)
## Keep in mind
**All of the paramaters listed can be changed at startup when the script will ask for the values of the paramaters. *(of course if it isn't given the values it will go for the default ones listed previously)***                                                                                