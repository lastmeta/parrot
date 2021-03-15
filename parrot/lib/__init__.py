def get_backup_path():
    from parrot import config
    bk_path = config.get().get('backup path', 'default')
    if bk_path == 'default':
        return config.root('..', 'backup')
    else:
        return bk_path


def get_allow_duplicates():
    from parrot import config
    return config.get().get('allow duplicates', True)


def find_new_and_updated_files(host: str, share: str, backup_path: str, allow_duplicates: bool = True):
    ''' backup should have a folder for each host, and backup folder '''
    import os
    remote_root = f'//{host}/{share}'
    os.makedirs(os.path.join(backup_path, host, share), exist_ok=True)
    local_root = os.path.join(backup_path, host, share)
    for directory, folders, files in os.walk(remote_root):
        path_folders = '\\'.join([x for x in directory.split(remote_root)[-1].split('\\') if x])
        for folder in folders:
            if not os.path.exists(os.path.join(local_root, path_folders, folder)):
                print('creating folder:', os.path.join(local_root, path_folders, folder))
                os.mkdir(os.path.join(local_root, path_folders, folder))
        for file in files:
            remote_path = os.path.join(directory, file)
            local_path = os.path.join(local_root, path_folders, file)
            if os.path.exists(local_path):
                # notice a feature: if you change a modify a file locally it is
                # not overridden until the remote source is modified again
                local_time = get_time(unc_path=local_path, kind='modified')
                remote_time = get_time(unc_path=remote_path, kind='modified')
                if remote_time > local_time:
                    copy_file(remote_path, local_path)
                    #check_for_duplicate(local_path, allow_duplicates)
            else:
                copy_file(remote_path, local_path)
                #check_for_duplicate(local_path, allow_duplicates)


def check_for_duplicate(local_path, allow_duplicates):
    '''
    this is logic to decide if we should delete this file. Its not finished,
    it wont work as designed, we need to add more logic to make sure it works
    right, everytime we copy a file we have to add an entry saying we copied
    that file, then modify that entry if we find it is a duplicate, saying we
    removed it, and we should remove it, and the timestamp at now. then if the
    file is ever modified we can compare the modificaiton dates, if it is after
    the timestamp in the database we can try it again, but if it already exists
    in the database we don't want to make a new record, basically we now need
    database crud logic which is beyond the scope at this time. and if we do
    implement, maybe we should just use a sql database rather than a csv,
    although, that doesn't help us much because sqlite is also in-memory so...
    its whatever, we'll implement this later.
    '''
    import pandas as pd
    if not allow_duplicates:
        # hash the file at the path
        from parrot.lib import hash
        local_hash = hash.this_file(unc_path=local_path)
        # look up the hash in the database
        df = get_database()
        # if the file is a duplicate...
        if local_hash in df[df['removed']=='False']['hash'].values.tolist():
            # ...remove it from the filesystem
            os.remove(local_path)
            # ...add an entry for that path in the database with timestamp
            df2 = pd.DataFrame(
                [[local_path, local_hash, str(dt.datetime.now()), 'True']],
                columns=['local_path', 'local_hash', 'timestamp', 'removed'])
            pd.concat([df2, df])
            # .......Also, modify the comparison logic in previous function to avoid copy if in database and mtime before database timestamp
        pass


def get_database():
    ''' database can just be a csv for now '''
    from parrot import config
    import pandas as pd
    df = pd.read_csv(config.root('database', 'database.csv'))
    return df

def copy_file(remote_path, local_path):
    import os
    import shutil
    print('copying file:', local_path)
    shutil.copy2(
        os.path.join(remote_path),
        os.path.join(local_path))
    return True


def get_time(unc_path, kind='modified'):
    import pathlib
    fname = pathlib.Path(unc_path)
    if fname.exists():
        if kind in ['modified', 'm', 'modify']:
            return fname.stat().st_mtime
        if kind in ['created', 'c', 'create']:
            return fname.stat().st_ctime
        if kind in ['accessed', 'a', 'access']:
            return fname.stat().st_atime
        print('unknown kind:', kind, 'using "modified"')
        return fname.stat().st_mtime
