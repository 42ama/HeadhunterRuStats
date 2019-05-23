import os

script_dir=os.path.dirname(os.path.abspath("_main.py"))
with open('run_hhrustats.bat', 'w') as f:
	f.write("python "+script_dir+"\\_main.py")
print("Completed")