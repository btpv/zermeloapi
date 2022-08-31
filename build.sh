#!/bin/sh
cp "./src/zermeloapi/__init__.py" "./src\zermeloapi\__init__.py"
VERS=`python3 -c 'exec("import datetime\nprint(datetime.datetime.now())")'`
VERS="build $VERS"
echo "$VERS"
PWS=`cat ~/pws/twine`
ls src/zermeloapi
python3 -m build
python3 -m twine upload -u btpv -p $PWS dist/*
rm dist -r
rm ./"src\zermeloapi\__init__.py"
git add * 
git commit -m "$VERS" 
git push -u origin main
pip install --upgrade zermeloapi
