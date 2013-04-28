"""
Flacon
-------------

Flask application manager
"""
from setuptools import setup

setup(
    name='Flacon',
    version='0.0.1',
    url='',
    license='BSD',
    author='Mehdi Bayazee, Mostafa Rokooie',
    author_email='bayazee@gmail.com, mostafa.rokooie@gmail.com',
    description='Flask based web framework',
    long_description=__doc__,
    packages=['flacon', 'flacon.commands'],
    include_package_data=True,
    package_data={'flacon': ['flacon/actions/project_template/*']},
    namespace_packages=['flacon'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'flask>=0.9'
    ],
#    scripts=['flacon/actions/flacon.py'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
