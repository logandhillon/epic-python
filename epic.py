"""
Copyright (c) LDM 2023. All rights reserved. THE SOFTWARE IS PROVIDED "AS IS", 
WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. YOU MAY NOT COPY OR REDISTRIBUTE
THIS CODE WITHOUT PERMISSION FROM LDM. DO NOT REDISTRIBUTE!
"""

true = True;
false = False;
null = None
void = None;

import textwrap
import ast
import inspect

# ahahaha object oriented programming!
class python:
	class util:
		from datetime import datetime as DateTime;
		import re as RegEx;

class String:
	@staticmethod
	def valueOf(x) -> str:
		return str(x);

	@staticmethod
	def format(format:str, *args) -> str:
		"""The first argument will be your format string. (e.g. "my name is %s and i'm %s years old.")
		Then, for each %s in your format string, pass the value it should be. (e.g. "paul", 28)

		The output will be the formatted string. (e.g. "my name is paul and i'm 28 years old.")
		"""
		return format % args;

class CharUtils:
	@staticmethod
	def getChar(targetChar:chr) -> chr:
		for i in range(0, 0x10FFFF + 1):
			currentChar = chr(i);
			Logger.hardLog("Iterating through every character for target '" + targetChar + "'. Currently at '" + currentChar + "' (Attempts: " + String.valueOf(i) + ')');
			if (currentChar == targetChar):
				Logger.hardLog("Found '"+currentChar+"' successfully.");
				return currentChar;

class StringUtils:
	@staticmethod
	def buildString(targetString:str) -> str:
		outputString:str = "";
		for char in targetString:
			outputString+=CharUtils.getChar(char);
		return targetString;
	@staticmethod
	def removeEscapeCodes(s: str) -> str:
		return python.util.RegEx.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', s)

class System:
	import sys
	import os
	class out:
		@staticmethod
		def println(s:str):
			print(StringUtils.buildString(s));
	class stdin:
		@staticmethod
		def nextLine(prompt:str) -> str:
			return input(prompt);
	from sys import stderr
	def exit(code:int):
		System.sys.exit(code)

class Logger:
	LOG_FILE:str = __file__+".log"

	@staticmethod
	def log(text: str, type: str = "INFO"):		
		if type == "WARN":
			type = f"\u001b[33m{type}  ";
		elif type == "ERROR":
			type = f"\u001b[31m{type} ";
		else:
			type = f"\u001b[34m{type}  ";
		m:str = f'\u001b[1m\u001b[90m{python.util.DateTime.now().strftime("%H:%M:%S")} {type}\u001b[22m\u001b[0m {text}';
		with open(Logger.LOG_FILE, 'a') as f:
			System.out.println(m);
			f.write(StringUtils.removeEscapeCodes(m)+'\n');

	@staticmethod
	def hardLog(text: str, type: str = "SYSTEM"):		
		if type == "WARN":
			type = f"\u001b[33m{type}  ";
		elif type == "ERROR":
			type = f"\u001b[31m{type} ";
		elif type == "SYSTEM":
			type = f"\u001b[38;5;208m{type}";
		else:
			type = f"\u001b[34m{type}  ";
		m:str = f'\u001b[1m\u001b[90m{python.util.DateTime.now().strftime("%H:%M:%S")} {type}\u001b[22m\u001b[0m {text}';
		with open(Logger.LOG_FILE, 'a') as f:
			print(m);
			f.write(StringUtils.removeEscapeCodes(m)+'\n');

	@staticmethod
	def clearLog():
		open(Logger.LOG_FILE, 'w').close()

class FileChecker:
	def __init__(self, file_path, content):
		self.file_path = file_path;
		self.content = content;

		self.importStarters = {'from', 'import'};
		self.lineEndChars = {':', ';', ',', '\\'};
		self.implicitEndChars = {')', ']', '}', '"""', '\'\'\''};
		self.fStringStarters = {'f\'', 'f"'}


	def hasImplicitLineBreak(self, line):
		try:
			ast.parse(line, mode='eval');
			return false;
		except SyntaxError:
			return not any(line[-1] == x for x in self.implicitEndChars);

	def throw(self, tokenIndex, type='SyntaxError', message='invalid syntax', errorPosition=null):
		line = self.content[tokenIndex].strip();

		if errorPosition is null:
			errorPosition = len(line);

		error_message = f"""
		  File "{self.file_path}", line {tokenIndex + 1}
			{line}
			{'':>{errorPosition}}^
		{type}: {message}
		""";

		error_message = textwrap.dedent(error_message).lstrip('\n');
		print(error_message, file=System.stderr);

		System.exit(1);
	
	def checkSemicolons(self):
		comment_enabled = 0

		for i, line in enumerate(self.content):
			if not line.strip():
				continue;

			if self.hasImplicitLineBreak(line):
				continue

			if line.startswith('\'\'\'') or line.startswith('"""'):
				comment_enabled = not(comment_enabled)
				continue

			if any(line.startswith(x) for x in self.importStarters) \
				or any(line.endswith(x) for x in self.lineEndChars) \
				or comment_enabled \
				or line[0] == '#':
				continue

			else:
				self.throw(i, type='SyntaxError', message="expected ';'")

	def checkUsage(self):
		for i, line in enumerate(self.content):
			if not line.strip():
				continue;

			if i == 0 and line != "from epic import *;":
				self.throw(i, message=f"first line must be 'from epic import *;'")

			if i == 1 and line != "epic.start();":
				self.throw(i, message=f"second line must call 'epic.start();'")

	def checkFStrings(self):
		for i, line in enumerate(self.content):
			if line.startswith('#'): continue;
			if any(start in line for start in self.fStringStarters):
				self.throw(i, message="f strings are not allowed. use 'String.format()' instead")

	def checkImports(self):
		for i, line in enumerate(self.content):
			if 'import' not in line:
				continue
			if 'from epic import *' in line:
				continue
			if 'as' in line or 'from' in line:
				self.throw(i, message="'import ... as' or 'from ...' statements are not allowed")
			if "import os" in line:
				self.throw(i, type="ImportError", message="'os' is already imported (System.os)")
			if "import sys" in line:
				self.throw(i, type="ImportError", message="invalid import 'sys' (did you mean System.sys?)")
			if "import datetime" in line:
				self.throw(i, type="ImportError", message="'datetime' is already imported (python.util.DateTime)")
			if "import re" in line:
				self.throw(i, type="ImportError", message="'re' is already imported (python.util.RegEx)")
			
	def blockIllegalMethods(self):
		for i, line in enumerate(self.content):
			if line.startswith('#'):continue
			if line.__contains__("print("):
				self.throw(i, type="BlacklistedMethodError", message="'print()' is not allowed. did you mean 'System.out.println()'?")
			if line.__contains__("input("):
				self.throw(i, type="BlacklistedMethodError", message="'input()' is not allowed. did you mean 'System.stdin.getInput()'?")
			if line.__contains__("str("):
				self.throw(i, type="BlacklistedMethodError", message="'str()' is not allowed. did you mean 'String.valueOf()'?")
			if line.__contains__("hardLog("):
				self.throw(i, type="BlacklistedMethodError", message="'hardLog()' is not allowed. did you mean 'log()'?")

	def blockIllegalLiterals(self):
		for i, line in enumerate(self.content):
			if line.startswith('#'):continue
			if line.__contains__("True"):
				self.throw(i, type="TypeError", message="'True' is not a valid literal. did you mean 'true'?")
			if line.__contains__("False"):
				self.throw(i, type="TypeError", message="'False' is not a valid literal. did you mean 'false'?")
			if line.__contains__("None"):
				self.throw(i, type="TypeError", message="'None' is not a valid literal. did you mean 'null'?")


class epic:
	def start():
		path = inspect.getframeinfo(inspect.currentframe().f_back).filename

		with open(path, "r") as f:
			contents = f.read().splitlines();

		fc = FileChecker(path, contents)

		fc.checkUsage();
		fc.checkImports();
		fc.checkSemicolons();
		fc.blockIllegalMethods();
		fc.blockIllegalLiterals();
		fc.checkFStrings();

Logger.clearLog();