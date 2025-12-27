
import os
import pymongo
from dotenv import load_dotenv
import sys

load_dotenv()
uri = os.getenv('MONGODB_URI')

if not uri:
    print("MONGODB_URI missing")
    sys.exit(1)

print(f"Resolving URI: {uri}")

try:
    # Connect to get topology
    client = pymongo.MongoClient(uri)
    # Force connection
    client.admin.command('ping')
    
    # Get nodes
    nodes = client.nodes
    if not nodes:
        print("Could not resolve nodes.")
        sys.exit(1)
        
    print(f"Found nodes: {nodes}")
    
    # Construct standard URI
    # mongodb://user:pass@host1:27017,host2:27017/DbName?replicaSet=...&ssl=true
    
    # Extract credentials and options form original URI
    # This is a bit manual, but usually we can just ask pymongo.uri_parser check
    # But simpler: just construct new string from nodes + auth
    
    auth_part = uri.split('@')[0].replace('mongodb+srv://', 'mongodb://')
    
    hosts_part = ",".join([f"{n[0]}:{n[1]}" for n in nodes])
    
    # Safe param injection
    params = "ssl=true&replicaSet=atlas-xdduwtq-shard-0&authSource=admin&retryWrites=true&w=majority"
    
    new_uri = f"{auth_part}@{hosts_part}/SmartEducation?{params}"
    
    print("\nSUGGESTED RESOLVED URI:")
    print(new_uri)
    
    # We can also just update .env directly
    
except Exception as e:
    print(e)
