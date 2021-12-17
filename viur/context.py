import signal
import logging
from io import BytesIO
from pexpect import popen_spawn
from typing import Union, List
from shutil import which
import traceback

class ViurCommandContextError(Exception):
	pass

VIUR_COMMAND_NAME = "viur"

from subprocess import check_output

class ViurCommandContext(object):
	def __init__(self, sub_cmd: str, *args) -> None:
		super().__init__()

		if not which(VIUR_COMMAND_NAME):
			raise ViurCommandContextError("Please install the viur command line.")
		else:
			version = check_output(["viur", "--version"])
			logging.debug(f"Found viur: {version}")

		self.__process: popen_spawn.PopenSpawn = None
		self.__sub_cmd: str = sub_cmd
		self.__args: str = " ".join(args)
		#self.__kwargs: dict[str, any] = kwargs
		self.__output: BytesIO = BytesIO()

	def __enter__(self):
		logging.debug(f"Executing {self.__sub_cmd} {self.__args}")
		self.__process = popen_spawn.PopenSpawn(f"viur {self.__sub_cmd} {self.__args}")
		self.__process.logfile = self.__output

		return self

	def expect(self, pattern: Union[List[str], str], timeout: int = -1, searchwindowsize: int = -1, async_: bool = False, **kw) -> None:
		if isinstance(pattern, list):
			pattern = " ".join(pattern)

		logging.debug(f"Waiting for command line pattern: {pattern}")
		self.__process.expect(pattern, timeout, searchwindowsize, async_, **kw)

	def send_line(self, text: str = '') -> None:
		logging.debug(f"Sending line with text: {self.__process.pid}:{text}")

		self.__process.sendline(text)

	def send(self, text: str) -> None:
		if not text:
			return

		logging.debug(f"Sending text to process {self.__process.pid}:{text}")
		self.__process.send(text)

	@property
	def output(self) -> str:
		return self.__output.getvalue().decode("utf-8")

	@property
	def output_lines(self) -> List[str]:
		return self.output.splitlines()

	### Process
	@property
	def pid(self) -> Union[int, None]:
		return self.__process.pid if self.__process else None
	
	@property
	def name(self) -> Union[str, None]:
		return self.__process.name if self.__process else None

	@property
	def cmd_name(self) -> str:
		return self.__sub_cmd

	def __repr__(self) -> str:
		return f"{self.__process.pid}:{self.__process.name}"

	def __exit__(self, exc_type, exc_val, exc_tb):
		try:
			logging.debug("Trying to kill process: {self}")
			self.__process.kill(sig=signal.SIGTERM)
		except PermissionError:
			logging.error(f"Trying to kill a process without enough permission.", )
			logging.error(f"Process: {self._process.name}:{self._process.pid}", )
		except:
			logging.error("Caught error...")
			logging.error(traceback.format_exc())