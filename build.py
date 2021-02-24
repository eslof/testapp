import os
import zipapp
import subprocess
import sys
from os.path import basename
from zipfile import ZipFile


def install():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "./testapp/requirements.txt", "-t", "./testapp"])


install()
zipapp.create_archive('./testapp', 'app.pyz')
with ZipFile('dist/app.zip', 'w') as zipObj:
    zipObj.write('app.pyz')
    zipObj.write('ledger.sqlite')

    for folderName, subfolders, filenames in os.walk("./templates"):
        for filename in filenames:
            filePath = os.path.join(folderName, filename)
            zipObj.write(filePath)

os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), "app.pyz"))
