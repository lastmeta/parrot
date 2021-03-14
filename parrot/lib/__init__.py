def get_backup_path():
    from parrot import config
    bk_path = config.get()['backup path']
    if bk_path == 'default':
        return config.root('..', 'backup')
    else:
        return bk_path


def find_new_and_updated_files(host: str, share: str, backup_path: str):
    ''' backup should have a folder for each host, and backup folder '''
    import os
    remote_root = f'//{host}/{share}'
    #if not os.path.exists(backup_path):

    os.makedirs(os.path.join(backup_path), exist_ok=True)
    local_root = os.path.join(backup_path, host, share)
    for directory, folders, files in os.walk(remote_root):
        path_folders = directory.split(remote_root)[-1]
        print('lr', local_root, path_folders, directory)
        for folder in folders:
            print('f',folder,os.path.join(local_root, path_folders, folder))
            if not os.path.exists(os.path.join(local_root, path_folders, folder)):
                print(os.path.join(local_root, path_folders, folder))
                os.mkdir(os.path.join(local_root, path_folders, folder))
        for file in files:
            local_path = os.path.join(local_root, path_folders, file)
            if os.path.exists(local_path):
                # notice a feature: if you change a modify a file locally it is
                # not overridden until the remote source is modified again
                local_time = get_time(unc_path=local_path, kind='modified')
                remote_time = get_time(unc_path=remote_path, kind='modified')
                if remote_time > local_time:
                    copy_file(remote_path, local_path)


def copy_file(remote_path, local_path):
    import os
    import shutil
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
