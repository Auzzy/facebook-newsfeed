class CommandNotFoundError(NotImplementedError):
	pass

class CommandError(ValueError):
	pass

class LoadError(CommandError):
	pass

class NextError(CommandError):
	pass

class PrevError(CommandError):
	pass

class CommentsError(CommandError):
	pass

class PrintError(CommandError):
	pass

class GoError(CommandError):
	pass

class HelpError(CommandError):
	pass
