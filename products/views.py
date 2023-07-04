from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages

# from django.core.files.uploadedfile import InMemoryUploadedFile


# from django.core.files.images import ImageFile

import ast
import csv
import pandas as pd

from .models import get_database
from .helper_func import read_csv_data, store_image

# Create your views here.


def index(request):
    # check if user is logged in
    if "uid" in request.session:
        product_db = get_database("Products")
        product_col = product_db["products"]
        temp_product_list = product_col.find()
        product_count = product_col.count_documents({})
        out_stock = product_col.count_documents({"quantity": 0})
        in_stock = product_count - out_stock

        product_list = []
        total_price = 0
        for product in temp_product_list:
            # product["id"] = product.pop("_id")
            product_list.append(product)
            total_price += float(product["price"]["USD"])

        total_price = round(total_price, 2)
        context = {
            "product_list": product_list,
            "product_count": product_count,
            "out_stock": out_stock,
            "in_stock": in_stock,
            "total_price": total_price,
        }
        return render(request, "index.html", context)
    else:
        return redirect("base:login")


def user_index(request):
    if "uid" in request.session:
        user_db = get_database("User")
        customer_col = user_db["customers"]
        temp_ = customer_col.find()

        product_purchased_list = []
        qty_purchased_list = []
        data_list = []
        total_spent = 0
        pp_count = 0
        print(request.session["uid"])
        for temp in temp_:
            print(temp["_id"])
            print(temp)
            if (str(temp["_id"]) == str(request.session["uid"])) and (
                "product_purchased" in temp
            ):
                print("in")
                product_purchased_list = temp["product_purchased"]
                qty_purchased_list = temp["qty_purchased"]

                product_purchased_list = ast.literal_eval(product_purchased_list)
                qty_purchased_list = ast.literal_eval(qty_purchased_list)
        print(product_purchased_list)

        if len(product_purchased_list) > 0:
            pp_count = len(product_purchased_list)
            total_spent = 0
            for i in product_purchased_list:
                product_db = get_database("Products")
                products_col = product_db["products"]
                _prd = products_col.find_one({"name": i})
                if _prd:
                    print("_prod gotten")
                    price_ = float(_prd["price"]["USD"])
                    price_ = round(price_, 2)

                    total = price_ * int(
                        qty_purchased_list[product_purchased_list.index(i)]
                    )
                    total_spent += total

                    data = {
                        "name": _prd["name"],
                        "image": _prd["image"],
                        "short_description": _prd["short_description"],
                        "description": _prd["description"],
                        "price": _prd["price"]["USD"],
                        "qty_bought": qty_purchased_list[
                            product_purchased_list.index(i)
                        ],
                        "total": total,
                    }
                    data_list.append(data)
        request.session["products"] = data_list

        context = {
            "pp_count": pp_count,
            "total_spent": total_spent,
            "data_list": data_list,
        }
        return render(request, "user_index.html", context)
    else:
        return redirect("base:login")


# {"USD": "11.99","XAF": "7000","EUR": "10.98","JPY": "1682.97","GBP": "9.98"}


def download_csv(request):
    # Define your data as a list of dictionaries
    if "uid" in request.session:
        data = []

        product_db = get_database("Products")
        product_col = product_db["products"]
        all_products = product_col.find()

        for product in all_products:
            data.append(product)

        # Create a response object with CSV content type and attachment
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="products.csv"'

        # Write the data to the response as a CSV file
        writer = csv.DictWriter(response, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

        return response
    else:
        return redirect("base:login")


def download_excel(request):
    if "uid" in request.session:
        # Define your data as a list of dictionaries
        data = []

        product_db = get_database("Products")
        product_col = product_db["products"]
        all_products = product_col.find()

        for product in all_products:
            data.append(product)

        # Create a Pandas DataFrame from the data
        df = pd.DataFrame(data)

        # Create a response object with Excel content type and attachment
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="products.xlsx"'

        # Write the DataFrame to the response as an Excel file
        df.to_excel(response, index=False)

        return response
    else:
        return redirect("base:login")


# for the user dashboard to download csv


def user_download_csv(request):
    # Define your data as a list of dictionaries
    if "uid" in request.session:
        data = []
        product_list = request.session["products"]
        data = product_list
        # product_purchased_list = ast.literal_eval(product_purchased_list)

        # Create a response object with CSV content type and attachment
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="products.csv"'

        # Write the data to the response as a CSV file
        writer = csv.DictWriter(response, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

        return response
    else:
        return redirect("base:login")


def user_download_excel(request):
    if "uid" in request.session:
        # Define your data as a list of dictionaries
        data = []
        product_list = request.session["products"]
        data = product_list

        # Create a Pandas DataFrame from the data
        df = pd.DataFrame(data)

        # Create a response object with Excel content type and attachment
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="products.xlsx"'

        # Write the DataFrame to the response as an Excel file
        df.to_excel(response, index=False)

        return response
    else:
        return redirect("base:login")


def add_products(request):
    if "uid" in request.session:
        if request.method == "POST":
            manually = True
            try:
                name = request.POST["productName"]
                price_usd = request.POST["price_usd"]
                price_xaf = request.POST["price_usd"]
                price_gbp = request.POST["price_gbp"]
                price_euro = request.POST["price_eur"]
                price_jpy = request.POST["price_jpy"]
                quantity = request.POST["quantity"]
                img_file = request.FILES["image"]
                print(f"frst {img_file}")
                description = request.POST["description"]
                short_description = str(description)[:171]

            except:
                csv_file = request.FILES["csv_file"]
                manually = False

            if manually:
                # check if product with such name exists
                print("get db")
                product_db = get_database("Products")
                product_col = product_db["products"]
                find_product = product_col.find_one({"name": name})
                print("nter try")
                try:
                    if find_product:
                        print("if part")
                        context = {
                            "error_message": "Product with such name already exist"
                        }
                        return render(request, "add-products.html", context)

                    else:
                        print("else part")
                        print(f"frst {img_file}")
                        resp, ext = store_image(img_file, name)
                        if resp:
                            product_data = {
                                "name": name,
                                "image": f"/products/{name}.{ext}",
                                "description": description,
                                "short_description": short_description,
                                "quantity": quantity,
                                "price": {
                                    "USD": price_usd,
                                    "XAF": price_xaf,
                                    "GBP": price_gbp,
                                    "EUR": price_euro,
                                    "JPY": price_jpy,
                                },
                            }
                            print("inserting")
                            store_data = product_col.insert_one(product_data)
                            context = {
                                "success_message": "Your Product has successfully been created"
                            }
                            return render(request, "add-products.html", context)
                        else:
                            context = {
                                "error_message": "File uploaded must be an Image"
                            }
                            return render(request, "add-products.html", context)
                except Exception as e:
                    print(e)
                    context = {"error_message": "Something went wrong, Try again"}
                    return render(request, "add-products.html", context)

            else:
                resp, data = read_csv_data(csv_file)
                if resp and (len(data) > 0):
                    print(data)
                    # print(resp)
                    product_db = get_database("Products")
                    product_col = product_db["products"]
                    in_prods = []
                    for d in data:
                        short_description = str(d[1])[:171]

                        resp_1, ext = store_image(d[2], d[0], from_string=True)
                        prices = ast.literal_eval(d[4])
                        if resp_1:
                            product_data = {
                                "name": d[0],
                                "image": f"/products/{d[0]}.{ext}",
                                "description": d[1],
                                "short_description": short_description,
                                "quantity": d[3],
                                "price": {
                                    "USD": prices[0],
                                    "XAF": prices[1],
                                    "GBP": prices[2],
                                    "EUR": prices[3],
                                    "JPY": prices[4],
                                },
                            }
                            in_prods.append(product_data)
                            # TODO: do and else statement to log any product that isnt uploaded

                    product_col.insert_many(in_prods)
                    context = {
                        "success_message": "Your Product has successfully been created"
                    }
                    return render(request, "add-products.html", context)
                else:
                    print(resp, data)
                    context = {
                        "error_message": "Uploaded File Must be a CSV and must have atleast 1 product"
                    }
                    return render(request, "add-products.html", context)

        context = {}
        return render(request, "add-products.html", context)

    else:
        return redirect("base:login")


def delete_product(request, product_name):
    if "uid" in request.session:
        print(product_name)
        product_db = get_database("Products")
        product_col = product_db["products"]
        del_req = product_col.delete_one({"name": product_name})

        return redirect("dashboard:index")
    else:
        return redirect("base:login")


def update_product(request, product_name):
    if "uid" in request.session:
        if request.method == "POST":
            manually = True
            try:
                name = request.POST["productName"]
                price_usd = request.POST["price_usd"]
                price_xaf = request.POST["price_usd"]
                price_gbp = request.POST["price_gbp"]
                price_euro = request.POST["price_eur"]
                price_jpy = request.POST["price_jpy"]
                quantity = request.POST["quantity"]
                img_file = request.FILES["image"]
                print(f"frst {img_file}")
                description = request.POST["description"]
                short_description = str(description)[:171]

            except Exception as e:
                pass

            if manually:
                # check if product with such name exists
                print("get db")
                product_db = get_database("Products")
                product_col = product_db["products"]
                find_product = product_col.find_one({"name": name})
                print("nter try")
                try:
                    if find_product:
                        request.session[
                            "update_fail"
                        ] = "Product with such name already exist"

                        return redirect("dashboard:edit_product", product_name)

                    else:
                        print("else part")
                        print(f"frst {img_file}")
                        resp, ext = store_image(img_file, name)
                        if resp:
                            product_data = {
                                "name": name,
                                "image": f"/products/{name}.{ext}",
                                "description": description,
                                "short_description": short_description,
                                "quantity": quantity,
                                "price": {
                                    "USD": price_usd,
                                    "XAF": price_xaf,
                                    "GBP": price_gbp,
                                    "EUR": price_euro,
                                    "JPY": price_jpy,
                                },
                            }
                            new_update = {"$set": product_data}
                            print("inserting")
                            store_data = product_col.update_one(
                                {"name": product_name}, new_update
                            )
                            request.session[
                                "update_success"
                            ] = "Your Product has successfully been updated"
                            print(f"Name: {name}")

                            return redirect("dashboard:edit_product", name)

                        else:
                            request.session[
                                "update_fail"
                            ] = "File uploaded must be an Image"

                            return redirect("dashboard:edit_product", product_name)
                except Exception as e:
                    print(e)
                    request.session["update_fail"] = "Something went wrong, Try again"

                    return redirect("dashboard:edit_product", product_name)
    else:
        return redirect("base:login")


def edit_product(request, product_name):
    if "uid" in request.session:
        product_db = get_database("Products")
        product_col = product_db["products"]
        query = product_col.find_one({"name": product_name})
        message = None
        if "update_success" in request.session:
            message = request.session["update_success"]
            del request.session["update_success"]
            messages.success(request, message)
        elif "update_fail" in request.session:
            message = request.session["update_fail"]
            del request.session["update_fail"]
            messages.error(request, message)

        context = {"query": query}
        print(query)
        return render(request, "edit-products.html", context)
    else:
        return redirect("base:login")
