def copy_file(
    machine,
    shared_folder, filepath,
    bk_folder, bk_filepath,
    user, password
):
    networkpath = r'\\' + f'{machine}' + r'\'+ f'{shared_folder}'
    command = 'NET USE ' + networkpath + ' /User:' + user + ' ' + password
    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    import shutil
    shutil.copy2(
        os.path.join(networkpath + filepath),
        os.path.join(bk_folder + bk_filepath))
    # verify
    return True


def hash_file(
    machine,
    shared_folder, filepath,
    bk_folder, bk_filepath,
    user, password,
    mode='md5'
):
    import hashlib
    h = hashlib.new(mode)
    networkpath = r'\\' + f'{machine}' + r'\'+ f'{shared_folder}'
    with open(os.path.join(networkpath + filepath), 'rb') as file:
        data = file.read()
    h.update(data)
    digest = h.hexdigest()
    return digest

def check_hash():
    '''
    if has of remote file does not match database then copy file
    hash backup file, verify it was the same, and save hash in database.
    '''


def database():
    ''' put and get information about all files copied. '''
    from pandas as pd
    from parrot import config
    pd.read_pickle(config.root('..', 'database', 'table.pkl'))
    '''
    machine, share, filepath, discovered, modified, backedup, destination, hash
    something like that
    '''



# main loop
