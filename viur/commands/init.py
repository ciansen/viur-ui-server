from ..command import ViurCommand
from ..context import ViurCommandContext


#@ViurCommand()
#def hello(context: ViurCommandContext, level: str):
#	print("Calling hello!", level)

@ViurCommand()
def init(context: ViurCommandContext):
#	hello(level=1000)
	return "Hello"

@ViurCommand()
def work12x2(context: ViurCommandContext, tomate: int, tomate2: int, ekelig: int):
#	hello(level=1000)
	print(tomate, tomate2)

	return f"{tomate}"