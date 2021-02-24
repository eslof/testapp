dist/app.zip contains a python 'portable' zipapp and all requirements included should only need python 3 interpreter  
running build.py will install requirements into testapp and reproduce dist/app.zip
  
Usage: python app.pyz --help  
to start the flask/swagger: python app.pyz serve  
  
Example run:  
python app.pyz login ola 123  
Session token: F4TR6ke5F  
python app.pyz balance F4TR6ke5F  
0  
python app.pyz deposit F4TR6ke5F 100  
Deposit success, new balance: 100  
python app.pyz withdraw F4TR6ke5F 25  
Withdraw success, new balance: 75  
python app.pyz balance F4TR6ke5F  
75  
  
python app.pyz login ingvar 456  
Session token: 5453fE6Gk  
python app.pyz deposit 5453fE6Gk 500  
Deposit success, new balance: 500  
python app.pyz transfer 5453fE6Gk ola 400  
Transfer complete, new balance: 100  
  
python app.pyz balance F4TR6ke5F  
475  
