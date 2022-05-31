import string
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from posts.models import Post
import bleach
from html2text import html2text
import threading
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# download the latest version of nltk datasets
nltk.download('punkt')
nltk.download('stopwords')


class ProcessedPost(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, db_index=True)
    body = models.TextField(blank=False, null=False)


@receiver(models.signals.post_save, sender=Post)
def post_saved(sender, instance, **kwargs):
    processedPost = ProcessedPost.objects.create(post=instance,
                                                 body=instance.body)
    PostProcessor(processedPost).run()


class PostProcessor(threading.Thread):
    def __init__(self, processedPost):
        self.processedPost = processedPost
        threading.Thread.__init__(self)

    def tokenize(self, doc, stop_words):
        tokens = word_tokenize(doc.lower())
        return " ".join([w for w in tokens if not w in stop_words])
    
    def process(self, body):
        ONE_OR_MORE = "+"
        START = "^"
        END = "$"

        PUNCTUATION = '[^\w\s]' #^=not, \w=alphanumeric character, \s=space
        SPACE = "\s"
        ERASE = ""
        NEWLINES = "[\r\n\t]"

        stop_words = set(stopwords.words('english'))
        
        processedBody = body.lower()
        
        processedBody = re.sub(PUNCTUATION, ' ', processedBody)
        processedBody = processedBody.translate(str.maketrans(dict.fromkeys(string.punctuation)))
        processedBody = re.sub(NEWLINES, ' ', processedBody)
        processedBody = re.sub(SPACE+ONE_OR_MORE, " ", processedBody)
        processedBody = re.sub(SPACE, " ", processedBody)
        processedBody = re.sub(START+SPACE, ERASE, processedBody)
        processedBody = re.sub(SPACE+END, ERASE, processedBody)
        processedBody = self.tokenize(processedBody, stop_words)
        
        return processedBody

    def run(self):
        cleanedBody = bleach.clean(self.processedPost.body,
                                   tags=settings.BLEACH_ALLOWED_STYLES,
                                   attributes=settings.BLEACH_ALLOWED_ATTRIBUTES)
        body = html2text(cleanedBody)
        self.processedPost.body = self.process(body)
        self.processedPost.save()
        from .utils import inlemmaEngine
        vector = inlemmaEngine.D2Vmodel.infer_vector(self.processedPost.body.split())
        inlemmaEngine.D2Vmodel.dv.add_vector(str(self.processedPost.post.id), vector)
        inlemmaEngine.D2Vmodel.dv.norms = None