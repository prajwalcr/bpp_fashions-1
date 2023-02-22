import pickle
from typing import Optional

import torch
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils import PreTrainedTokenizer
from datasets import Dataset

from flaskapp.api.products.dal.product import ProductDAL
from flaskapp.database import db, engine

import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'


class Encoder:
    def __init__(self, tokenizer: PreTrainedTokenizer, model: PreTrainedModel,
                 dataset: Optional[Dataset]=None) -> None:
        self.embeddings_dataset = None
        self.tokenizer = tokenizer
        self.model = model
        self.dataset = dataset

    def load_product_dataset(self):
        df = ProductDAL.find_all_df(db, engine)
        product_dataset = Dataset.from_pandas(df)
        self.dataset = product_dataset
        self.clean_product_dataset()

    def clean_product_dataset(self):
        self.dataset = self.dataset.filter(lambda example: example["productDescription"] is not None)

    def embed_dataset(self):
        if self.dataset is None:
            self.load_product_dataset()
        self.model.eval()
        with torch.no_grad():
            product_embeddings_dataset = \
                self.dataset.map(lambda example: {
                    'embeddings':
                        self.model(**self.tokenizer(example["productDescription"], return_tensors="pt")).pooler_output[0].numpy()
                })

        product_embeddings_dataset.add_faiss_index(column="embeddings")
        self.embeddings_dataset = product_embeddings_dataset

    def save_embeddings(self, filepath):
        embeddings_file = open(filepath, 'wb')
        pickle.dump(self.embeddings_dataset, embeddings_file)

    def load_embeddings(self, filepath):
        try:
            embeddings_file = open(filepath, 'rb')
            self.embeddings_dataset = pickle.load(embeddings_file)
        except FileNotFoundError as e:
            print("Embedding file not found")
            print(e)

    def retrieve_nearest(self, product_id, k=5):
        if self.embeddings_dataset is None:
            return 0

        product = ProductDAL.find_by_id(db, product_id)
        product_description = product.productDescription

        self.model.eval()
        with torch.no_grad():
            product_embedding = self.model(**self.tokenizer(product_description, return_tensors="pt")).pooler_output[
                0].numpy()
        scores, retrieved_product_dataset = self.embeddings_dataset.get_nearest_examples('embeddings', product_embedding, k=k)
        retrieved_product_ids = retrieved_product_dataset["id"][1:]
        print(scores, retrieved_product_ids)

        retrieved_products = [ProductDAL.find_by_id(db, retrieved_product_id) for retrieved_product_id in retrieved_product_ids]
        return scores, retrieved_products






