from distutils.core import setup

EGG = '#egg='
install_requires = []

with open('requirements.txt') as f:
    for line in f.read().splitlines():

        if line.startswith('git+'):
            if EGG not in line:
                raise Exception('egg specification is required.')
            package_name = line[line.find(EGG) + len(EGG):]
            dependency_link = line[:line.find(EGG)]
            install_requires.append(f"{package_name} @ {dependency_link}")
        else:
            install_requires.append(line)

setup_info = {'name':'ps_interface',
              'version': '0.0.1',
              'description': 'A web application for public statements',
              'author': 'Johanan Tai',
              'author_email': 'jtai.dvlp@gmail.com',
              'url':'https://gitlab.com/jtai-dev/ps_interface',
              'packages':['ps_interface'],
              'install_requires': install_requires}

setup(**setup_info)