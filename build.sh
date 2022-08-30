#!/bin/sh
VERS=`python3 -c 'exec("import datetime\nprint(datetime.datetime.now())")'`
VERS="build $VERS"
echo "$VERS"
PWS=`cat ~/pws/twine`
python3 -m build && python3 -m twine upload -u btpv -p $pws dist/*
git add * && git commit -m "{vers}" && git push -u origin main && pip install --upgrade zermeloapi
