from pymongo import MongoClient

# Use the exact non-SRV connection string that bypasses the DNS bug!
MONGO_URI = "mongodb://keoteakash:Akash%40db123@cluster0-shard-00-00.jl5jf.mongodb.net:27017,cluster0-shard-00-01.jl5jf.mongodb.net:27017,cluster0-shard-00-02.jl5jf.mongodb.net:27017/subsidy_db?ssl=true&replicaSet=atlas-13g8ac-shard-0&authSource=admin&retryWrites=true&w=majority"

def upload_to_mongodb(scheme_data):
    if not scheme_data:
        return
        
    try:
        print(f"🚀 Uploading '{scheme_data.get('title')}' to MongoDB...")
        client = MongoClient(MONGO_URI)
        db = client['subsidy_db']
        collection = db['subsidies']
        
        # Check if scheme already exists to prevent duplicates
        exists = collection.find_one({"title": scheme_data.get("title")})
        if exists:
            print(f"⚠️ Scheme '{scheme_data.get('title')}' already exists in DB. Skipping.")
        else:
            collection.insert_one(scheme_data)
            print(f"✅ Successfully added to Database!")
            
    except Exception as e:
        print(f"❌ Database Upload Failed: {e}")
    finally:
        client.close()
