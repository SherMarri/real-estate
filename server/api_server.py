import logging
from logging.handlers import RotatingFileHandler
import os
from utils.config import CONFIG, init_from_file
from schemas.job import Job
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from services.crawler_service import crawler_service


def get_env():
    return os.environ.get("API_ENV", "local")


def is_local_env():
    return get_env() == "local"


def root_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_logger(app: Flask):
    LOG_LOCATION = "/log/application.log"
    LOG_FILE_MAX_BYTES = 1024 * 1024 * 50  # 50 MBs
    handler = RotatingFileHandler(LOG_LOCATION, maxBytes=LOG_FILE_MAX_BYTES, backupCount=5)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info("Logger setup successfully.")


def setup_config(app: Flask):
    if not CONFIG.is_already_initialized():
        init_from_file("configs/{}.yml".format(get_env()), **dict(os.environ))


def setup_db_configs(app: Flask):
    DATABASE_URI = {"zameen_data": CONFIG.get("db", "url")}
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI["zameen_data"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



application = Flask(__name__)
setup_logger(application)
setup_config(application)
setup_db_configs(application)
db = SQLAlchemy(application)


@application.before_request
def log_request():
    """Prints requests to standard output."""
    application.logger.info(request)


@application.route('/')
def status():
    return {"message": "Server is healthy."}

@application.route("/crawler/crawl_rental_area_properties")
def crawl_rental_area_properties():
    # Hardcoded for Karachi temporarily
    job = Job()
    job.city = "Karachi"
    job.job_type = Job.JOB_TYPE_CRAWL_RENTAL_AREA_PROPERTIES
    crawler_service.process_job(job)
    return {"message": "success"}
