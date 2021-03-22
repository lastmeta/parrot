import os
import time
import pandas as pd
from parrot import lib
from parrot import config

class Parrot(object):
    """docstring for Parrot"""
    def __init__(self):
        self.backup_path = lib.get_backup_path()
        self.allow_duplicates = lib.get_allow_duplicates()
        self.database = lib.database.get()
        self.key, self.schema = lib.database.get_key_schema(self.database)
        self.save_flag = False

    def save(self):
        if self.save_flag:
            print('saving', self.database.shape[0])
            lib.database.save(self.database)
            self.save_flag = False

    def run(self, forever=True, throttle=60):
        def run_once(throttle=60):
            for host, share in config.get('shares').items():
                print('                                            ', end='\r')
                print('contacting:', host, share, end='\r')
                #try:
                self.find_new_and_updated_files(host, share)
                #except Exception as e:
                #    print(host, share, 'unreachable:', e)
                self.save()
                time.sleep(throttle)

        if not forever:
            print('running 1 time')
            run_once(0)
            return
        print('running forever')
        while True:
            run_once(throttle)

    def find_new_and_updated_files(self, host: str, share: str):
        ''' backup should have a folder for each host, and backup folder '''
        def create_folders(folders):
            for folder in folders:
                if not os.path.exists(os.path.join(local_root, path_folders, folder)):
                    print('creating folder:', os.path.join(local_root, path_folders, folder))
                    os.mkdir(os.path.join(local_root, path_folders, folder))

        def create_files(files):
            def remote_is_newer(local_path, remote_time):
                # notice a feature: if you change a modify a file locally it is
                # not overridden until the remote source is modified again
                local_time = lib.get_time(unc_path=local_path)
                return remote_time > local_time

            def remote_newer_that_removed(local_path, remote_time):
                '''
                see if its remove modified time is newer than the database
                timestamp and if it is return True, if it is not in the
                database return True, else return False
                '''
                return remote_time > self.database[
                    self.database[self.key]==local_path.replace('\\','\\\\')
                ]['timestamp'].iloc[0] or 0

            def copy_and_record(remote_path, local_path):
                self.save_flag = True
                lib.copy_file(remote_path, local_path)
                local_hash = lib.hash.this_file(unc_path=local_path)
                self.database = lib.database.upsert(
                    database=self.database,
                    record={
                        self.key: local_path.replace('\\', '\\\\'),
                        'hash': local_hash,
                        'removed': False,
                        'created': time.time(),
                        'timestamp': time.time()})
                self.remove_older_duplicates(local_path, local_hash)

            for file in files:
                remote_path = os.path.join(directory, file)
                local_path = os.path.join(local_root, path_folders, file)
                try:
                    remote_time = lib.get_time(unc_path=remote_path)
                except OSError as e:
                    remote_time = 0
                if os.path.exists(local_path):
                    if remote_is_newer(local_path, remote_time):
                        copy_and_record(remote_path, local_path)
                else:
                    if local_path.replace('\\','\\\\') in self.database[self.key].values.tolist():
                        if remote_newer_that_removed(local_path, remote_time):
                            copy_and_record(remote_path, local_path)
                    else:
                        copy_and_record(remote_path, local_path)

        remote_root = f'//{host}/{share}'
        os.makedirs(os.path.join(self.backup_path, host, share), exist_ok=True)
        local_root = os.path.join(self.backup_path, host, share)
        for directory, folders, files in os.walk(remote_root):
            path_folders = '\\'.join([x for x in directory.split(remote_root)[-1].split('\\') if x])
            create_folders(folders)
            create_files(files)

    def remove_older_duplicates(self, local_path, local_hash):
        ''' remove older duplicates '''
        if self.allow_duplicates:
            return
        duples = self.database[
            (self.database['removed']==False)&
            (self.database[self.key]!=local_path.replace('\\', '\\\\'))&
            (self.database['hash']==local_hash)]
        for ix, duple in duples.iterrows():
            print('removing file', duple[self.key])
            if os.path.exists(duple[self.key]):
                try:
                    os.remove(duple[self.key])
                except PermissionError as e:
                    print('unable to delete', duple[self.key], 'due to PermissionError:', e)
            self.save_flag = True
            self.database = lib.database.upsert(
                database=self.database,
                record={
                    **{k: duple[k] for k in self.schema},
                    **{'removed': True, 'timestamp': time.time()}})
