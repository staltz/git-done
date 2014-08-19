git-done
========

### The simplest TODO-based task tracker integrated into git.

**Git done is a tool to manage commit messages with a TODO file.** It converts done-marked tasks in your TODO file into commit messages. You plan your future commit messages using the TODO file. This way, each task is supposed to be a small piece of contribution you should work on.

Installation
============

(`sudo`) ```pip install git+git://github.com/staltz/git-done.git#v2.0.1```

Usage
=====

Setup your git repo
-------------------

**Create a file named TODO at the root level of your project, and `git add` it to the repository.**

Workflow
--------

**1.** Insert and manage your TODO file with small and clear tasks. Remember that each task will be converted into
a commit message.

```
DONE Update README.md
DONE Add more unit tests for module x
TODO Refactor file y
```

**2.** Start working on the issue (it should be topmost TODO, i.e., 'Refactor file y').

**3.** When the task is done, flip the flag of the task from `TODO` to `DONE`:

```
DONE Update README.md
DONE Add more unit tests for module x
DONE Refactor file y
```

**4.** ```git done```

This will commit your changes with the message "Refactor file y".

TODO syntax
===========

Only lines with the keywords TODO and DONE are relevant to the commit messages.
Lines that do not have these are *silent* to the ```git done``` command and serve only for read purposes.

A line starting with `TODO` represents an unfinished task to become a commit message.

```TODO Refactor file y```

A line starting with `DONE` represents a done task turned into commit message on the next `git done` command, if the repository is currently dirty.

```DONE Refactor file y```

A line starting with `>>>` represents a tag name to be applied on `git done` once no lines above it are marked `TODO` anymore.

```>>> v0.3```

This is useful when you want to plan tags to be applied in the future once the file up until this line has been marked DONE.

Line comments are marked with ```##```:

```TODO Refactor file y ## This text will be ignored for the commit message```

Hints
----

If your todo file is not named `TODO`, you need to specify it in your repository's `.git/config` file as:

```
[gitdone]
    todofile = mytodofile
```

Multiple tasks can be marked done, and ```git done``` will concatenate them separated with `;`.

Use ```git done -p``` to preview the commit message without performing the commit.

Use vim? Include some sweet syntax highlighting: https://gist.github.com/staltz/6595113
