from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config
from apscheduler.schedulers.background import BackgroundScheduler
import models
import atexit
import scraper
import populate_db
import logging
import requests

app = Flask(__name__)

app.config.from_object(config["development"])

bootstrap = Bootstrap(app)
moment = Moment(app)
models.db.init_app(app)

logging.basicConfig(filename='errors.log', level=logging.DEBUG)

def scrape_news_in_background():
    try:
        vanguard = scraper.Vanguard()
        vanguard.get_titles()
        vanguard.get_summary()
        vanguard.get_links()
        vanguard.get_post_times()

        the_nation = scraper.TheNation()
        the_nation.get_titles()
        the_nation.get_summary()
        the_nation.get_links()
        the_nation.get_post_times()

        vanguard_populator = populate_db.DBPopulate(vanguard.summary, vanguard.time, vanguard.links, vanguard.titles)
        vanguard_populator.add_to_db()

        the_nation_populator = populate_db.DBPopulate(the_nation.summary, the_nation.time, the_nation.links, the_nation.titles)
        the_nation_populator.add_to_db()

    except requests.exceptions.ConnectionError:
        logging.info("Requests error", exc_info=True)


scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_news_in_background, trigger="interval", seconds=360)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@app.route("/")
@app.route("/<int:number>")
def index(number=None):
    news_details = models.News.query.all()
    if number:
        a = "Strikometer - {}".format(number)
        return render_template("index.html", news_details = news_details)
    else:
        "Strikometer"
        return render_template("index.html")


@app.route("/about")
def about():
    return "Strikometer - About"


@app.route("/contact")
def contact():
    return "Strikometer - Contact"



if __name__ == '__main__':
    app.run()