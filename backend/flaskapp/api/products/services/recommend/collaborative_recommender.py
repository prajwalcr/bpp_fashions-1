import json

from flaskapp.api.products.dal.product import ProductDAL
from flaskapp.database import db


class CollaborativeRecommender:
    def __init__(self, products_prob=None):
        self.products_prob = products_prob

    def load_df(self, filepath):
        with open(filepath) as f:
            self.products_prob = json.load(f)

    def recommend(self, product_id, k=4):
        finalpred = []
        if product_id not in self.products_prob['columns']:
            print('[]')
            return []
        else:
            index = self.products_prob['columns'].index(product_id)
            ratings = self.products_prob['data']
            indexratings = []
            for i in ratings:
                indindexratings = []
                for j in range(len(i)):
                    indindexratings.append([i[j], j])
                indexratings.append(indindexratings)
            s = indexratings[index]
            sorte = sorted(s, key=lambda x: x[0], reverse=True)
            no_of_suggestions = k
            pred = sorte[:no_of_suggestions]

            for i in pred:
                finalpred.append([self.products_prob['columns'][i[1]]])

        finalpred = [ProductDAL.find_by_id(db, product[0]) for product in finalpred]

        return finalpred
