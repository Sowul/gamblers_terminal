import sys
sys.path.append("..")

from flask import Flask, jsonify
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

BETS = [
    {
        'arb': '3.05%',
        'age': '4 min',
        'sport': 'Hockey',
        'participants': 'Italy vs Belarus',
        'type': 'CM',
        'bet1': '3.10 @ StanleybetDK',
        'bet1Odds': 3.10,
        'bet2': '2.90 @ Pinnacle',
        'bet2Odds': 2.90,
        'bet3': '3.30 @ Pinnacle',
        'bet3Odds': 3.30,
    },
    {
        'arb': '9.77%',
        'age': '43 min',
        'sport': 'Soccer',
        'participants': 'FC Sabah vs Neftchi',
        'type': 'CM',
        'bet1': '2.10 @ Pinnacle',
        'bet1Odds': 2.10,
        'bet2': '2.30 @ PaddyPower',
        'bet2Odds': 2.30,
    }
]

import random
def testo():
    print('scraping markets...')
    BETS[0]['age'] = f'{random.randint(1, 10)} min'
    BETS[1]['age'] = f'{random.randint(1, 10)} min'
    print('done')
    return BETS

from datetime import datetime
def tick():
    print('Tick! The time is: %s' % datetime.now())
    testo()
    # scraper_manager.get_all_markets()
    # swap this testo function with scraper_manager.get_all_markets() function when you implement it

@app.route('/bets', methods=['GET'])
def all_bets():
    return jsonify({
        'status': 'success',
        'bets': testo()
    })

if __name__ == '__main__':
    from apscheduler.schedulers.background import BackgroundScheduler

    sched = BackgroundScheduler()
    sched.add_job(tick, 'interval', seconds=3)
    sched.start()  # start the scheduler

    app.run()