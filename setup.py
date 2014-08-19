from distutils.core import setup

setup(
	name="git-done",
	version='2.0.0',
	author="Andre Staltz",
	author_email='andrestaltz@gmail.com',
	packages=['gitdone'],
	scripts=['bin/git-done'],
	url='https://github.com/staltz/git-done',
	license='LICENSE.txt',
	description="A git extension to manage todos and commit messages.",
	long_description=open('README.md').read(),
	install_requires=[
		"GitPython == 0.3.2.RC1",
		"termcolor == 1.1.0",
	],
)

