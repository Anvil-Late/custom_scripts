First checkout your branch (for my case master branch):
git checkout master

Then reset to remote HEAD^ (it'll remove all your local changes), force clean and pull:

git reset HEAD^ --hard && git clean -df && git pull
