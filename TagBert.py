import numpy as np
from typing import List, Union, Tuple
import torch
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from packaging import version
from sklearn import __version__ as sklearn_version
class TagBert:
    def __init__(self,model,tokenizer,encode,embed):
        self.model=model
        self.tokenizer=tokenizer
        self.encode=encode
        self.embed=embed
        

    def extract_tag(
        self,
        docs: Union[str, List[str]],
        candidates: List[str] = None,
        keyphrase_ngram_range: Tuple[int, int] = (1, 1),
        stop_words: Union[str, List[str]] = "english",
        top_n: int = 5,
        min_df: int = 1,
        use_maxsum: bool = False,
        use_mmr: bool = False,
        diversity: float = 0.5,
        nr_candidates: int = 20,
        vectorizer: CountVectorizer = None,
        seed_keywords: List[str] = None,
    ) -> Union[List[Tuple[str, float]], List[List[Tuple[str, float]]]]:
        if isinstance(docs,str):
            if docs:
                docs=[docs]
            else:
                return []
        
        if vectorizer:
            count = vectorizer.fit(docs)
        else:
            try:
                count = CountVectorizer(
                    ngram_range=keyphrase_ngram_range,
                    stop_words=stop_words,
                    min_df=min_df,
                ).fit(docs)
            except ValueError:
                return []
        
        if version.parse(sklearn_version) >= version.parse("1.0.0"):
            words = count.get_feature_names_out()
        else:
            words = count.get_feature_names()

        df = count.transform(docs)

        encoded_words=self.encode(self.tokenizer,words)
        encoded_docs=self.encode(self.tokenizer,docs)

        doc_embeddings = self.embed(self.model,encoded_docs)
        word_embeddings = self.embed(self.model,encoded_words)

        doc_embeddings=np.array([ele.detach().numpy() for ele in doc_embeddings])
        word_embeddings=np.array([ele.detach().numpy() for ele in word_embeddings])

        all_tags=[]

        for index,_ in enumerate(docs):
            try:
                candidate_indices = df[index].nonzero()[1]
                candidates = [words[index] for index in candidate_indices]
                candidate_embeddings = word_embeddings[candidate_indices]
                doc_embedding = doc_embeddings[index]

                # Guided KeyBERT with seed keywords
                if seed_keywords is not None:
                    seed_embeddings = self.model.embed([" ".join(seed_keywords)])
                    doc_embedding = np.average(
                        [doc_embedding, seed_embeddings], axis=0, weights=[3, 1]
                    )

                if use_maxsum:
                    pass
                else:
                    candidate_embeddings=np.squeeze(candidate_embeddings,axis=1)
                    distances = cosine_similarity(doc_embedding, candidate_embeddings)
                    tags = [
                        (candidates[index], round(float(distances[0][index]), 4))
                        for index in distances.argsort()[0][-top_n:]
                    ][::-1]
                
                all_tags.append(tags)
            except ValueError:
                print("Value Error")
                all_tags=[[]]
        
        return all_tags



        