from terminaltables import DoubleTable

from core.console.Command import Command
from core.console.input.InputOption import InputOption
from core.snips.SamkillaManager import SamkillaManager
from core.snips.SnipsConsoleManager import SnipsConsoleManager
from core.util.ThreadManager import ThreadManager
from core.voice.LanguageManager import LanguageManager


#
# AssistantSyncCommand synchronize dialogTemplates + cache with snips assistant
#
class AssistantSyncCommand(Command):

	def create(self):
		self.name = 'assistant:sync'
		self.setDescription('Sync dialog templates for all modules')
		self.setDefinition([
			InputOption(name='--download', shortcut='-d', mode=InputOption.Mode.NONE, description='Also download the new trained assistant'),
		])
		self.setHelp('> The %command.name% command sync dialog templates for all modules:\n'
					 '  <fg:magenta>%command.full_name%<fg:reset>')


	def execute(self, inputt):
		TABLE_DATA = [['Assistant Dialog Templates Sync']]
		table_instance = DoubleTable(TABLE_DATA)
		self.write('\n' + table_instance.table + '\n', 'green')

		languageManager = LanguageManager()
		languageManager.onStart()

		threadManager = ThreadManager()
		threadManager.onStart()

		snipsConsoleManager = SnipsConsoleManager()
		snipsConsoleManager.onStart()

		samkillaManager = SamkillaManager()

		self.write('It may take some time...')
		changes = samkillaManager.sync(download=False)
		self.nl()

		if changes:
			self.write('There are <fg:green>changes<fg:reset>')
		else:
			self.write('There are no <fg:red>changes<fg:reset>')

		self.nl()
		self.write('All dialog templates <fg:green>synced!<fg:reset>')
		self.nl()

		if inputt.getOption('download'):
			snipsConsoleManager.download(languageManager.activeSnipsProjectId)
			self.write('Downloading assistant...')
			self.nl()
			self.write('Assistant <fg:green>downloaded!<fg:reset>')
			self.nl()
