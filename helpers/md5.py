import hashlib

def md5_string_hash(input_str):
    m = hashlib.md5()
    m.update(input_str.encode('utf-8'))
    return m.hexdigest()