from crontab import CronTab

# Use the current user's cron
cron = CronTab(user='vboxuser')

# Create a new cron job
job = cron.new(
    command='python "/home/testgit/os/l6/l6py/l6_mmap_big_array.py"',
    comment='My job'
)

job.setall('*/1 * * * *')  # Every minute
cron.write()