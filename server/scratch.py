import cachehelper

X= cachehelper.CacheProvider('192.168.88.219', 6379)
print(X.getCachedJson("a0065267-c30c-4ce8-b404-b16a432cec9d"))