#!/usr/bin/env python3
import json, urllib.request, subprocess

APPS_URL = "https://script.google.com/macros/s/AKfycbyZkdn7n9ZYNCR0UXpgRMt5oaS9dAJUvh66FWwHw0HYH5M4hS61penR1rnbQ4C-x6wN/exec"

with open("commands/pending.json","r",encoding="utf-8") as f:
    cmd = json.load(f)

if "action" not in cmd:
    print("No action, skipping")
    exit(0)

print(f"Running: {cmd.get('action')} on {cmd.get('projectId','?')}")

data = json.dumps(cmd).encode("utf-8")
req = urllib.request.Request(APPS_URL, data=data,
    headers={"Content-Type":"text/plain"})
req.get_method = lambda: "POST"

try:
    import urllib.request as ur
    # Follow redirects manually
    resp = ur.urlopen(req)
    result = resp.read().decode("utf-8")
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")

# Reset commands file
with open("commands/pending.json","w",encoding="utf-8") as f:
    json.dump({"status":"done"},f)

subprocess.run(["git","config","user.name","מאיה"])
subprocess.run(["git","config","user.email","maya@nagaria.app"])
subprocess.run(["git","add","commands/pending.json"])
subprocess.run(["git","commit","-m","clear [skip ci]"])
subprocess.run(["git","push"])
print("Done!")
