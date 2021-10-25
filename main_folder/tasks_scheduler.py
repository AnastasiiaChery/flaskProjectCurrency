from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from main_folder.loading_currencies import get_data_from_app

client = MongoClient('localhost', 27017)

jobstores = {
    'mongo': MongoDBJobStore(collection='job', database='test', client=client),
    'default': MemoryJobStore()
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
scheduler.add_job(get_data_from_app, 'cron', day='1-31', hour=16, minute=30)

try:
    scheduler.start()
except SystemExit:
    client.close()
