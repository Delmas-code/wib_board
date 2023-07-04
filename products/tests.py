from django.test import TestCase

# Create your tests here.
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)
# import ast


# def convert_string_to_list(string_list):
#     # Use ast.literal_eval to safely evaluate and convert the string to a list
#     python_list = ast.literal_eval(string_list)

#     return python_list


# st = "[1,2,3,4,5]"
# con = convert_string_to_list(st)
# print(con)
# from products.models import get_database


# product_db = get_database("Products")
# product_col = product_db["products"]
# product_list = product_col.find()

# for i in range(1):
#     print(product_list[i])


d = {"product_purchased": "['Mokaset','Sneaker Shoes']", "qty_purchased": "[7,3]"}
if "product_purchased" in d:
    print("in")
else:
    print("out")
