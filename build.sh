#!/bin/sh
cp "./src/zermeloapi/__init__.py" "src\zermeloapi\__init__.py"
python3 -c "exec('path = \'src/zermeloapi.egg-info\'\nfrom os import listdir,system\nfrom os.path import join\nitems = []\nfor i in listdir(path):\n\titems.append([join(path,i),join(path,i).replace(\'/\',\'\\\\\\\\\\\\\\\\\')])\nfor i in items:\n\tsystem(f\'cp {i[0]} {i[1]}\')')"
VERS=`python3 -c 'exec("import datetime\nprint(datetime.datetime.now())")'`
VERS="build $VERS"
echo "$VERS"
python3 -m build -s
python3 -m build -w
python3 -m twine upload dist/*
rm dist -r
rm build -r
rm src\\zermeloapi*
git add * 
git commit -m "$VERS" 
git push -u origin main
sleep 5
pip install --upgrade zermeloapi
