import os
import re
import sys
from distutils.core import setup
from setuptools.command.install import install


tests_require = [
    'pytest',
    'pytest-cov'
]

install_requires = [
    'requests'
]

MAINPACKAGE = "jsonbinio"

def parse_version_file():
    here = os.path.abspath(os.path.dirname(__file__))
    ver_dict = {}
    with open(os.path.join(here, MAINPACKAGE, '__version__.py'), 'r') as f:
        for line in f.readlines():
            m = re.match('__(\w+)__\s*=\s*(.+)', line)
            if m:
                key = m.group(1)
                val = m.group(2)
                val = re.sub("[\'\"]", "", val)
                ver_dict[key] = val
    return ver_dict


def readme():
    """print long description"""
    with open('README.rst') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != ver['version']:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, ver['version']
            )
            sys.exit(info)


ver = parse_version_file()

# setup
setup(
        title=ver['title'],
        name='JSONBinIO',
        version=ver['version'],
        packages=["jsonbinio",],
        url=ver['url'],
        license='',
        author=ver['author'],
        author_email=ver['author_email'],
        keywords='aquarium api',
        description=ver['description'],
        install_requires=install_requires,
        python_requires='>=3.4',
        tests_require=tests_require,
        classifiers=[],
        cmdclass={
            'verify': VerifyVersionCommand,
        }
)
