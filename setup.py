from setuptools import setup, find_packages


setup(
    name='django-distributedlock',
    version='0.2.4',
    description="A distributed lock",
    long_description=open("README.rst").read(),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='distributed lock',
    author='Erik Rivera',
    author_email='erik.river@gmail.com',
    maintainer='Paul Logston',
    maintainer_email='code@logston.me',
    license='BSD',
    include_package_data=True,
    test_suite='runtests.runtests',
    tests_require=['gevent'],
)

