from datetime import datetime
import yaml,datetime
with open('../../pws.yaml') as file:
    documents = yaml.full_load(file)
    print(documents["twine"])
vers = f"build {datetime.datetime.now()}"