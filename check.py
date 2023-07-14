import os
import hashlib


def hash_files(folder):
    file_hashes = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                file_contents = f.read()
                file_hash = hashlib.sha256(file_contents).hexdigest()
                file_hashes[file] = file_hash
    return file_hashes


result = hash_files('Folder1')

res_zwei = hash_files('Folder2')

for name, hash_value in result.items():
    if res_zwei[name] != hash_value:
        print('Datei anders: \t\t' + name)
