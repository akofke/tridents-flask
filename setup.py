from setuptools import setup

setup(
    name='tridents',
    packages=['tridents'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'Flask-SqlAlchemy',
        'SQLAlchemy-Utils',
        'psycopg2',
        'arrow',
        'Flask-WTF',
        'Flask-Migrate',
        'markdown',
        'BeautifulSoup4',
        'bleach',
        'Flask-SSLify'
    ],
)