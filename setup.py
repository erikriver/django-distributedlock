from setuptools import setup, find_packages

version = '0.2.3'

setup(name='django-distributedlock',
      version=version,
      description="",
      long_description=open("README.rst").read(),
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='distributed lock',
      author='Erik Rivera',
      author_email='erik.river@gmail.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
