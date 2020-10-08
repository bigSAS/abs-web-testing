from distutils.core import setup
setup(
  name = 'abs-web-testing',
  packages = ['abswt'],
  version = '0.4',
  license='MIT',
  description = 'Action Based Selenium WebTesting library - selenium in more accessible way :)',
  author = 'Tomasz Majk',
  author_email = 'sas.it.tomasz.majk@gmail.com',
  url = 'https://github.com/bigSAS/abs-web-testing',
  download_url = 'https://github.com/bigSAS/abs-web-testing/archive/v0.4.tar.gz',
  keywords = ['selenium', 'action-based', 'web-testing', 'testing', 'abs-web-testing', 'abs'],
  install_requires=['selenium>=3.141.0'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
