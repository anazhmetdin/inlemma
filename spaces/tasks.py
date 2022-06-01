from celery import shared_task
from .utils import inlemmaEngine

@shared_task(bind=True, name='updateD2Vmodel')
def updateD2Vmodel(self):
    inlemmaEngine.updateD2Vmodel()
    return True