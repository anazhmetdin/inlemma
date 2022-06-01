import multiprocessing as mp
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from datetime import datetime
from posts.models import Post
from django.conf import settings
from .models import ProcessedPost


class TaggedCorpus:        
    def __iter__(self):
        for processedPost in ProcessedPost.objects.all():
            title, words = str(processedPost.post.id), processedPost.body
            words = words.split()
            # if len(words) < 75:
            #     continue
            yield TaggedDocument(words=words, tags=[title])


class inlemmaCore():
    def __init__(self, D2VmodelPath=f'{settings.BASE_DIR}/spaces/D2Vmodels/latest.model'):
        try:
            self.D2Vmodel = self.loadD2Vmodel(D2VmodelPath)
        except:
            self.D2Vmodel = None
            self.updateD2Vmodel()
    
    def loadD2Vmodel(self, D2VmodelPath):
        return Doc2Vec.load(D2VmodelPath)
    
    def updateD2Vmodel(self):
        try:
            self.D2Vmodel.save(f'{settings.BASE_DIR}/spaces/D2Vmodels/{datetime.now().strftime("%d_%m_%Y_%H_%M")}.model')
        except:
            pass
        documents = TaggedCorpus()
        workers = mp.cpu_count() - 4  # multiprocessing.cpu_count() - 1  # leave one core for the OS & other stuff
        # PV-DM: paragraph vector in distributed memory mode
        model_dm = Doc2Vec(
            # hs=1, negative=0,
            dm=1, dm_mean=1,  # use mean of context word vectors to train DM
            vector_size=100, window=8, epochs=60, workers=workers, max_final_vocab=1000000,
        )
        model_dm.build_vocab(documents, progress_per=100000)
        model_dm.train(documents, total_examples=model_dm.corpus_count, epochs=model_dm.epochs, report_delay=15*60)
        self.D2Vmodel = model_dm
        self.D2Vmodel.save(f'{settings.BASE_DIR}/spaces/D2Vmodels/latest.model')

    def similarPosts(self, post, n=5):
        similars = self.__similarPosts(post, n)
        return [Post.objects.get(id=int(similiar[0])) for similiar in similars]

    def __similarPosts(self, post, n):
        if str(post.id) not in self.D2Vmodel.dv:
            try:
                processedPost = ProcessedPost.objects.get(post=post)
            except:
                return []
            vector = self.D2Vmodel.infer_vector(processedPost.body.split())
            self.D2Vmodel.dv.add_vector(str(post.id), vector)
            self.D2Vmodel.dv.norms = None
        return self.D2Vmodel.dv.most_similar(positive=[str(post.id)], topn=n)


inlemmaEngine = inlemmaCore()