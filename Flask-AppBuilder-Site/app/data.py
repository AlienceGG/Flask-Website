import datetime
import random
import logging
from models import Gender, Country, CountryStats
from app import db

log = logging.getLogger(__name__)


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()


def fill_data():
    countries = ['LR', 'SVM', 'DT', 'RF', 'PB', 'DNN', 'PCA+DNN', 'PCA+RF']
    for country in countries:
        c = Country(name=country)
        try:
            db.session.add(c)
            db.session.commit()
        except Exception as e:
            log.error("Update ViewMenu error: {0}".format(str(e)))
            db.session.rollback()
    try:
        data = db.session.query(CountryStats).all()
        if len(data) == 0:
            for x in range(1, 40):
                cs = CountryStats()
                cs.temperature = random.randint(1, 100)
                cs.power = random.randint(1, 100)
                cs.electricity = random.randint(1, 100)

                cs.voltage = random.randint(1, 100)
                cs.pressure = random.randint(1, 100)
                db.session.add(cs)
                db.session.commit()
    except Exception as e:
        log.error("Update Data error: {0}".format(str(e)))
        db.session.rollback()
