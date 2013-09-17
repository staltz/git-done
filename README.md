git-done
========

### Git done is a tool to manage commit messages with a TODO file.

It converts done-marked tasks in your TODO file into commit messages. 
Essentially it's a lightweight task tracker integrated into git. You plan your future commit messages 
using the TODO file. This way, each task is supposed to be a small piece of contribution you should work on.

Installation
============

```pip install git+git://github.com/staltz/git-done.git```

Usage
=====

Setup your git repo
-------------------

**1.** Create a file named TODO or something else you wish, and add it to your repository.

**2.** Edit ```.git/config``` to point to the TODO file:

```
[gitdone]
    todofile = TODO
```

Workflow
--------

**1.** Insert and manage your TODO file with small and clear tasks. Remember that each task will be converted into
a commit message.

```
+ DONE update README.md
+ DONE add more unit tests for module x
- TODO refactor file y
```

**2.** Start working on the issue (in this case, you are 'refactoring file y').

**3.** When the task is done, flip the flag of the task from ```- TODO``` to ```+ DONE```:

```
+ DONE update README.md
+ DONE add more unit tests for module x
+ DONE refactor file y
```

**4.** ```git done```

This will commit your changes with the message "refactor file y".

TODO syntax
===========

Only lines with the keywords TODO and DONE are relevant to the commit messages. 
Lines that do not have these are *silent* to the ```git done``` command and serve
only for read purposes.

A line starting with a dash (spaces before it are allowed) represents a silent unfinished task.

```- refactor file y```

A line starting with a plus represents a silent done task.

```+ refactor file y```

A line starting with dash and TODO represents an unfinished task to become a commit message.

```- TODO refactor file y```

A line starting with plus and DONE represents a done task turned into commit message on a ```git done``` command.

```+ DONE refactor file y```

A line starting with `>>>` represents a tag name to be applied on ```git done``` once no lines above it
are marked `- TODO`.

```>>> 0.3```

This is useful when you want to plan tags to be applied in the future once the file up until this line
has been marked DONE.

Line comments are marked with ```##```:

```- TODO refactor file y ## this text will be ignored for the commit message```

Hints
----

Multiple tasks can be marked done, and ```git done``` will concatenate them separated with `;`. 

Use ```git done -p``` to preview the commit message without performing the commit.

Use vim? Include some sweet syntax highlighting: https://gist.github.com/staltz/6595113
