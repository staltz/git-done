# -*- coding: utf-8 -*-
#
# grassit git utility
#
# Copyright (c) 2012 by Andre Medeiros.
import re
import optparse
from optparse import OptionParser
from git import *
import os.path, sys, os
import subprocess

GRITVERSION = "0.9"
_bullet_re = re.compile(r'\s*[-+*]\s+')
_done_re = re.compile(r'\+[ \t]*\+ *DONE')

class PlainHelpFormatter(optparse.IndentedHelpFormatter): 
	def format_description(self, description):
		if description:
			return description + '\n'
		else:
			return ''

def quit_and_normal_commit():
	subprocess.call(['hg commit'], shell=True)
	sys.exit(0)

def normalize_log(lines):
	"""Outdents newly inserted list items."""
	last_indention = 0
	for idx, line in enumerate(lines):
		match = _bullet_re.match(line)
		if match is not None:
			last_indention = match.end()
			lines[idx] = line[last_indention:]
		elif last_indention:
			if not line[:last_indention].strip():
				lines[idx] = line[last_indention:]
	return '; '.join(lines)

def ignore_comments(line):
	"""Anything after \'##\' in a line is considered a comment, will not show in the commit message"""
	poscomment = line.find('##')
	if poscomment >= 0:
		return line[0:poscomment]
	else:
		return line

def main(env=os.environ):
	desc="""\
Grassit """+GRITVERSION+""" ('hyg') is a Git tool that performs git commits using a TODO
file to get the commit message.
Any line in your TODO file marked as done will be used as part of the commit
message when you execute Grassit.

In your Git repository, set the name of your todo file in hgrc:

	[grassit]
	todofile = todo.txt

Your todo file should have one task per line. Todo tasks should start with
'- ', while done tasks should start with '+ '. When a done task is supposed
to be reported in the commit message, have the line start with '+ DONE'. Start
a line with '- TODO' just to tell yourself that the task should be reported
in a commit message, when you change it to '+ DONE'.

Example TODO file:
+ use LinkedList instead of List
+ DONE NEW login functionality ##I am a comment
- refactor those ugly classes
- TODO fix bug #3

Type 'grit' whenever you want to commit. If the TODO has got new lines
starting with '+ DONE', those tasks will be the commit message. If there is
no task marked with '+ DONE', 'grit' behaves just like 'git commit'.
"""
	parser = OptionParser(usage='%prog [options]', description=desc, formatter=PlainHelpFormatter(), version="%prog "+GRITVERSION)
	parser.add_option('-p', '--preview', 
		action='store_true', dest='preview', default=False, 
		help=u"shows what message would be committed, but does not commit".encode(sys.stdout.encoding))
	parser.add_option('-c', '--comments',
		action='store_true', dest='comments', default=False,
		help=u"includes comments (\'## ...\') in the commit message".encode(sys.stdout.encoding))

	# get options from command line
	(options, args) = parser.parse_args()

	# build repo reference
	repo = Repo(os.path.abspath(os.curdir.decode(sys.stdin.encoding)))
	rootfolder = repo.working_tree_dir
	try:
		todofilename = repo.config_reader().get_value('grassit', 'todofile')
	except Exception:
		print('ERROR: todo filename not defined. Please define \'todofile\' in section \'grassit\' of the config file')
		sys.exit(1)

	if not todofilename:
		print('ERROR: todo filename not defined')
		sys.exit(1)
	
	# quit if todo file does not exist
	if not os.path.exists(rootfolder+'/'+todofilename):
		print('ERROR: todo file not found')
		sys.exit(1)
	
	print repo
	print repo.head
	print repo.head.commit
	## discover what files were modified
	#files_modified = []
	#for line in repo.git.execute("diff","--stat").splitlines()[0:-1]:
	#	if line.find('+') >= 0:
	#		files_modified.append(line.split(' ')[1])
	
	## quit if todo file was not modified
	#if todofilename not in files_modified:
	#	# preview and exit
	#	if options.preview:
	#		print('-- Nothing from ' + todofilename + ' --')
	#		return
	#	quit_and_normal_commit()
	#
	## get all done lines from the diff
	#diffoutput = repo.hg_command("diff","-U","999999999999",rootfolder.encode(sys.getfilesystemencoding())+'/'+todofilename.encode(sys.getfilesystemencoding()))
	#log = []
	##all_lines = diffoutput.splitlines()[4:]
	#for line in diffoutput.splitlines():
	#	if not options.comments:
	#		line = ignore_comments(line)
	#	# all new lines starting with '+ DONE' are the changelog
	#	if _done_re.match(line) is not None:
	#		log.append(line[1:].lstrip().replace('+','',1).lstrip().expandtabs().replace('DONE ','').rstrip())
	#
	## show done lines
	#for line in log:
	#	print(line)
	#
	## preview and exit
	#if options.preview:
	#	if not log:
	#		print('-- Nothing from ' + todofilename + ' --')
	#	return
	#
	## do the final commit, if there was a message extracted from the todo file
	#log = normalize_log(log)
	#if not log:
	#	quit_and_normal_commit()
	#else:
	#	subprocess.Popen(['hg','commit','--message',log], shell=False)
	#	sys.exit(0)

if __name__ == '__main__':
	main()
