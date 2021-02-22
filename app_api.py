import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from typing import Dict, Any
from flask_restplus import Resource
from commands.transfer import do_transfer
from commands.auth import login, logout
from commands.atm import deposit, withdraw, balance
from flaskapp import api, app


@api.route('/login/<string:user_name>/<int:pin>')
class LoginAPI(Resource):
    @api.doc(params={'user_name': 'your desired or claimed unique user name',
                     'pin': 'your desired or registered pin code'})
    def get(self, user_name: str, pin: int):
        return {'message': login(user_name, pin)}


@api.route('/logout/<string:token>')
class LogoutAPI(Resource):
    @api.doc(params={'token': 'your session token to invalidate'})
    def get(self, token: str):
        return {'message': logout(token)}


@api.route('/deposit/<string:token>/<int:amount>')
class DepositAPI(Resource):
    @api.doc(params={'token': 'your session token from login',
                     'amount': 'the amount of coins to deposit into your account'})
    def get(self, token: str, amount: int):
        return {'message': deposit(token, amount)}


@api.route('/withdraw/<string:token>/<int:amount>')
class WithdrawAPI(Resource):
    @api.doc(params={'token': 'your session token from login',
                     'amount': 'the amount of coins to withdraw from your account'})
    def get(self, token: str, amount: int):
        return {'message': withdraw(token, amount)}


@api.route('/balance/<string:token>')
class BalanceAPI(Resource):
    @api.doc(params={'token': 'your session token from login'})
    def get(self, token: str):
        return {'message': balance(token)}


@api.route('/transfer/<string:token>/<string:second_party>/<int:amount>')
class TransferAPI(Resource):
    @api.doc(params={'token': 'your session token from login',
                     'second_party': 'the user name of recipient',
                     'amount': 'the amount of coins to transfer from your account'})
    def get(self, token: str, second_party: str, amount: int) -> Dict[str, Any]:
        return {'message': do_transfer(token, second_party, amount)}


def run_app():
    api.init_app(app)
    app.run()
