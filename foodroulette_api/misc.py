import hashlib

def md5_hash(s):
  m = hashlib.md5()
  m.update(s)
  return m.hexdigest()