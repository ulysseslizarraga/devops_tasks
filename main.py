import os
import colorama
import datetime
import devops_tasks.devops_adapter as doa

colorama.init()
format_str = '%m/%d %I:%M %p'

try:
    while True:
        devops_adapter = doa.DevOpsAdapter()
        now = datetime.datetime.now()
        print(f"\n[{now.strftime(format_str)}]: {devops_adapter.clr.OKGREEN}Retrieved data from DevOps{devops_adapter.clr.ENDC}")
        devops_adapter.print_work_items()
        input()

except KeyboardInterrupt:
    print(f"\nKeyboard interrupt: shutting down")
