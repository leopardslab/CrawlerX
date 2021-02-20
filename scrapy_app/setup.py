from setuptools import setup, find_packages

setup(
    name         = 'scrapy_app',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = scrapy_app.settings']},
)