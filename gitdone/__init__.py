# -*- coding: utf-8 -*-
#
# git-done utility
#
# Copyright (c) 2012-2014 by Andre Staltz.

import re
import sys
import os
import subprocess
import optparse
from optparse import OptionParser
import git
from termcolor import colored


GITDONEVERSION = "2.0.0"


class PlainHelpFormatter(optparse.IndentedHelpFormatter):
	def format_description(self, description):
		if description:
			return description + '\n'
		else:
			return ''


def quit_and_normal_commit():
	subprocess.call(['git commit -a'], shell=True)
	sys.exit(0)


def normalize_log(lines):
	"""Outdents newly inserted list items."""
	last_indention = 0
	for idx, line in enumerate(lines):
		match = re.compile(r'\s+').match(line)
		if match is not None:
			last_indention = match.end()
			lines[idx] = line[last_indention:]
		elif last_indention:
			if not line[:last_indention].strip():
				lines[idx] = line[last_indention:]
	return '; '.join(lines)


def ignore_comments(line):
	'''Anything after \'##\' in a line is considered a comment, will not show
	in the commit message'''
	poscomment = line.find('##')
	if poscomment >= 0:
		return line[0:poscomment]
	else:
		return line


def main(env=os.environ):
	desc='''\
Git done is a tool that performs commits using a TODO file to get the commit 
message.
Any line in your TODO file marked as done will be used as part of the commit 
message when you execute git done.

Your todo file should have one task per line. Todo tasks should start with
'TODO', while done tasks should start with 'DONE'.

Example TODO file:
DONE Use LinkedList instead of List
DONE Login functionality ## I am a comment
TODO Refactor those ugly classes
TODO Fix bug #3

Type 'git done' whenever you want to commit. If the TODO has got new lines
starting with 'DONE', those tasks will be the commit message. If there is
no task marked with 'DONE', 'git done' behaves just like 'git commit -a'.
'''
	parser = OptionParser(
		usage='%prog [options]',
		description=desc,
		formatter=PlainHelpFormatter(),
		version="%prog "+GITDONEVERSION)
	parser.add_option('-p', '--preview',
		action='store_true', dest='preview', default=False,
		help=u"shows what message would be committed, but does not commit".encode(sys.stdout.encoding))
	parser.add_option('-c', '--comments',
		action='store_true', dest='comments', default=False,
		help=u"includes comments (\'## ...\') in the commit message".encode(sys.stdout.encoding))

	# get options from command line
	(options, args) = parser.parse_args()

	# build repo reference
	repo = git.Repo(os.path.abspath(os.curdir.decode(sys.stdin.encoding)))
	rootfolder = repo.working_tree_dir
	try:
		todofilename = repo.config_reader().get_value('gitdone', 'todofile')
	except Exception:
		todofilename = "TODO"

	# quit if todo file does not exist
	if not os.path.exists(rootfolder+'/'+todofilename):
		print("ERROR: file "+ todofilename +" not found")
		sys.exit(1)

	## discover what files were modified
	files_modified = []
	for line in repo.git.execute(['git','diff','--name-status']).splitlines():
		if line[0] == 'M':
			files_modified.append(line.split('\t')[1])

	## quit if todo file was not modified
	if todofilename not in files_modified:
		# preview and exit
		if options.preview:
			print('(Nothing from ' + todofilename + ')')
			return
		quit_and_normal_commit()

	## get all done lines from the diff
	diffoutput = repo.git.execute(['git','diff','-U999999999','--',rootfolder.encode(sys.getfilesystemencoding())+'/'+todofilename.encode(sys.getfilesystemencoding())])
	log = []
	sprint_has_to_do = False
	sprint_has_new_done = False
	tags = []
	for line in diffoutput.splitlines()[5:]:
		if not options.comments:
			line = ignore_comments(line)
		# Detected TODO
		if re.compile(r'\+{0,1}[ \t]*TODO.+').match(line):
			sprint_has_to_do = True
		# Detected DONE
		elif re.compile(r'\+[ \t]*DONE.+').match(line):
			sprint_has_new_done = True
			log.append(line[1:].lstrip().replace('DONE','').lstrip().expandtabs().rstrip())
		# Detected tag
		elif re.compile(r'\+{0,1}[ \t]*\>\>\>.+').match(line):
			if sprint_has_new_done and not sprint_has_to_do:
				tags.append(line[1:].lstrip().replace('>>>','').strip())
			# Reset sprint
			sprint_has_new_done = False
			sprint_has_to_do = False

	# show done lines
	if len(log) > 0:
		print("Done on this commit:\n")
	for line in log:
		print colored('    '+line, 'green')
	if len(log) > 0:
		print('') # newline

	# show tags to apply
	for tag in tags:
		print("This commit is tagged as "+colored(tag, 'yellow'))

	# preview and exit
	if options.preview:
		if not log:
			print('(Nothing from ' + todofilename + ')')
		return

	# do the final commit, if there was a message extracted from the todo file
	log = normalize_log(log)
	if not log:
		quit_and_normal_commit()
	else:
		repo.git.execute(['git','commit','--all','--message',log])
		for tag in tags:
			splitted = tag.split()
			message = ''
			if len(splitted)>=3 and splitted[1]=='-m':
				message = ' '.join(splitted[2:])
				repo.git.execute(['git','tag','-a',splitted[0],'-m',message])
			else:
				repo.git.execute(['git','tag',splitted[0].lstrip().rstrip()])
	return

if __name__ == '__main__':
	main()

