========
Git done
========

Git-done is a tool that performs commits using a TODO file to get the commit message.
Any line in your TODO file marked as done will be used as part of the commit
message when you execute git done.

In your Git repository, set the name of your todo file in .git/config:

	[gitdone]
		todofile = TODO

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

Type 'git done' whenever you want to commit. If the TODO has got new lines
starting with '+ DONE', those tasks will be the commit message. If there is
no task marked with '+ DONE', 'git done' behaves just like 'git commit -a'.

