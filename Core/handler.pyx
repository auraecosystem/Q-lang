def dax_handler(data):
    return {"learned": "dax format", "data": data}

plugins.register(".dax", dax_handler)
