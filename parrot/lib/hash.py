# should save local and remote has in database and only get this if missing (upon copy)...
#localhash = hash_file_at_unc(local_path)
#remote_path = os.path.join(diretory, file)
#remotehash = hash_file_at_unc(remote_path)
#if localhash == remotehash:
#    copy_file(remote_path, local_path)


def this_file(unc_path, mode='md5'):
    ''' use modified instead, we can get that without pulling the whole file '''
    import hashlib
    h = hashlib.new(mode)
    with open(unc_path, 'rb') as file:
        data = file.read()
    h.update(data)
    digest = h.hexdigest()
    return digest
