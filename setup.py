from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
version = (here / 'src' / 'adbPullAs' / 'VERSION').read_text(encoding='utf-8')
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='adbPullAs',
    version=version,
    description='adb pull wrapper to pull package private files from Android device',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ViliusSutkus89/adbPullAs/',
    author="Vilius Sutkus '89",
    author_email='ViliusSutkus89@gmail.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: Android',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities'
    ],
    keywords='adb pull run-as',
    project_urls={
        'Tracker': 'https://github.com/ViliusSutkus89/adbPullAs/issues'
    },
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9',
    package_data={'adbPullAs': ['VERSION']},
    entry_points={'console_scripts': ['adbPullAs=adbPullAs:main']}
)
