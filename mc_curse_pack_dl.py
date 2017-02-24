import requests
import zipfile
import json
from urlparse import urlparse
import os
import sys
import xextract


def getDepends(url):
    r = requests.get(os.path.join(url, "relations/dependencies"))
    eles = xextract.Element(xpath='//*[contains(@class,"project-listing")]//*[contains(@class, "name-wrapper")]/a').parse(r.text)
    #print [repr(x.items()) for x in eles]

    print repr([(x.itertext().next(),x.get("href")) for x in eles])



def process_zip(z):
	with zipfile.ZipFile(z) as zf:
		manifest_f = zf.open("manifest.json")
		manifest = json.loads(manifest_f.read())

		mc_version = manifest["minecraft"]["version"]
		forge_version = manifest["minecraft"]["modLoaders"][0]["id"]
		vers_str = mc_version + "-" + forge_version[6:]
		pack_name = manifest["name"]

		requests.get("http://files.minecraftforge.net/maven/net/minecraftforge/forge/" + vers_str + "/forge-" + vers_str + "-universal.jar")
		
		profiles = None
		
		for f in manifest["files"]:
			r = requests.get("http://minecraft.curseforge.com/projects/" + str(f["projectID"]))
                        print r.url
                        getDepends(r.url)
			#r2 = requests.get(os.path.join(r.url, "files", str(f["fileID"]), "download"))
			#u = urlparse(r2.url)
			#fname = "~/.minecrat/versions/" + pack_name + "/mods/" + os.path.basename(u.path)
			#with open(fname, "w") as ff:
			#	ff.write(r2.content)



if __name__ == "__main__":
	process_zip(sys.argv[1])		
