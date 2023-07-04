from django.shortcuts import render, redirect
from products.models import get_database
from datetime import datetime


import bcrypt

# Create your views here.


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user_db = get_database("User")
        customer_col = user_db["customers"]
        admin_col = user_db["customers"]

        c_query = customer_col.find_one({"email": email})
        a_query = admin_col.find_one({"email": email})

        if c_query:
            # Verifying a password
            password_attempt = password.encode("utf-8")
            hashed_password = c_query["password"]

            if bcrypt.checkpw(password_attempt, hashed_password):
                print("Password is correct!")
                session_id = c_query["_id"]
                request.session["uid"] = str(session_id)
                # TODO: Change this redirect --DONE--
                return redirect("dashboard:user_index")
            else:
                print("Password is incorrect.")
                context = {"error_message": "Wrong Credentials"}
                return render(request, "login.html", context)

        elif a_query:
            # Verifying a password
            password_attempt = password.encode("utf-8")
            hashed_password = a_query["password"]

            if bcrypt.checkpw(password_attempt, hashed_password):
                print("Password is correct!")
                session_id = a_query["_id"]
                request.session["uid"] = str(session_id)
                return redirect("dashboard:index")
            else:
                print("Password is incorrect.")
                context = {"error_message": "Wrong Credentials"}
                return render(request, "login.html", context)

    context = {}
    return render(request, "login.html", context)


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user_db = get_database("User")
        customer_col = user_db["customers"]
        query = customer_col.find_one({"email": email})
        if query:
            context = {
                "error_message": "That email already exist, if you already have an account then log In"
            }
            return render(request, "register.html", context)

        else:
            # Hashing a password
            password = password.encode("utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            user_data = {
                "username": username,
                "email": email,
                "password": hashed_password,
                "reg_date": datetime.now(),
            }
            store_data = customer_col.insert_one(user_data)

            session_id = store_data.inserted_id
            request.session["uid"] = str(session_id)

            # TODO: change redirect to user dashboard --DONE--
            return redirect("dashboard:user_index")

    context = {}
    return render(request, "register.html", context)


# create admin accountss
def create_admin(request):
    if "uid" in request.session:
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]

            user_db = get_database("User")
            admin_col = user_db["admins"]
            query = admin_col.find_one({"email": email})
            if query:
                context = {
                    "error_message": "That email already exist, if you already have an account then log In"
                }
                return render(request, "create.html", context)

            else:
                # Hashing a password
                password = password.encode("utf-8")
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

                user_data = {
                    "username": username,
                    "email": email,
                    "password": hashed_password,
                    "reg_date": datetime.now(),
                }
                store_data = admin_col.insert_one(user_data)

                # session_id = store_data.inserted_id
                # request.session["uid"] = str(session_id)

                return redirect("accounts:admin_accounts")

        context = {}
        return render(request, "create.html", context)
    else:
        return redirect("base:login")


# Logout users
def logout(request):
    del request.session["uid"]
    return redirect("base:login")
