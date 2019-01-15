from __future__ import absolute_import
import datetime
from flask import current_app
from google.cloud import storage
import six
from werkzeug import secure_filename
from werkzeug.exceptions import BadRequest
from model.ImagePipeline import ImagePipeline


def _get_storage_client():
    return storage.Client(project=current_app.config['PROJECT_ID'])


def _check_extension(filename, allowed_extensions):
    if '.' not in filename or filename.split('.').pop().lower() not in allowed_extensions:
        raise BadRequest('{} has an invalid name or extension'.format(filename))


def _safe_filename(filename):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage
    :param filename:
    :return: filename.ext is transformed into filename-YYYY-MM-DD-HHMMSS.ext
    """
    filename = secure_filename(filename)
    date = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
    basename, extension = filename.rsplit('.', 1)
    return '{}-{}.{}'.format(basename, date, extension)


def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket.
    :param file_stream:
    :param filename:
    :param content_type:
    :return: public url of given object
    """
    _check_extension(filename, current_app.config['ALLOWED_EXTENSIONS'])
    filename = _safe_filename(filename)

    client = _get_storage_client()
    bucket = client.bucket(current_app.config['CLOUD_STORAGE_BUCKET'])
    blob = bucket.blob("uploads/"+filename)

    blob.upload_from_string(file_stream, content_type=content_type)

    url = blob.public_url

    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url, filename
