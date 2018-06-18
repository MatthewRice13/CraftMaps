#! /usr/bin/python3
print("Running File...\n")
from django.db import connection
print (connection.queries)