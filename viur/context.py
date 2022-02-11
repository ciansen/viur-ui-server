import signal
import logging
from io import BytesIO
from typing import Union, List
from shutil import which
from subprocess import PIPE, Popen, check_output
import os
import sys

import traceback


class ViurCommandContextError(Exception):
	pass

VIUR_COMMAND_NAME = "viur"


class ViurCommandContext(object):
	def __init__(self, sub_cmd: str, *args) -> None:
		super().__init__()

		if not which(VIUR_COMMAND_NAME):
			raise ViurCommandContextError("Please install the viur command line.")
		else:
			version = check_output(["viur", "--version"])
			logging.debug(f"Found viur: {version}")

		self._process: Popen = None
		self._sub_cmd: str = sub_cmd
		self._args: List[str] = args
		self._output: BytesIO = BytesIO()
		self._send_list: List[str] = list()
		self._err = None

	def __enter__(self):
		logging.debug(f"Open new sub process with the command {self.command}")
		self._process = Popen(self.command, stdin = PIPE, stdout = PIPE, stderr = PIPE, encoding='utf-8', universal_newlines=True)
		# self._process = Popen(self.command, stdin = PIPE, encoding='utf-8', bufsize=650001)
		return self

	def send_line(self, text: str = '') -> None:
		self._send_list.append(text + os.linesep)
		logging.debug(f"[{self._process.pid}] Append {text} to the queue.")

	def send(self, text: str) -> None:
		if not text:
			return

		if not self._send_list:
			return

		index = len(self._send_list)-1
		self._send_list[index] += text
		logging.debug(f"[{self._process.pid}] Append {text} to line index {index}.")
	
	@property
	def command(self) -> List[str]:
		cmd = ["viur", self._sub_cmd]
		cmd.extend(self._args)
		return cmd

	@property
	def output(self) -> str:
		if isinstance(self._output, (bytes, BytesIO)):
			#return "".join(map(chr, bytearray(self._output)))
			return self._output.decode("utf-8")
		
		return self._output

	@property
	def output_lines(self) -> List[str]:
		return self.output.splitlines()

	### Process
	@property
	def pid(self) -> Union[int, None]:
		return self._process.pid if self._process else None
	
	@property
	def cmd_name(self) -> str:
		return self._sub_cmd

	def __repr__(self) -> str:
		return f"{__class__.__name__}:{self.pid}"

	def __exit__(self, exc_type, exc_val, exc_tb):
		rep = "".join(self._send_list)
		print(rep.encode("utf-8"))
		
		self._output, self._err = self._process.communicate(rep)
		print(self._output)


		self._process.wait()
		logging.debug(f"Output of the command {self.output_lines} error {self._err}")
		try:
			logging.debug(f"Trying to kill process: {self}")
			self._process.send_signal(sig=signal.SIGTERM)
			logging.debug(f"Process succesfully {self} killed.")
		except PermissionError:
			logging.error(f"Trying to kill a process without enough permission.", )
			logging.error(f"Process: {self}", )
		except:
			logging.error("Caught error...")
			logging.error(traceback.format_exc())