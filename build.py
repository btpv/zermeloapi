import yaml,datetime,os
with open('../../pws.yaml') as file:
    documents = yaml.full_load(file)
    pws = documents["twine"]
vers = f"build {datetime.datetime.now()}"
print(os.system(f'pythons -m build && pythons -m twine upload -u btpv -p {pws} dist/*'))
print(os.system(f'git add * && git commit -m "{vers}" && git push -u origin main && pip install --upgrade zermeloapi'))
print(vers)