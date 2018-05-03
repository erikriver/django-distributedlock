from setuptools import setup


setup(
    name='django-distributedlock',
    version='0.4.0',
    description="A distributed lock",
    long_description=open("README.rst").read(),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=['distributedlock'],
    keywords='distributed lock',
    author='Erik Rivera',
    author_email='erik.river@gmail.com',
    maintainer='Paul Logston',
    maintainer_email='code@logston.me',
    license='BSD',
    include_package_data=True,
    test_suite='runtests.runtests',
    tests_require=['django', 'gevent'],
)

