from setuptools import setup

setup(name='csv_intel',
      version='0.32',
      description='Get the vital statistics of a CSV file',
      long_description=open('README.md', 'rb').read(),
      url='http://github.com/MarkNenadov/csv-intel',
      classifiers=['License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha'],
      author='Sam Birch',
      author_email='marknenadov@gmail.com',
      license='MIT',
      packages=['csv_intel'],
      scripts=['scripts/csv-intel'],
      zip_safe=False)
