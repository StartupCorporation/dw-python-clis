import os

from invoke.context import Context
from invoke.tasks import task

from dw_python_clis.config import ConfigVar


@task
def change_to_root_dir(
    context: Context,
):
    """
    Internal pre-task to change working directory to the root directory of the project.
    """
    os.chdir(context[ConfigVar.ROOT_DIR])
