from parrot.lib import database
from parrot.lib import hash


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
    try:
        shutil.copy2(
            os.path.join(remote_path),
            os.path.join(local_path))
    except PermissionError as e:
        print(e)
    return True


def get_time(unc_path, kind=None):
    ''' gets the most recent of modified or created '''
    import pathlib
    fname = pathlib.Path(unc_path)
    if fname.exists():
        if kind in ['modified', 'm', 'modify']:
            return fname.stat().st_mtime
        if kind in ['created', 'c', 'create']:
            return fname.stat().st_ctime
        if kind in ['accessed', 'a', 'access']:
            return fname.stat().st_atime
        return max([fname.stat().st_mtime, fname.stat().st_ctime])


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
