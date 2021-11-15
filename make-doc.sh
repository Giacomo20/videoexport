rm -rf docs
sphinx-quickstart -q -a Giacomo -p VideoExport --ext-autodoc --extension sphinx_autodoc_typehints docs
sed -i '/# import os/ c\import os' docs/conf.py
sed -i '/# import sys/ c\import sys' docs/conf.py
sed -i "/# sys.path.insert/ c\sys.path.insert(0, os.path.abspath('..'))" docs/conf.py
sed -i "/html_theme/ c\html_theme = 'sphinx_rtd_theme'" docs/conf.py
sed -i "12 a \ \ \ modules" docs/index.rst

pushd docs
sphinx-apidoc -o . ..
make html
popd
