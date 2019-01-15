from flask import current_app
from google.cloud import firestore


def init_app(app):
    pass


def get_client():
    return firestore.Client(current_app.config['PROJECT_ID'])


def create(data):
    db = get_client()

    try:
        db.collection(u'uploads').document(u'original').set(data, merge=True)
        current_app.logger.info('Added entry {}'.format(data))
    except:
        current_app.logger.info('Error adding entry {}'.format(data))
