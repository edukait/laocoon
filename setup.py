from distutils.core import setup
setup(
  name = 'laocoon',
  packages = ['laocoon'],
  version = '0.1',
  license='MIT',
  description = 'Automatically and efficiently count the number of cells in a fluorescently stained image.',
  author = 'Kaitlin Lim',
  author_email = 'kaitlin.y.lim@gmail.com',
  url = 'https://github.com/edukait/laocoon',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['analysis', 'high-throughput', 'efficient'],
  install_requires=[
          'numpy',
          'panda',
          'mahotas',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Science/Research',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
