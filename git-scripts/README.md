Hooks are scripts that are run at certain times when you're using git,
such as before a commit is made, after a commit, etc. There's a lot of
information available online about them, so do some Googling if you're
interested!

To install hooks, put them in the .git/hooks/ folder, starting from your
Github repo. So if you cd into your holbertonschool-low_level_programming
folder, run

	'cd .git/hooks/'

to cd to the hooks folder for your repo.

The name of the hook is important: pre-commit hooks should be named pre-commit
for git to run them properly. And all hooks must have executable permissions
for git to run them.

So to install c-pre-commit, try something like this:

   cp c-pre-commit <path to repo here>/.git/hooks/pre-commit &&
      chmod +x <path to repo here>/.git/hooks/pre-commit



Pre Commit Hooks:
    c-pre-commit runs the Betty checker against each file you commit,
    and only allows you to commit ones that pass Betty. You can always
    run git commit with the --no-verify flag to ignore the warnings.
    Important:
	This requires that you have a script to run the betty checkers in your
	$PATH. If you don't, or aren't sure what I mean, check the betty folder
	in this repo for an example.