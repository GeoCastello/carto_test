import os
import sys
from shutil import copyfile

os.chdir(os.path.dirname(__file__))

hooks = ['pre-commit', 'pre-push']

if len(sys.argv) > 1 and sys.argv[1] == 'remove':
    print('Removing git hooks:\n---')
    for hook in hooks:
        print('\U0001F5D1 ' + hook)
        git_hook = '../.git/hooks/' + hook
        try:
            os.remove(git_hook)
        except Exception:
            pass

else:
    print('Installing git hooks:\n---')
    for hook in hooks:
        print('\U00002705 ' + hook)

        git_hook = '../.git/hooks/' + hook
        copyfile(hook, git_hook)
        os.chmod(git_hook, 0o755)

print('---\nDone \U0001f44d')
