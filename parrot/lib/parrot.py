from parrot import lib


class Parrot(object):
    """docstring for Parrot"""
    def __init__(self):
        self.backup_path = lib.get_backup_path()

    def run(self, forever=True, throttle=60):
        def run_once(throttle=60):
            import time
            for host, share in config.get('shares').items():
                lib.find_new_and_updated_files(host, share, self.backup_path)
                time.sleep(throttle)

        from parrot import config
        if not forever:
            print('running 1 time')
            run_once(0)
            return
        while True:
            print('running forever', end='\r')
            run_once(throttle)
