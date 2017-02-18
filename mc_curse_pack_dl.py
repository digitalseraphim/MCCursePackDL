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
		
		for f in manifest["files"]:
			r = requests.get("http://minecraft.curseforge.com/projects/" + str(f["projectID"]))
			r2 = requests.get(os.path.join(r.url, "files", str(f["fileID"]), "download"))
			u = urlparse(r2.url)
			fname = os.path.basename(u.path)
			with open(fname, "w") as ff:
				ff.write(r2.content)



if __name__ == "__main__":
	process_zip(sys.argv[1])		
