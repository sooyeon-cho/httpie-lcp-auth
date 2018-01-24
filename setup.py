from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='httpie-lcp-auth',
    description='Loyalty Commerce Platform HMAC Auth plugin for HTTPie.',
    long_description=open('README.md').read().strip(),
    version='0.1.0',
    author='Ferdinand Cardoso',
    author_email='ferdinand.cardoso@points.com',
    license='GNU General Public License',
    url='https://github.com/pts-ferdinandcardoso/httpie-lcp-auth',
    download_url='https://github.com/pts-ferdinandcardoso/httpie-lcp-auth',
    py_modules=[
        'auth',
        'generators'
    ],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'auth = auth:LcpHmacAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.9.8'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: GNU General Public License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)