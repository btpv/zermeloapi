#!/bin/sh
cp "./src/zermeloapi/__init__.py" "src\zermeloapi\__init__.py"
python3 -c "exec('path = \'src/zermeloapi.egg-info\'\nfrom os import listdir,system\nfrom os.path import join\nitems = []\nfor i in listdir(path):\n\titems.append([join(path,i),join(path,i).replace(\'/\',\'\\\\\\\\\\\\\\\\\')])\nprint(items)\nfor i in items:\n\tsystem(f\'cp {i[0]} {i[1]}\')')"
VERS=`python3 -c 'exec("import datetime\nprint(datetime.datetime.now())")'`
VERS="build $VERS"
echo "$VERS"
PWS=`cat ~/pws/twine`
python3 -m build -s
python3 -m build -w
python3 -m twine upload -u btpv -p $PWS dist/*
rm dist -r
rm build -r
# rm ./"src\zermeloapi\__init__.py"
git add * 
git commit -m "$VERS" 
git push -u origin main
pip install --upgrade zermeloapi
