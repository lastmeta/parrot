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


def prune_empty_directories():
    import os
    root = get_backup_path()
    removed = 0
    for path, folders, files in os.walk(root):
        if len(files) == 0 and len(folders) == 0:
            print('removing', path)
            os.rmdir(path)
            removed += 1
    if removed == 0:
        return
    prune_empty_directories()
