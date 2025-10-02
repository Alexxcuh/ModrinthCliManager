import os
import requests
import platform
from pathlib import Path
import urllib.request
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
By Alexx
""")
defau = versions["result"][0]
while True:
    version = input(f"Minecraft version (default {defau}): ").strip()
    if not version:
        version = defau
        break
    if version in versions["result"]: break
    print("❌ Invalid version, try again.")
loader = input("minecraft loader (default fabric): ")
if not loader: loader = "fabric"
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

path = os.path.realpath(os.getcwd())
modstofetch = Path(f"{path}/mods.txt")
mods = []

def getmod(name):
    response = requests.get(f"https://api.modrinth.com/v2/project/{name}/version")
    if response.status_code == 404: return 1

    versions = response.json()
    for v in versions:
        if version in v["game_versions"] and loader in v["loaders"]:
            print(f"Got download URL for {v["name"]} ({name}) ✅")
            return v["files"][0]["url"]
    return 0
def replacemods():
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
def fetchmods():

    if not modstofetch.exists():
        with open(modstofetch, "a") as f:
            f.write("## Put project-id(s) in here\n")
            print("mods.txt was not found, place the modrinth project-id(s) of the mods you want the script to take care of: https://modrinth.com/mod/project-id")
            f.close()
            
    with open(modstofetch) as f:
        for line in f.read().splitlines():
            if line.startswith("##"): continue
            uri = getmod(line)
            if uri == 0: 
                print(f"💔 mod {line} was not found for version {version} 💔") 
                continue
            elif uri == 1:
                print(f"💔 mod {line} doesn't exist, make sure you typed/copied it correctly 💔") 
                continue
            mods.append(uri)
        f.close()
    print("Replacing...")
    replacemods()
def main():
    fetchmods()

if __name__ == "__main__":
    main()