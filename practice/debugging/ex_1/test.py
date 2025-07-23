"""

SET K1 V1
GET K1
[V1]

"""

cache = {}
t_cache = {} 
history = []
commit_count = 0

print("Cache: {cache}")

def _set(key, value):
    cache[str(key)] = str(value)

def _get(key):
    return cache[str(key)]

_set("k1","v1")
print(_get("k1"))
_set("k1","v2")
print(_get("k1"))
_set("k1","v1")
print(_get("k1"))


"""BRC"""

def _begin():
    t_cache = cache.copy()
    print(f"Temp Cache: {t_cache}")
    history.append(t_cache)
    print(f"Printing History: {history}, {len(history)}")

def _rollback():
    global cache
    print(f"Current Cache: {cache}")
    print(f"Previous Cache: {history[0]}")
    t_cache_two = cache.copy()
    print(f" Pop: {history[-1]}")
    cache = dict(history.pop())
    print(f"Length of history: {len(history)}")
    print(f"Backed up cache: {t_cache_two}")
    print(f"New Cache: {cache}")

    #cache = history[-1]
    #history.pop()

def _commit():
    #commit_count-=1
    history.pop()

_set("k1","v1")
_set("k2","v2")
_begin()
_set("k3","v3")
_set("k4","v4")
_set("k5","v5")
#print(cache)
_rollback()
#print(cache)



