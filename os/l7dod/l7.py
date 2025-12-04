import os

# Example: Run my_script.py every day at 19:00
python_path = r"C:/Users/Валера/AppData/Local/Programs/Python/Python313/python.exe"
script_path = r"S:\Users\L\Downloads\New folder (175)\testgit\os\l6\l6py\l6_mmap_big_array.py"

command = f'schtasks /create /tn "MyPythonTask" /tr "{python_path} {script_path}" /sc daily /st 18:47 /rl HIGHEST'
os.system(command)