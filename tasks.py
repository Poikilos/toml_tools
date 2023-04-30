from invoke import task

from pathlib import Path

INVOKE_VENVS_DIR = Path(__file__) / '.invoke_venvs'

VENVS = {'py27': r'C:\Python27\python.exe',
         'ipy27': r'C:\Program Files\IronPython 2.7\ipy.exe',
         'py312': r'C:\Program Files\Python312\python.exe'
         }




@task
def setup(c, envs = None):
    if envs is None:
        items = VENVS.items()
    else:
        items = {env: VENVS[env] for env in envs} 
    for key, val in items:
        c.run(f'{val} -m virtualenv {INVOKE_VENVS_DIR / key}')



