from PIL import Image
from pathlib import Path
import os
import csv

from django.core.files import File
from django.http import HttpRequest


def read_csv_data(file):
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Specify the folder where you want to store the image
    folder_path = os.path.join(BASE_DIR, "media/files")
    print("filepart 1")
    # Generate a unique file name
    df_file_name = file.name
    extension = str(df_file_name).split(".")[-1]
    data = []
    print(extension)
    if extension == "csv":
        # Combine the folder path and file name
        file_path = os.path.join(folder_path, df_file_name)
        print("filepart 2")
        # Save the file to the specified folder
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        try:
            with open(file_path, "r") as csv_f:
                reader = csv.reader(csv_f)
                # Skip the header row if needed
                next(reader)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print("File not found!")

        print("filepart 3")
        print("leave read_csv_data")
        return True, data
    else:
        return False, data


def is_image(file, from_string=False):
    print("in is_image")
    try:
        if from_string:
            with open(file, "rb") as file:
                file_ = File(file)
                # Open the file using PIL's Image module
                img = Image.open(file_)
                img.verify()  # Verify the image data

                # Check if the file format is supported (e.g., JPEG, PNG)
                supported_formats = ("JPEG", "PNG", "GIF")
                if img.format not in supported_formats:
                    return False

                # Additional checks can be performed, like checking the dimensions, file size, etc.
                print("leave is_image")
                return True

        else:
            # Open the file using PIL's Image module
            img = Image.open(file)
            img.verify()  # Verify the image data

            # Check if the file format is supported (e.g., JPEG, PNG)
            supported_formats = ("JPEG", "PNG", "GIF")
            if img.format not in supported_formats:
                return False

            # Additional checks can be performed, like checking the dimensions, file size, etc.
            print("leave is_image")
            return True
    except (IOError, SyntaxError):
        print("here")
        return False


def store_image(file, file_name, from_string=False):
    print("in store_image")
    # Verify if the file is an image
    is_an_image = is_image(file, from_string)
    if is_an_image:
        BASE_DIR = Path(__file__).resolve().parent.parent

        # Specify the folder where you want to store the image
        folder_path = os.path.join(BASE_DIR, "media/products")
        print("aprt 1")
        # Generate a unique file name
        if from_string:
            with open(file, "rb") as file:
                file_ = File(file)

                df_file_name = file_.name
                extension = str(df_file_name).split(".")[-1]
                file_name_ = f"{file_name}.{extension}"

                # Combine the folder path and file name
                file_path = os.path.join(folder_path, file_name_)
                print("aprt 2")
                # Save the file to the specified folder
                with open(file_path, "wb+") as destination:
                    for chunk in file_.chunks():
                        destination.write(chunk)
                print("aprt 3")
                print("leave store_image")
                return True, extension

        else:
            df_file_name = file.name
            extension = str(df_file_name).split(".")[-1]
            file_name_ = f"{file_name}.{extension}"

            # Combine the folder path and file name
            file_path = os.path.join(folder_path, file_name_)
            print("aprt 2")
            # Save the file to the specified folder
            with open(file_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            print("aprt 3")
            print("leave store_image")
            return True, extension
    else:
        print("leave store_image")
        return False, None


def string_to_file_link(string):
    # Create a dummy request object
    request = HttpRequest()

    # Set the current domain and protocol for the request
    request.META["HTTP_HOST"] = "example.com"
    request.META["wsgi.url_scheme"] = "http"  # or 'https' if using HTTPS

    # Construct the absolute URI using the string
    file_link = request.build_absolute_uri(string)

    return file_link
