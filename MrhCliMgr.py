import os
import requests
import platform
from pathlib import Path
import urllib.request
import sys
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
modstofetch = Path(f"{path}/mods.txt")
mods = []

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
        filename = os.path.basename(url)
        filepath = os.path.join(moddir, filename)
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded {filename} ✅")
    print("Downgrade/Upgrade done sucessfully 😄😄😄😄😄😄😄")
def fetchmods(ver=None,load=None,path=None):
    defau = versions["result"][0]
    if not ver:
        while True:
            version = input(f"Minecraft version (default {defau}): ").strip()
            if not version:
                version = defau
                break
            if version in versions["result"]: break
            print("❌ Invalid version, try again.")
    else: 
        version = ver
        if version not in versions["result"]:
            print("❌ Invalid version.")
            return
    if not load:
        loader = input("minecraft loader (default fabric): ")
        if not loader: loader = "fabric"
    else: loader = load
    if not path:
        defidir = ""
        match platform.system():
            case "Linux": # any linux distribution
                defdir = f"{os.path.expanduser('~/.minecraft/mods')}"
            case "Windows": # windows
                defdir = f"{os.getenv('APPDATA')}/.minecraft/mods"
            case "Darwin": # macOS
                defdir = f"{os.path.expanduser('~/Library/Application Support/minecraft/mods')}"
            case _:
                defdir = "couldn't recognise the OS you are running, please enter it manually."
                print("gng what fucking os are u running 😭😭😭")
        moddir = input(f"minecraft mods directory (default {defdir}): ")
        if not moddir: moddir = defdir
    else:
        if platform.system() != "Windows":
            moddir = os.path.expanduser(path)
        else:
            moddir = path
    if not modstofetch.exists():
        with open(modstofetch, "a") as f:
            f.write("## Put project-id(s) in here\n")
            print("mods.txt was not found, place the modrinth project-id(s) of the mods you want the script to take care of: https://modrinth.com/mod/project-id")
            f.close()
            
    with open(modstofetch) as f:
        for line in f.read().splitlines():
            if line.startswith("##"): continue
            uri = getmod(line,version,loader)
            if uri == 0: 
                print(f"💔 mod {line} was not found for version {version} 💔") 
                continue
            elif uri == 1:
                print(f"💔 mod {line} doesn't exist, make sure you typed/copied it correctly 💔") 
                continue
            mods.append(uri)
        f.close()
    print("Replacing...")
    replacemods(moddir)
# -H
def helpusage():
    print(r"""        -S , --search : search for a mod on modrinth (args: search, limit(15 default) ).
        -U , --update : updates the script .
        -I , --install : deletes all mods from the mods folder and installs the latest mods from mods.txt for the version given ( args: version, loader, path ) .
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