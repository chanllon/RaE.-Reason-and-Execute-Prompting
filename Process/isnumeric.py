
# def is_numeric(data):
#     if data is None:
#         return False
#     if isinstance(data, tuple):
#         return False
#     if isinstance(data, list):
#         return False
#     if type(data)=='list':
#         return is_numeric(data[0])
#     try:
#         float(data)
#         return float(data)
#     except ValueError:
#         return False

def is_numeric(data):
    if isinstance(data, (str, int, float)):
        try:
            float(data)
            return float(data)
        except ValueError:
                return False
    else:
        return False