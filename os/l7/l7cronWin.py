from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

def run_script():
    subprocess.Popen([
        r"C:\Users\Валера\AppData\Local\Programs\Python\Python313\python.exe",
        r"S:\Users\L\Downloads\New folder (175)\testgit\os\l6\l6py\l6_mmap_big_array.py"
    ])

scheduler = BlockingScheduler()
scheduler.add_job(run_script, 'cron', minute='*')  # every minute
scheduler.start()
