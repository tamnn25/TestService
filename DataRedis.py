import redis

# Connect to Redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 0  # Redis database index (default is 0)
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

# Example data to push
data = {'key1': 'value1', 'key2': 'value2', 'key3': 'value1', 'key4': 'value2'}

# Push data to Redis
for key, value in data.items():
    redis_client.set(key, value)

# Optionally, set expiration time for keys
# redis_client.expire('key1', 60)  # Expires key1 in 60 seconds

# Retrieve data from Redis (optional)
for key in data.keys():
    retrieved_value = redis_client.get(key)
    print(f"Retrieved {key}: {retrieved_value.decode('utf-8')}")

# Close Redis connection
redis_client.close()
