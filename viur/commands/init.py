from ..command import ViurCommand
from ..context import ViurCommandContext


#@ViurCommand()
#def hello(context: ViurCommandContext, level: str):
#	print("Calling hello!", level)

@ViurCommand()
def init(context: ViurCommandContext, name: str):
#	hello(level=1000)
	## Asking for project.conf
	context.send_line("y")
	context.send_line("1")
	context.send_line("1")
	context.send_line(name)
	context.send_line("abc")
	context.send_line("n")
	context.send_line("n")
	context.send_line("n")
	return "Hello"

@ViurCommand()
def work12x2(context: ViurCommandContext, tomate: int, tomate2: int, ekelig: int):
#	hello(level=1000)
	print(tomate, tomate2)

	return f"{tomate}"