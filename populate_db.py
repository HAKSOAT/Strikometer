import models
import app

class DBPopulate(object):

    def __init__(self, summary, time, link, title):
        self.summary = summary
        self.time = time
        self.link = link
        self.title = title

    def add_to_db(self):
        for summary, time, link, title in zip(self.summary, self.time, self.link, self.title):
            with app.app.app_context():
                if models.News.query.filter(models.News.link == link).first():
                    continue
                else:
                    news = models.News(summary=summary, link=link, title=title, time=time)
                    models.db.session.add(news)
                    print("New data")
                models.db.session.commit()
