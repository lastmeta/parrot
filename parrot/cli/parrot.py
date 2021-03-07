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
def go():
    ''' contains main loop '''
    


@main.command()
@click.argument('words', type=list, nargs=-1, required=True)
def args(words):
    '''args '''
    commit = ' '.join([''.join(letters) for letters in words])
    print(os.popen(f'git commit -m "{commit}"').read())
