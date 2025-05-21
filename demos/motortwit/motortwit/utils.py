import os
from hashlib import md5

import pymongo
from pymongo import MongoClient
import pytz
import yaml
from aiohttp import web
from dateutil.parser import parse
from pydantic import ValidationError

from . import db
from .models import UserCreate


def load_config(fname):
    with open(fname, 'rt') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    # TODO: add config validation
    return data


async def init_mongo(conf):
    host = os.environ.get('DOCKER_MACHINE_IP', '127.0.0.1')
    conf['host'] = host
    mongo_uri = "mongodb://{}:{}".format(conf['host'], conf['port'])
    client = MongoClient(
        mongo_uri,
        maxPoolSize=conf['max_pool_size']
    )
    db_name = conf['database']
    return client[db_name]


def robo_avatar_url(user_data, size=80):
    """Return the gravatar image for the given email address."""
    hash = md5(str(user_data).strip().lower().encode('utf-8')).hexdigest()
    url = "https://robohash.org/{hash}.png?size={size}x{size}".format(
        hash=hash, size=size)
    return url


def format_datetime(timestamp):
    if isinstance(timestamp, str):
        timestamp = parse(timestamp)
    return timestamp.replace(tzinfo=pytz.utc).strftime('%Y-%m-%d @ %H:%M')


def redirect(request, name, **kw):
    router = request.app.router
    location = router[name].url_for(**kw)
    return web.HTTPFound(location=location)


async def validate_register_form(mongo, form_data):
    """Validate registration form data using Pydantic."""
    try:
        # Validate form data using Pydantic model
        user_data = UserCreate(**form_data)
        
        # Check if username is already taken
        user_id = await db.get_user_id(mongo.user, user_data.username)
        if user_id is not None:
            return 'The username is already taken'
            
        return None
    except ValidationError as e:
        # Return the first validation error message
        return str(e.errors()[0]['msg'])
