from typing import Callable
from utils import Singleton
from .context import ViurCommandContext

import logging
import inspect

class ViurCommand(object):
	def __init__(self, name: str = None, *args, **kwargs) -> None:
		self._name = name
		self._args = args
		self._kwargs = kwargs
	
	def __call__(self, func: Callable):
		name = self._name if self._name else func.__name__

		def wrapped_func(*args, **kwargs):
			_args = list(args)
			_args.extend(self._args)
			args = tuple(_args)


			self._kwargs.update(kwargs)
			
			res = None
			with ViurCommandContext(name, *args) as context:
				res = func(context, *args, **self._kwargs)
			return res
		
		sig = inspect.signature(func)
		args = list(sig.parameters.keys())[1:]
		setattr(wrapped_func, "args", args)
		#cx = [type.annotation for type in list(sig.parameters.values())[1:]]
		#setattr(wrapped_func, "args_type", cx)

		wrapped_func.__name__ = func.__name__

		ViurCommandManager().register_command(name, wrapped_func)

		return wrapped_func

class ViurCommandManager(Singleton, dict):
	def __init__(self) -> None:
		super(dict, self).__init__()
		super(Singleton, self).__init__()

	def register_command(self, name: str, cmd: ViurCommand):
		if name in self.keys():
			logging.warn(f"The command with the name {name} is already registered.")

			self[name] = cmd
		else:
			self.update({
				name: cmd
			})

