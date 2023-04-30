from invoke import task

from pathlib import Path

INVOKE_VENVS_DIR = Path(__file__) / '.invoke_venvs'

VENVS = {'py27': r'C:\Python27\python.exe',
         'ipy27': r'C:\Program Files\IronPython 2.7\ipy.exe',
         'py312': r'C:\Program Files\Python312\python.exe'
         }




@task
def test(c, envs = None):
    interpreter = INVOKE_VENVS_DIR /
    c.run('py -2 -m virtualenv')



