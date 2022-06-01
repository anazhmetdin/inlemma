from celery import shared_task
from .utils import inlemmaEngine

@shared_task(bind=True)
def updateD2Vmodel(self):
    inlemmaEngine.updateD2Vmodel()
    return True