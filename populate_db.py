import models
import app


class DBPopulate(object):
    """
    Object adds initialization parameters to the database

    :params : summary --> String object
                time --> Datetime object
                link --> String object
                title --> String object
    """
    def __init__(self, summary, time, link, title):
        self.summary = summary
        self.time = time
        self.link = link
        self.title = title

    def add_to_db(self):
        for summary, time, link, title in zip(self.summary, self.time, self.link, self.title):
            # Activates the app context
            # This needed to be able to access the database
            with app.app.app_context():
                # Adds news to database only if link doesn't already exist
                if models.News.query.filter(models.News.link == link).first():
                    continue
                else:
                    news = models.News(summary=summary, link=link, title=title, time=time)
                    models.db.session.add(news)
                models.db.session.commit()
