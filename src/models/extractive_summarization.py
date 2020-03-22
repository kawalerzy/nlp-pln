import torch
import pandas as pd
import numpy as np
from config import SQLALCHEMY_ENGINE_STR
from db import get_engine_session, Article
from itertools import groupby
from nltk.tokenize import sent_tokenize
from sklearn.cluster import KMeans
from transformers import BertTokenizer, BertModel, BertForMaskedLM


class Summarizer:

    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.model = BertModel.from_pretrained('bert-base-multilingual-cased')
        self.model.eval()

    def batch_summarization(self, text_list, k):
        summary = []
        for text in text_list:
            summary.append(self.summarize_text(text, k))
        return summary

    def summarize_text(self, text, k):
        text = self.clean_text(text)
        tokenized_sent = np.array(sent_tokenize(text))
        sent_encodings = [self.encode_sentence(sent) for sent in tokenized_sent]
        sent_encodings = torch.cat(sent_encodings).numpy()
        kmeans = KMeans(n_clusters=k, random_state=0).fit(sent_encodings)
        cluster_mins = self.find_representants(sent_encodings, kmeans)
        summary_list = tokenized_sent[sorted(cluster_mins.distance)]
        summary = ' '.join([str(sent) for sent in summary_list])
        return summary

    def find_representants(self, sent_encodings, kmeans):
        cluster_centers = kmeans.cluster_centers_[kmeans.labels_]
        dist_from_center = np.sum((sent_encodings - cluster_centers)**2, axis=1)
        dist_df = pd.DataFrame({'label': kmeans.labels_, 'distance': dist_from_center})
        cluster_mins = dist_df.groupby('label').idxmin()
        return cluster_mins


    def encode_sentence(self, sentence):
        marked_text = '[CLS] ' + sentence + ' [SEP]'
        tokenized_text = self.tokenizer.tokenize(marked_text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        segments_ids = [1] * len(tokenized_text)

        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])

        with torch.no_grad():
            # See the models docstrings for the detail of the inputs
            outputs = self.model(tokens_tensor, segments_tensors)
            # Transformers models always output tuples.
            # See the models docstrings for the detail of all the outputs
            # In our case, the first element is the hidden state of the last layer of the Bert model
            encoded_layers = outputs[0]
            return encoded_layers[0][0].reshape(1,768)

    def clean_text(self, text):
        text = text.replace('- KLIKNIJ!', '')
        return text

## EXAMPLE: ##
engine, session = get_engine_session(SQLALCHEMY_ENGINE_STR, verbose=False)
df = pd.read_sql(session.query(Article).limit(10).statement, session.bind)

s = Summarizer()

text = df.text[1]
summary = s.summarize_text(text, 3)

text_list = df.text
summary_list = s.batch_summarization(text_list, 3)
