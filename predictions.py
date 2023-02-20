import json

with open('products_prob.json') as f:
   products_prob = json.load(f)

index=products_prob['columns'].index('00103086')

ratings=products_prob['data']
indexratings=[]
for i in ratings:
    indindexratings=[]
    for j in range(len(i)):
        indindexratings.append([i[j],j])
    indexratings.append(indindexratings)
s=indexratings[index]
sorte=sorted(s,key=lambda x:x[0],reverse=True)
no_of_suggestions=5
pred=sorte[:no_of_suggestions]
finalpred=[]
for i in pred:
    finalpred.append(products_prob['columns'][i[1]])
print(finalpred)

'''
basket = ['The contrast between the plastic frames and metal brow bar gives these sunglasses a sleek look you can wear with confidence.']
#Select the number of relevant items to suggest
no_of_suggestions = 3

all_of_basket = products_prob[basket]
all_of_basket = all_of_basket.sort_values(by = basket, ascending=False)
suggestions_to_customer = list(all_of_basket.index[:no_of_suggestions])

print('You may also consider buying:', suggestions_to_customer)'''