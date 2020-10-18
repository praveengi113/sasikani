import uuid
from src.common.database import Database
from datetime import datetime
from pytz import timezone


class Feed(object):

    def __init__(self, cases, cured, death, created_date=datetime.now(timezone('Asia/Kolkata')).strftime("%d/%m/%Y "
                                                                                                         "%H:%M:%S"),
                 _id=None):
        self.cases = cases
        self.cured = cured
        self.death = death
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='feeds',
                        data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'cases': self.cases,
            'cured': self.cured,
            'death': self.death,
            'time': self.created_date
        }

    @staticmethod
    def from_mongo():
        feed_data = Database.find(collection='feeds')
        return [feed for feed in feed_data]

    @staticmethod
    def from_mongo_all():
        all_data = Database.find(collection='feeds').sort([("_id", -1)])
        return [feed for feed in all_data]
