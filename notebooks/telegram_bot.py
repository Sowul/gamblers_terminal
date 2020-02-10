from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
import requests

trigger = OrTrigger([
   CronTrigger(hour='7', minute='30-59'),
   CronTrigger(hour='8-22', minute='*'),
   CronTrigger(hour='23', minute='0-30')
])

def check_cdp(cdp_no=44120):
    try:
        resp = requests.get(f'https://mkr.tools/api/v1/cdp/{cdp_no}').json()[0]
        msg = f"""
{datetime.now().strftime("%H:%M:%S")}
CDP ({resp['id']}) is {'**SAFE** 😁' if round(100*resp['art'] / resp['tab'], 2) < 66.5 else '**RISKY** 😨'}
**Collateral USD**: ${round(resp['tab'], 2)}
**Debt**: {round(resp['art'], 2)} DAI
**Available (Max)**: {round(resp['tab']*0.6665585 - resp['art'], 2)} DAI
**Collateral**: {round(resp['ink']*float(resp['per']), 2)} ETH
**Free (Max)**: {round(resp['ink']*float(resp['per']) - resp['art']/(0.6665585*resp['pip']), 2)} ETH
**ETH Price**: ${round(resp['pip'], 2)}
**Liquidation**: ${round(resp['liq_price'], 2)}
**Ratio**: {round(100*resp['art'] / resp['tab'], 2)}%
"""
    except requests.exceptions.RequestException as e:
        msg='Something went wrong! Caught requests.exceptions.RequestException.'
    print(msg)

def main():
    sched = BackgroundScheduler()
    sched.add_job(trigger=trigger, func=check_cdp, args=[44120])
    sched.start()

if __name__ == "__main__":
    check_cdp(cdp_no=44120)
    main()