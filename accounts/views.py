from django.shortcuts import render, redirect

from products.models import get_database


# Create your views here.


def user_accounts(request):
    if "uid" in request.session:
        user_db = get_database("User")
        customer_col = user_db["customers"]
        customer_count = customer_col.count_documents({})
        query = customer_col.find()
        customer_list = []

        for cust in query:
            # product["id"] = product.pop("_id")
            date = str(cust["reg_date"]).split()[0]
            cust["reg_date"] = date
            customer_list.append(cust)

        context = {"customer_list": customer_list, "customer_count": customer_count}
        return render(request, "userAccounts.html", context)
    else:
        return redirect("base:login")


def admin_accounts(request):
    if "uid" in request.session:
        user_db = get_database("User")
        admin_col = user_db["admins"]
        admin_count = admin_col.count_documents({})
        query = admin_col.find()
        admin_list = []

        customer_col = user_db["customers"]
        customer_count = customer_col.count_documents({})
        user_count = admin_count + customer_count

        for admin in query:
            date = str(admin["reg_date"]).split()[0]
            admin["reg_date"] = date
            admin_list.append(admin)

        context = {
            "admin_list": admin_list,
            "admin_count": admin_count,
            "user_count": user_count,
        }
        return render(request, "adminAccounts.html", context)
    else:
        return redirect("base:login")


def delete_customer(request, cust_email):
    if "uid" in request.session:
        user_db = get_database("User")
        customer_col = user_db["customers"]
        del_req = customer_col.delete_one({"email": cust_email})

        return redirect("accounts:user_accounts")
    else:
        return redirect("base:login")


# def delete_admin(request, admin_email):
#     if "uid" in request.session:
#         user_db = get_database("User")
#         admin_col = user_db["admins"]
#         del_req = admin_col.delete_one({"email": admin_email})

#         return redirect("accounts:admin_accounts")
#     else:
#         return redirect("base:login")


"""
1 - email: chrisbrain89@gmail.com
    pass: ChrisBrain111
2-  email: wib237@gmail.com
    pass: Wib237
3-  email: tester@gmail.com
    pass: Tester
"""
