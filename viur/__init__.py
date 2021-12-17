from .context import ViurCommandContext
from .command import ViurCommand, ViurCommandManager
from .commands import *

def exits(name:str):
	return not ViurCommandManager().get(name) is None

def execute(command_name:str, *args, **kwargs):
	cmd = ViurCommandManager().get(command_name)
	if not cmd:
		return

	cmd(*args, **kwargs)