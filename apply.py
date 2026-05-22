#!/usr/bin/env python3
import json, urllib.request, subprocess

APPS_URL = "https://script.google.com/macros/s/AKfycbyZkdn7n9ZYNCR0UXpgRMt5oaS9dAJUvh66FWwHw0HYH5M4hS61penR1rnbQ4C-x6wN/exec"

with open("commands/pending.json","r",encoding="utf-8") as f:
    cmd = json.load(f)

if "action" not in cmd:
    print("No action, skipping")
    exit(0)

print(f"Running: {cmd.get('action')} on {cmd.get('projectId','?')}")

# Handle POST redirects properly
class PostRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        data = req.data
        new_req = urllib.request.Request(newurl, data=data, method="POST")
        new_req.add_header("Content-Type", "text/plain")
        return new_req

data = json.dumps(cmd, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(APPS_URL, data=data, method="POST")
req.add_header("Content-Type", "text/plain")

opener = urllib.request.build_opener(PostRedirectHandler)
try:
    resp = opener.open(req)
    result = resp.read().decode("utf-8")
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")

with open("commands/pending.json","w",encoding="utf-8") as f:
    json.dump({"status":"done"},f)

subprocess.run(["git","config","user.name","מאיה"])
subprocess.run(["git","config","user.email","maya@nagaria.app"])
subprocess.run(["git","add","commands/pending.json"])
subprocess.run(["git","commit","-m","clear [skip ci]"])
subprocess.run(["git","push"])
print("Done!")
