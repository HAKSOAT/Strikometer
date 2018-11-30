from flask import Flask, render_template, abort, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import os
from config import config
from apscheduler.schedulers.background import BackgroundScheduler
import models
import atexit
import scraper
import populate_db
import requests
import forms
import mailer

app = Flask(__name__)

app.config.from_object(config[os.environ["APP_CONFIG"]])

bootstrap = Bootstrap(app)
moment = Moment(app)
mailer.mail.init_app(app)
models.db.init_app(app)


def scrape_news_in_background():
    try:
        print("Start")
        vanguard = scraper.Vanguard()
        vanguard.get_titles()
        vanguard.get_summary()
        vanguard.get_links()
        vanguard.get_post_times()

        print("Half")
        the_nation = scraper.TheNation()
        the_nation.get_titles()
        the_nation.get_summary()
        the_nation.get_links()
        the_nation.get_post_times()

        vanguard_populator = populate_db.DBPopulate(vanguard.summary, vanguard.time, vanguard.links, vanguard.titles)
        vanguard_populator.add_to_db()

        the_nation_populator = populate_db.DBPopulate(the_nation.summary, the_nation.time, the_nation.links,
                                                      the_nation.titles)
        the_nation_populator.add_to_db()

    except requests.exceptions.ConnectionError:
        print("Connection Error")


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=scrape_news_in_background, trigger="interval", seconds=360)
# scheduler.start()
#
# atexit.register(lambda: scheduler.shutdown())


@app.route("/")
@app.route("/<int:number>")
def index(number=None):
    scrape_news_in_background()
    news_details = models.News.query.all()
    sorted_news_details = sorted(news_details, key=lambda news: news.time, reverse=True)
    number_of_news_per_page = 6
    if number is not None and number > 1:
        if len(news_details) > number_of_news_per_page * (number - 1):
            page_articles_beginning = number_of_news_per_page * (number - 1)
            page_articles_ending = number_of_news_per_page * (number)
            page_title = "Strikometer - {}".format(number)
            return render_template("index.html",
                                   news_details=sorted_news_details[page_articles_beginning:page_articles_ending],
                                   page_title=page_title)
        else:
            abort(404)
    elif number is None or number == 1:
        page_title = "Strikometer"
        return render_template("index.html", news_details=sorted_news_details[:number_of_news_per_page],
                               page_title=page_title)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = forms.ContactForm()
    if form.validate_on_submit():
        flash("Thanks for reaching out.")
        contact_mailer = mailer.Mailer(form.first_name.data, form.last_name.data, form.email.data, form.message.data)
        contact_mailer.send_messages()
        return redirect(url_for("index"))
    return render_template("contact.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run()