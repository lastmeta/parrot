import click


@click.group()
def main():
    '''display help '''


@main.command()
def help():
    '''open this file to modify'''
    print('after installing this package using python setup.py develop... ')
    print(os.popen(f'explorer {os.path.dirname(os.path.abspath(__file__))}').read())


@main.command()
@click.argument('forever', type=bool, required=False, default=True)
@click.argument('throttle', type=int, required=False, default=60)
def run(forever=True, throttle=60):
    ''' backsup all shares in config '''
    from parrot.lib.parrot import Parrot
    Parrot().run(forever, throttle)


@main.command()
def prune():
    ''' removes all empty directories in the backup location '''
    from parrot.lib import prune_empty_directories
    prune_empty_directories()
