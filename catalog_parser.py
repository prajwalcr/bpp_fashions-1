import json

dataFile = open("out.json")

data = json.load(dataFile)

l1Categories = set()
l2Categories = set()
l2CategoriesMen = set()
l2CategoriesWomen = set()
l2CategoriesExp = set()
genders = set()

for product in data:
    if product["sku"] != product["uniqueId"]:
        print("1 wow")

    if "color" not in product:
        print("2 wow")

    if "availability" not in product:
        print("3 wow")

    # if "size" not in product:
    #     print("4 wow")
    #
    # if "productDescription" not in product:
    #     print("5 wow")
    #
    if "catlevel2Name" not in product:
        print("6 wow")
        print(product["catlevel1Name"] == "exp")
        # print("catlevel3Name" in product)
        # print("catlevel4Name" in product)
    else:
        l2Categories.add(product["catlevel2Name"])

        if product["catlevel1Name"] == "men":
            l2CategoriesMen.add(product["catlevel2Name"])
        if product["catlevel1Name"] == "women":
            l2CategoriesWomen.add(product["catlevel2Name"])
        if product["catlevel1Name"] == "exp":
            l2CategoriesExp.add(product["catlevel2Name"])

    if "productImage" not in product:
        print("7 wow")

    if "price" not in product:
        print("8 wow")

    if "catlevel1Name" not in product:
        print("9 wow")
    else:
        l1Categories.add(product["catlevel1Name"])

    if "gender" not in product:
        print("10 wow")
    else:
        for gender in product["gender"]:
            genders.add(gender)

print("l1Categories", l1Categories)
print("l2Categories", l2Categories)
print("l2CategoriesMen", sorted(list(l2CategoriesMen)))
print("l2CategoriesWomen", sorted(list(l2CategoriesWomen)))
print("l2CategoriesExp", sorted(list(l2CategoriesExp)))
print("genders", genders)


'''
color: []
availability: boolean
size: []
productDescription: string
catlevel2Name: string
title: string
productImage: string (URL)
sku: string
price: float
catlevel1Name: string
gender: []
uniqueId: string
'''