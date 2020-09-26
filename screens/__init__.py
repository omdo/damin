from .login import LoginScreen
from .main import MainScreen
from .about import AboutScreen
from .account import AccountScreen
from .render import RenderScreen

class Screens:
	def __init__(self):
		self.login = LoginScreen()
		self.main = MainScreen()
		self.about = AboutScreen()
		self.account = AccountScreen()
		self.render = RenderScreen()