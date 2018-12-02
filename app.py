from flask import Flask, render_template, abort, flash, redirect, url_for, session
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

# Initialize extensions to be used in app
# Bootstrap extension
bootstrap = Bootstrap(app)
# Moment extension for time formatting
moment = Moment(app)
# Mail extension for sending mails
mailer.mail.init_app(app)
# Models extension for accessing database tables
models.db.init_app(app)


def scrape_news():

    try:
        print("Vanguard")
        vanguard = scraper.Vanguard()
        vanguard.get_titles()
        vanguard.get_summary()
        vanguard.get_links()
        vanguard.get_post_times()

        print("PremiumTimes")
        premiumtimes = scraper.PremiumTimes()
        premiumtimes.get_titles()
        premiumtimes.get_summary()
        premiumtimes.get_links()
        premiumtimes.get_post_times()

        vanguard_populator = populate_db.DBPopulate(vanguard.summary, vanguard.time, vanguard.links, vanguard.titles)
        vanguard_populator.add_to_db()

        premiumtimes_populator = populate_db.DBPopulate(premiumtimes.summary, premiumtimes.time, premiumtimes.links,
                                                      premiumtimes.titles)
        premiumtimes_populator.add_to_db()

    except requests.exceptions.ConnectionError:
        print("Connection Error")


# Create a schedule to run the scrape_news function in the background
scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_news, trigger="interval", seconds=240)
# Starts the schedule
scheduler.start()

# Shuts down scheduler before file exists
atexit.register(lambda: scheduler.shutdown())


@app.route("/", methods=["GET", "POST"])
@app.route("/<int:number>", methods=["GET", "POST"])
def index(number=None):
    """
    :desc: Function is invoked when requests are made to the following urls:
            domainname/
            domainname/number e.g domainname/1, domaainname/2, domainname/3

    :param number: The page number to be accessed. Defaults to None.
    :return: a rendered template to match the request
    """

    # Fetch the news from database and sort according to time
    # in descending order
    news_details = models.News.query.all()
    sorted_news_details = sorted(news_details, key=lambda news: news.time, reverse=True)

    # 6 news would be displayed per page
    number_of_news_per_page = 6

    # Create sessions to ensure feedback is left once
    if "vote" in session.keys():
        form = None
    else:
        form = forms.FeedbackForm()
        if form.validate_on_submit():
            session["vote"] = 1
            flash("Thanks for giving feedback")
            votes = models.Votes(upvote=form.upvote.data, downvote=form.downvote.data)
            models.db.session.add(votes)
            models.db.session.commit()
            return redirect(url_for("index"))

    # Handle requested pages, checking if news exist for requested page
    # When news doesn't exist for requested page, request is aborted
    if number is not None and number > 1:
        if len(news_details) > number_of_news_per_page * (number - 1):
            page_articles_beginning = number_of_news_per_page * (number - 1)
            page_articles_ending = number_of_news_per_page * (number)
            page_title = "Strikometer - {}".format(number)
            return render_template("index.html",
                                   news_details=sorted_news_details[page_articles_beginning:page_articles_ending],
                                   page_title=page_title, form=form)
        else:
            abort(404)
    elif number is None or number == 1:
        page_title = "Strikometer"
        return render_template("index.html", news_details=sorted_news_details[:number_of_news_per_page],
                               page_title=page_title, form=form)



@app.route("/about")
def about():
    """
    Function is invoked when requests is made to url: dommainname/about
    :return: a rendered template for the about page
    """
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
        Function is invoked when requests is made to url: dommainname/contact
        :return: a rendered template for the about page
        """

    # Accesses the contact form and renders it in the contact html file
    # Submits the filled form and sends the values in a mail to a configured email address
    form = forms.ContactForm()
    if form.validate_on_submit():
        flash("Thanks for reaching out.")
        contact_mailer = mailer.Mailer(form.first_name.data, form.last_name.data, form.email.data, form.message.data)
        contact_mailer.send_messages()
        return redirect(url_for("index"))
    return render_template("contact.html", form=form)


@app.errorhandler(404)
def page_not_found(e):
    """
    Function is invoked when the requests made to the url have no response i.e. the page
    doesn't exist.

    The errorhandler decorator passes an error message to the function.
    Therefore is has to be received even when not used.

    :param e: The error message
    :return: a rendered template for the 404 page
    """
    return render_template("404.html")


if __name__ == '__main__':
    app.run()