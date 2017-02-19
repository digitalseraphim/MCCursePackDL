import requests
import zipfile
import json
from urlparse import urlparse
import os
import sys


def process_zip(z):
	with zipfile.ZipFile(z) as zf:
		manifest_f = zf.open("manifest.json")
		manifest = json.loads(manifest_f.read())

		mc_version = manifest["minecraft"]["version"]
		forge_version = manifest["minecraft"]["modLoaders"][0]["id"]
		vers_str = mc_version + "-" + forge_version[6:]
		pack_name = manifest["name"]

		requests.get("http://files.minecraftforge.net/maven/net/minecraftforge/forge/" + vers_str + "/forge-" + vers_str1 + "-universal.jar")
		
		profiles = None
		with open("~/.minecraft/launcher_profiles.json") as f:
			profiles = json.loads(f.read())
		

		if pack_name in profiles["profiles"]:
			print "there's already a profile for this pack"

		profiles["profiles"][pack_name] = {"name":pack_name,"lastVersionId":mc_version}

		os.mkdir("~/.minecraft/versions/" + pack_name)

		os.mkdir("~/.minecraft/versions/" + pack_name + "/mods")
		
		for f in manifest["files"]:
			r = requests.get("http://minecraft.curseforge.com/projects/" + str(f["projectID"]))
			r2 = requests.get(os.path.join(r.url, "files", str(f["fileID"]), "download"))
			u = urlparse(r2.url)
			fname = "~/.minecrat/versions/" + pack_name + "/mods/" + os.path.basename(u.path)
			with open(fname, "w") as ff:
				ff.write(r2.content)



if __name__ == "__main__":
	process_zip(sys.argv[1])		
