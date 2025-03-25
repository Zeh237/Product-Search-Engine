import atexit
from flask.cli import FlaskGroup
from src import app
from apscheduler.schedulers.background import BackgroundScheduler
# from src.tasks.scheduler import schedule_tasks, scheduler
#
# schedule_tasks()
#
# atexit.register(lambda: scheduler.shutdown(wait=False))

cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
