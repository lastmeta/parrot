import click


@click.group()
def main():
    '''display help '''


@main.command()
def help():
    '''open this file to modify'''
    print(
        'after installing this package using python setup.py develop... ')
    print(os.popen(f'explorer {os.path.dirname(os.path.abspath(__file__))}').read())


@main.command()
@click.argument('forever', type=bool, required=False, default=True)
def run(forever=True):
    ''' backsup all shares in config '''
    import time
    from parrot import config
    from parrot.lib import find_new_and_updated_files
    if not forever:
        print('running 1 time')
        for host, share in config.get('shares'):
            find_new_and_updated_files(host, share)
        return
    while True:
        print('running forever')
        for host, share in config.get('shares'):
            find_new_and_updated_files(host, share)
        time.sleep(60)
