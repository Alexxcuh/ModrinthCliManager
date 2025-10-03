import os
import requests
import platform
import urllib.request
import sys
import yaml
import io
settings = {
    "version": None,
    "loader": "fabric",
    "path": None,
    "mods": [
        "Put your mods in here"
    ]
}
versions = requests.get("https://mc-versions-api.net/api/java").json()
print(r"""
░███     ░███                   ░██          ░██              ░██    ░██          ░██████  ░██ ░██░███     ░███                                                                 
░████   ░████                   ░██                           ░██    ░██         ░██   ░██ ░██    ░████   ░████                                                                 
░██░██ ░██░██  ░███████   ░████████ ░██░████ ░██░████████  ░████████ ░████████  ░██        ░██ ░██░██░██ ░██░██  ░██████   ░████████   ░██████    ░████████  ░███████  ░██░████ 
░██ ░████ ░██ ░██    ░██ ░██    ░██ ░███     ░██░██    ░██    ░██    ░██    ░██ ░██        ░██ ░██░██ ░████ ░██       ░██  ░██    ░██       ░██  ░██    ░██ ░██    ░██ ░███     
░██  ░██  ░██ ░██    ░██ ░██    ░██ ░██      ░██░██    ░██    ░██    ░██    ░██ ░██        ░██ ░██░██  ░██  ░██  ░███████  ░██    ░██  ░███████  ░██    ░██ ░█████████ ░██      
░██       ░██ ░██    ░██ ░██   ░███ ░██      ░██░██    ░██    ░██    ░██    ░██  ░██   ░██ ░██ ░██░██       ░██ ░██   ░██  ░██    ░██ ░██   ░██  ░██   ░███ ░██        ░██      
░██       ░██  ░███████   ░█████░██ ░██      ░██░██    ░██     ░████ ░██    ░██   ░██████  ░██ ░██░██       ░██  ░█████░██ ░██    ░██  ░█████░██  ░█████░██  ░███████  ░██      
                                                                                                                                                        ░██                     
                                                                                                                                                ░███████                      
By AlexXD_ (Alexxcuh)
""")
path = os.path.realpath(os.getcwd())
modstofetch = []
mods = []
moddir = None
version = None
loader = None
def initializesettings():
    global moddir,version,loader,settings,modstofetch
    if os.path.exists(f"{path}/settings.yaml"):
        with open(f"{path}/settings.yaml", 'r') as stream:
            settings = {}
            settings = yaml.safe_load(stream)
    else:
        print(settings)
        settings["version"] = versions["result"][0]
        settings["loader"] = "fabric"
        match platform.system():
            case "Linux":
                settings["path"] = f"{os.path.expanduser('~/.minecraft/mods')}"
            case "Windows":
                settings["path"] = f"{os.getenv('APPDATA')}/.minecraft/mods"
            case "Darwin":
                settings["path"] = f"{os.path.expanduser('~/Library/Application Support/minecraft/mods')}"
        with io.open(f"{path}/settings.yaml", 'w', encoding='utf8') as outfile:
            yaml.dump(settings, outfile, default_flow_style=False, allow_unicode=True)
        print("settings.yaml file was created, enter the version, loader, mod directory path and mods the script will use")
        return False
    if platform.system() != "Windows":
        moddir = os.path.expanduser(settings.get("path"))
    else:
        moddir = settings["path"]
    version = settings["version"]
    loader = settings["loader"]
    modstofetch = settings["mods"]
    return True
    
# -U // --update
def getmod(name,version,loader):
    response = requests.get(f"https://api.modrinth.com/v2/project/{name}/version")
    if response.status_code == 404: return 1

    versions = response.json()
    for v in versions:
        if version in v["game_versions"] and loader in v["loaders"]:
            print(f"Got download URL for {v["name"]} ({name}) ✅")
            return v["files"][0]["url"]
    return 0
def replacemods(moddir):
    for mod in os.listdir(moddir):
        if not mod.endswith(".jar"): continue
        os.remove(f"{moddir}/{mod}")
    print("Deleted previous mods")
    for url in mods:
        filename = os.path.basename(url).replace("%2B","+")
        filepath = os.path.join(moddir, filename)
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded {filename} ✅")
    print("Downgrade/Upgrade done sucessfully 😄😄😄😄😄😄😄")
def fetchmods(ver=None,load=None,path=None):
    if version not in versions["result"]:
        print("the version given in the yaml file is invalid ❌")
        return
    for line in modstofetch:
        if line.startswith("##"): continue
        uri = getmod(line,version,loader)
        if uri == 0: 
            print(f"💔 mod {line} was not found for version {version} 💔") 
            continue
        elif uri == 1:
            print(f"💔 mod {line} doesn't exist, make sure you typed/copied it correctly 💔") 
            continue
        mods.append(uri)
    print("Replacing...")
    replacemods(moddir)
# -H
def helpusage():
    print(r"""        -S , --search : search for a mod on modrinth ( args: query, limit(15 default) ).
        -U , --update : updates the script .
        -I , --install : deletes all mods from the mods folder and installs the latest mods from the mods listed in settings.yaml for the version given ( args: version, loader, path ) .
        -H , --help : shows the help screen ( the screen you're currently on ) .
    """)
    return
# -U
def updatescript():
    print("Updating script...")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/Alexxcuh/ModrinthCliManager/refs/heads/master/MrhCliMgr.py", __file__)
    print("Script updated! 😄")
    return
# -S
def searchmod(search, limit=15):
    if not search:
        print("Gang.. enter a mod to search for 😭")
        return
    query = requests.get(f"https://api.modrinth.com/v2/search?query={search}&limit={limit}").json()
    for modinfo in query["hits"]:
        print(f"""            Title: {modinfo["title"]}
            Project-ID: {modinfo["slug"]}
            Author: {modinfo["author"]}
            Description: "{modinfo["description"]}"
            {modinfo["downloads"]} Downloads | {modinfo["follows"]} Follows
            """)
def main():
    if not initializesettings(): return
    match sys.argv[1:]:
        case ["-S", search, *rest] | ["--search", search, *rest]:
            limit = rest[0] if len(rest) > 0 else 15
            searchmod(search, limit)
        case ["-U", *rest] | ["--update", *rest]:
            updatescript()
        case ["-I", *rest] | ["--install", *rest]:
            ver = rest[0] if len(rest) > 0 else None
            load = rest[1] if len(rest) > 1 else None
            path = rest[2] if len(rest) > 2 else None
            fetchmods(ver, load, path)
        case ["-H", *rest] | ["--help", *rest]:
            helpusage()
        case []:
            helpusage()
    return

if __name__ == "__main__":
    main()