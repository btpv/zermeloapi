import yaml,datetime,os
with open('../../pws.yaml') as file:
    documents = yaml.full_load(file)
    pws = documents["twine"]
vers = f"build {datetime.datetime.now()}"
os.system(f'python -m build && python -m twine upload -u btpv -p {pws} dist/*')
os.system(f'git add * && git commit -m "{vers}" && git push -u origin main && pip install --upgrade zermeloapi')