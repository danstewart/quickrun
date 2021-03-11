## Release to pypi

0. Install dependencies `pip install twine wheel`
1. Build: `python setup.py sdist bdist_wheel`
2. Upload: `twine upload dist/*`
