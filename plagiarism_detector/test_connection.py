from pymongo import MongoClient

# Replace 'your_connection_string_here' with your actual MongoDB connection string
client = MongoClient('mongodb+srv://afrazasher2:7GZvOCYmHiW5jnXJ@cluster0.of7qhle.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.test  # Replace 'test' with your database name if needed
print(db.list_collection_names())


from django.core.management.utils import get_random_secret_key

print(get_random_secret_key()) # =p=h^m(m+y!xtq)nl=m6=kh--t&#%=0#c1ifd78$k=-1g*4qk7



