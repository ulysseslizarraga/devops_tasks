import os
import colorama
import datetime
from libops import colorstr
import devops_tasks.devops_adapter as doa

colorama.init()
clr = colorstr.bcolors()
format_str = '%m/%d %I:%M %p'

try:
    while True:
        now = datetime.datetime.now()
        print(f"\n[{now.strftime(format_str)}]: {clr.WARNING}Retrieving data from DevOps{clr.ENDC}")
        devops_adapter = doa.DevOpsAdapter()
        now = datetime.datetime.now()
        print(f"[{now.strftime(format_str)}]: {clr.OKGREEN}Retrieved data from DevOps{clr.ENDC}")
        devops_adapter.print_work_items()
        input()
except KeyboardInterrupt:
    print(f"\nKeyboard interrupt: shutting down")
