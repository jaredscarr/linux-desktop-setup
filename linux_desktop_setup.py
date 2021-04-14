#!/usr/bin/python3
'''
Script for setting up my linux desktop applications and tools.
Run with sudo python3 linux_desktop_setup.py
'''
import os
import subprocess
import sys

# TODO: zoom, slack


def update_and_upgrade():
    '''Run update and upgrade commands.'''
    subprocess.run(['apt-get', 'update'])
    subprocess.run(['apt-get', 'upgrade'])


def install_dependencies():
    '''A pile of dependencies for everything lumped together to avoid rentering password everytime.'''
    # pyenv
    subprocess.run([
        'apt-get', 'install', '--no-install-recommends', 'make', 'build-essential', 'libssl-dev', 'zlib1g-dev', 'libbz2-dev',
        'libreadline-dev', 'libsqlite3-dev', 'wget', 'curl', 'llvm', 'libncurses5-dev', 'xz-utils', 'tk-dev', 'libxml2-dev',
        'libxmlsec1-dev', 'libffi-dev', 'liblzma-dev'
    ])

    # Sublime
    subprocess.run(['apt-get', 'install', 'dirmngr', 'gnupg', 'apt-transport-https', 'ca-certificates', 'software-properties-common'])
    # Git
    subprocess.run(['apt-get', 'install', 'git'])


def configure_git(user_name, github_user_email):
    '''Install git and configure user.'''
    subprocess.run(['git', 'config', '--global', 'user.name', f'{user_name}'])
    subprocess.run(['git', 'config', '--global', 'user.email', f'{github_user_email}'])


def get_sublimetext_3(user_name):
    '''Install SublimeText3.'''
    base_path = os.path.expanduser(f'~{user_name}')
    subprocess.run(['wget', '-qO', '-','https://download.sublimetext.com/sublimehq-pub.gpg', '|', 'apt-key', 'add', '-'])
    subprocess.run(['echo', '"deb https://download.sublimetext.com/ apt/stable/"', '|', 'tee', '/etc/apt/sources.list.d/sublime-text.list'])
    subprocess.run(['apt-get', 'install', 'sublime-text'])

    # Install Package Control
    package_control_destination_path = os.path.join(base_path, '.config/sublime-text-3/Installed Packages/')
    subprocess.run(['wget', 'https://packagecontrol.io/Package%20Control.sublime-package', '-P', package_control_destination_path])

    # Add User configuration to User directory
    user_config_destination_path = os.path.join(base_path, '.config/sublime-text-3/Packages/User')
    subprocess.run(['cp', '-r', 'User/.', user_config_destination_path])


def get_flake8():
    '''Install flake8 package for python linting.'''
    subprocess.run(['apt-get', 'install', '-y', 'flake8'])


def get_pyenv_and_virtualenv(user_name):
    '''Install pyenv.'''
    subprocess.run(['git', 'clone', 'https://github.com/pyenv/pyenv.git', '~/.pyenv'])
    pyenv_root_path = os.environ['PYENV_ROOT']
    full_path = os.path.join(pyenv_root_path, 'plugins/pyenv-virtualenv')
    subprocess.run(['git', 'clone', 'https://github.com/pyenv/pyenv-virtualenv.git', full_path])


def get_direnv():
    '''Install direnv.'''
    subprocess.run(['apt-get', 'install', '-y', 'direnv'])


def get_protonvpn():
    '''Install protonvpn-cli.'''
    subprocess.run(['wget', '-q', '-O', '-', 'https://repo.protonvpn.com/debian/public_key.asc', '|', 'apt-key', 'add', '-'])
    subprocess.run(['add-apt-repository', 'deb https://repo.protonvpn.com/debian unstable main'])
    update_and_upgrade()
    subprocess.run(['apt-get', 'install', 'protonvpn'])


def bashrc_updates(user_name):
    '''Add all necessary bashrc updates.'''
    file_path = os.path.join(os.path.expanduser(f'~{user_name}'), '.bashrc')

    with open(file_path, 'a') as f:
        subprocess.run(['echo', 'export PYENV_ROOT="$HOME/.pyenv"'], stdout=f, check=True)
        subprocess.run(['echo', 'export PATH="$PYENV_ROOT/bin:$PATH"'], stdout=f, check=True)
        subprocess.run(['echo', '-e', '\nif command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi'], stdout=f, check=True)
        subprocess.run(['echo', 'eval "$(pyenv virtualenv-init -)"'], stdout=f, check=True)
        subprocess.run(['echo', 'eval "$(direnv hook bash)"'], stdout=f, check=True)


def main(box_user, github_user, github_user_email):
    """Entry point for script execution."""
    update_and_upgrade()
    install_dependencies()
    get_sublimetext_3(box_user)
    get_flake8()
    configure_git(github_user, github_user_email)
    get_pyenv_and_virtualenv(box_user)
    get_direnv()
    get_protonvpn()
    bashrc_updates()
    update_and_upgrade()


if __name__ == '__main__':
    if not sys.argv or len(sys.argv) < 1:
        print('Username and email required.')
    else:
        main(sys.argv[1], sys.argv[2])
