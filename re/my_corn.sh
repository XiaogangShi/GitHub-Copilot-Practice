# 写一个cronjob脚本，每天下午 14：51点执行 "/bin/ps"  命令。并且把log输出到 ~/xgshi/code/GitHub-Copilot-Practice/re/cron_ps.log 文件中。
#!/bin/bash
# This script sets up a cron job to run "/bin/ps" every day at 2:51 PM.

# Define the cron job command
CRON_JOB="51 14 * * * /bin/ps >> ~/xgshi/code/GitHub-Copilot-Practice/re/cron_ps.log 2>&1"
# Check if the cron job already exists
(crontab -l | grep -F "$CRON_JOB") || (crontab -l; echo "$CRON_JOB") | crontab - -