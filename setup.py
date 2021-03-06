from setuptools import setup


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: BSD License',
]

extras_require = {
    'test': [
        'tox >= 2.6.0',
        'pytest >= 3.0.3',
        'pytest-cov >= 2.3.1',
    ],
    'devel': [
        'bumpversion >= 0.5.2',
        'check-manifest >= 0.35',
        'readme-renderer >= 16.0',
        'flake8',
        'pep8-naming',
    ]
}

kw = {
    'name':                 'commandpool',
    'version':              '0.0.0',

    'description':          'Functions for running many subprocesses in parallel',
    'long_description':     open('README.rst').read(),

    'author':               'Georgi Valkov',
    'author_email':         'georgi.t.valkov@gmail.com',
    'license':              'Revised BSD License',
    'keywords':             'subprocess pool',
    'url':                  'https://github.com/gvalkov/python-commandpool',
    'classifiers':          classifiers,
    'extras_require':       extras_require,
    'py_modules':           ['commandpool'],
    'zip_safe':             True,
}


if __name__ == '__main__':
    setup(**kw)
