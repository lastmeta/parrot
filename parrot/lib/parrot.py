from parrot import lib


class Parrot(object):
    """docstring for Parrot"""
    def __init__(self):
        self.backup_path = lib.get_backup_path()
        self.allow_duplicates = lib.get_allow_duplicates()

    def run(self, forever=True, throttle=60):
        def run_once(throttle=60):
            import time
            for host, share in config.get('shares').items():
                print('contacting:', host, share, end='\r')
                #try:
                lib.find_new_and_updated_files(host, share, self.backup_path, self.allow_duplicates)
                #except Exception as e:
                #    print(host, share, 'unreachable:', e)
                time.sleep(throttle)

        from parrot import config
        if not forever:
            print('running 1 time')
            run_once(0)
            return
        print('running forever')
        while True:
            run_once(throttle)
