import os

from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import community.community_louvain as community_louvian
import random
import uuid

from flaskapp.api.products.services.recommend.collaborative_recommender import CollaborativeRecommender
from flaskapp.api.products.services.recommend.encoder import Encoder
from flaskapp.cache import cache
from flaskapp.api.products.services.product import ProductService
from flaskapp.api.products.services.search import SearchService
from flaskapp.schemas import PlainProductSchema, SearchSchema, ProductListSchema, PaginationSchema

from transformers import AutoTokenizer, AlbertModel
import torch


blp = Blueprint("product", __name__, description="Operations on products")


@blp.route("/api/products/<string:product_id>")
class Product(MethodView):
    """Controller class for handling requests on products."""
    @blp.response(200, PlainProductSchema)
    def get(self, product_id):
        product = ProductService.find_by_id(product_id)

        if product is None:
            search_params = {
                "q": product_id
            }

            search_data = SearchService.fire_search_query(search_params)
            status, response = SearchService.parse_search_results(search_data)

            if status != 200:
                abort(status, message=response)

            if response["total"] < 1:
                abort(404, message="Resource not found")

            return response["products"][0]

        return product


@blp.route("/api/products")
class ProductList(MethodView):
    """Controller class for handling requests on list of products."""
    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, ProductListSchema)
    # @cache.cached(query_string=True)
    def get(self, pagination_params):
        products, total = ProductService.find_all(pagination_params)
        if len(products) == 0:
            abort(400, message="No match found")

        response = {
            "total": total,
            "rows": pagination_params.get("rows", current_app.config['PRODUCTS_PER_PAGE']),
            "products": products
        }

        return response


@blp.route("/api/search")
class ProductSearch(MethodView):
    """Controller class for handling search requests on products."""
    @blp.arguments(SearchSchema, location="query")
    @blp.response(200, ProductListSchema)
    @cache.cached(query_string=True)
    def get(self, search_params):
        if "rows" not in search_params:
            search_params["rows"] = current_app.config["PRODUCTS_PER_PAGE"]

        search_data = SearchService.fire_search_query(search_params)
        status, response = SearchService.parse_search_results(search_data)

        if status != 200:
            abort(status, message=response)

        response["rows"] = search_params["rows"]

        return response


@blp.route("/api/products/categories/<int:category_id>")
class ProductCategory(MethodView):
    """Controller class for handling requests on products based on category type."""
    @blp.arguments(PaginationSchema, location="query")
    @blp.response(200, ProductListSchema)
    @cache.cached(query_string=True)
    def get(self, pagination_params, category_id):
        products, total = ProductService.find_by_category(category_id, pagination_params)

        if len(products) == 0:
            abort(400, message="No match found")

        response = {
            "total": total,
            "rows": pagination_params.get("rows", current_app.config['PRODUCTS_PER_PAGE']),
            "products": products
        }

        return response

# @blp.route("/api/recommend")
# class ProductRecommend(MethodView):
#     def get(self):
#         # ProductService.find_by_category(id)
#         # ProductService.find_all()
#         df=pd.DataFrame()
#         for j in range(3000):
#             k=random.randrange(1,100)
#             fixed_digits = 6
#             customerid=random.randrange(111111, 999999, fixed_digits)
#             productdesc,totalprod=ProductService.find_by_category(k, {"rows":9999})
#             fork = random.randrange(2,8)
#             for _ in range(fork):
#                 if totalprod==1:
#                     randid=1
#                 else:
#                     randid=random.randrange(1,totalprod)
#                 quantity=random.randrange(1,6)
#                 newrow={'customerid':customerid,'id':productdesc[randid-1].id,'description':productdesc[randid-1].productDescription,'Quantity':quantity}
#                 df=df.append(newrow,ignore_index=True)
#         item_lookup = df[['id', 'description']].drop_duplicates()
#         item_lookup['id'] = item_lookup.id.astype(str)
#         df['customerid'] = df.customerid.astype(float)
#         df = df[['id', 'Quantity', 'customerid']]
#         df_grouped = df.groupby(['customerid', 'id']).sum().reset_index()
#         df_grouped.Quantity.loc[df_grouped.Quantity == 0] = 1
#         df_grouped_purchased = df_grouped.query('Quantity > 0')
#         no_products = len(df_grouped_purchased.id.unique())
#         no_customers = len(df_grouped_purchased.customerid.unique())
#         print('Number of customers in dataset:', no_customers)
#         print('Number of products in dataset:', no_products)
#         ratings = df_grouped_purchased.pivot(index = 'customerid', columns='id', values='Quantity').fillna(0).astype('int')
#         ratings_binary = ratings.copy()
#         ratings_binary[ratings_binary != 0] = 1
#         products_integer = np.zeros((no_products,no_products))
#         print('Counting how many times each pair of products has been purchased...')
#         for i in range(no_products):
#             for j in range(no_products):
#                 if i != j:
#                     df_ij = ratings_binary.iloc[:,[i,j]] #create a temporary df with only i and j products as columns
#                     sum_ij = df_ij.sum(axis=1)
#                     pairings_ij = len(sum_ij[sum_ij == 2]) #if s1_ij == 2 it means that both products were purchased by the same customer
#                     products_integer[i,j] = pairings_ij
#                     products_integer[j,i] = pairings_ij
#         print('Counting how many times each individual product has been purchased...')
#         times_purchased = products_integer.sum(axis = 1)
#         print('Building weighted product matrix...')
#         products_weighted = np.zeros((no_products,no_products))
#         for i in range(no_products):
#             for j in range(no_products):
#                 if (times_purchased[i]+times_purchased[j]) !=0: #make sure you do not divide with zero
#                     products_weighted[i,j] = (products_integer[i,j])/(times_purchased[i]+times_purchased[j])
#         nodes_codes = np.array(ratings_binary.columns).astype('str')
#         item_lookup_dict = pd.Series(item_lookup.id.values,index=item_lookup.id).to_dict()
#         nodes_labels = [item_lookup_dict[code] for code in nodes_codes]
#
#         G = nx.from_numpy_matrix(products_weighted)
#         pos=nx.random_layout(G)
#         labels = {}
#         for idx, node in enumerate(G.nodes()):
#             labels[node] = nodes_labels[idx]
#         '''
#         nx.draw_networkx_nodes(G, pos , node_color="skyblue", node_size=100)
#         nx.draw_networkx_edges(G, pos,  edge_color='k', width= 0.3, alpha= 0.5)
#         nx.draw_networkx_labels(G, pos, labels, font_size=4)
#         plt.axis('off')
#         plt.show()
#         #Export Graph to Gephi
#         H=nx.relabel_nodes(G,labels) #create a new graph with Description labels and save to Gephi for visualizations
#         nx.write_gexf(H, "products.gexf")'''
#         def get_paired_color_palette(size):
#             palette = []
#             for i in range(size*2):
#                 palette.append(plt.cm.Paired(i))
#             return palette
#
# #Find communities of nodes (products)
#         louvain = community_louvian.best_partition(G, resolution = 1.5)
#         values = list(louvain.values())
#
#         communities =[]
#
#         for i in set(louvain.values()):
#             nodelist = [n for n in G.nodes if (louvain[n]==i)]
#             communities.append(nodelist)
#         '''
#         clusters_count = len(set(louvain.values()))
#         plt.figure(figsize=(10, 10))
#         light_colors = get_paired_color_palette(clusters_count)
#         dark_colors = get_paired_color_palette(clusters_count)
#         g = nx.drawing.layout.spring_layout(G, weight = 'weight')
#
# #iterate through each of the communities found by the Louvain algorithm and plot
#         for i in set(louvain.values()):
#             nodelist = [n for n in G.nodes if (louvain[n]==i)]
#             edgelist = [e for e in G.edges if ((louvain[e[0]]==i) or (louvain[e[1]]==i))]
#             node_color = [light_colors[i] for _ in range(len(nodelist))]
#             edge_color = [dark_colors[i] for _ in range(len(edgelist))]
#             nx.draw_networkx_nodes(G, g, nodelist=nodelist, node_color=node_color, edgecolors='k', label = i)
#             nx.draw_networkx_edges(G, g, edgelist=edgelist, alpha=.5, edge_color=edge_color)
# #set title, legend and show plot
#         plt.title('Communities in commodity purchase trend', fontdict={'fontsize': 25})
#         plt.legend()
#         plt.axis('off')
#         plt.show()
#         '''
#         clusters = []
#         for cluster in range(len(set(louvain.values()))):
#             cluster_list = []
#             for k, v in louvain.items():
#                 if v == cluster:
#                     cluster_list.append(k)
#             clusters.append(cluster_list)
#         louvain = clusters
#
#         '''x = ['modularity', 'coverage', 'performance']
#         y= [nx.community.modularity(G, eval('louvain')),
#         nx.community.coverage(G, eval('louvain')),
#         nx.community.performance(G, eval('louvain'))]
#         fig = plt.figure()
#         ax = fig.add_axes([0,0,1,1])
#         ax.bar(x,y)
#         plt.title('Metrics for Louvain Clustering', fontdict={'fontsize': 25})
#         plt.legend()
#         plt.show()'''
#
#         print('Number of communities:', len(np.unique(values)))
#
#         products_communities = pd.DataFrame(nodes_labels, columns = ['product_description'])
#         products_communities['community_id'] = values
#
#         products_communities[products_communities['community_id']==1].head(40)
#         products_weighted_pd = pd.DataFrame(products_weighted, columns = nodes_labels)
#         products_weighted_pd.set_index(products_weighted_pd.columns, 'product', inplace=True)
#
#         products_prob = products_weighted_pd.divide(products_weighted_pd.max(axis = 1), axis = 0)
#         products_prob.to_json('products_prob.json',orient="split")
#         return {}
@blp.route("/api/products/<string:product_id>/recommendations")
class ProductRecommend(MethodView):
    @blp.response(200, PlainProductSchema(many=True))
    # @cache.cached(query_string=True)
    def get(self, product_id):

        embeddings_filepath = os.path.join(current_app.instance_path, "embeddings.pkl")
        product_df_filepath = os.path.join(current_app.instance_path, "products_prob.json")

        tokenizer = AutoTokenizer.from_pretrained("albert-base-v2")
        model = AlbertModel.from_pretrained("albert-base-v2")
        encoder = Encoder(tokenizer, model)

        encoder.load_embeddings(embeddings_filepath)
        if encoder.embeddings_dataset is None:
            encoder.embed_dataset()
            encoder.save_embeddings(embeddings_filepath)

        scores, content_recommender_products = encoder.retrieve_nearest(product_id)

        collaborative_recommender = CollaborativeRecommender()
        collaborative_recommender.load_df(product_df_filepath)
        collaborative_recommender_products = collaborative_recommender.recommend(product_id)


        retrieved_products = []
        retrieved_products.extend(collaborative_recommender_products)
        retrieved_products.extend(content_recommender_products)

        return retrieved_products

