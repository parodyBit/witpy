import os
import platform
import subprocess

from pathlib import Path


def working_directory():
    '''

    :return: the working directory
    '''
    return os.getcwd()


def os_version():
    return os.name


def os_linux():
    '''
    :return: True if running linux
    '''
    return os_version() == 'posix'


def os_windows():
    '''
    :return: True if running windows
    '''
    return os_version() == 'nt'


def os_release():
    return platform.release()


def system():
    return platform.system().lower()


def rust_version():
    command = 'cargo --version'
    process = subprocess.Popen(f'{command}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    output = stdout.decode('utf-8')
    if os_windows():
        if 'not recognized' in output:
            output = 'Rust is Not Installed'
    elif os_linux():
        if 'not found' in output:
            output = 'Rust is Not Installed'
    return output.rstrip()


def docker_version():
    command = 'docker -v'
    process = subprocess.Popen(f'{command}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    output = stdout.decode('utf-8')
    installed = True
    if os_windows():
        if 'not recognized' in output:
            output = 'Docker is Not Installed'
            installed = False
    elif os_linux():
        if 'not found' in output:
            output = 'Docker is Not Installed'
            installed = False
    if installed:
        output = output[15:]
    return output.rstrip()


def print_system_info():
    print('-------------------------------')
    print('| System Information')
    print('| ------------------')
    print(f'| Operating System: \t{platform.system()} ({platform.platform()})')
    print(f'| Python Version: \t{platform.python_version()} {platform.python_build()}')
    print(f'| Rust Version: \t{rust_version()}')
    # print(f'| Docker Version: \t{docker_version()}')

    print('|')
    print('| Witnet Information')
    print('| ------------------')
    #print(f'| Witnet Version:\t{}')
    print(f'| ')
    print(f'| ')

