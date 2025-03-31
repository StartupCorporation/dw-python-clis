from invoke.collection import Collection
from invoke.context import Context
from invoke.tasks import task

from dw_python_clis.config import ConfigVar
from dw_python_clis.internal import change_to_root_dir
from dw_python_clis.utils import get_pyproject_content


@task(
    name="sync-kernel",
    pre=[change_to_root_dir],
)
def sync_shared_kernel(
    context: Context,
):
    """
    Installs local shared kernel to the virtual environment.
    """
    context.run("pip install -q ../../dw_shared_kernel")
    context.run("rm -r ../../dw_shared_kernel/src/dw_shared_kernel.egg-info")
    context.run("rm -r ../../dw_shared_kernel/build")
    print("Installed local shared kernel to the virtual environment.")


@task(
    name="regenerate",
    pre=[change_to_root_dir],
)
def regenerate_dependencies(
    context: Context,
):
    """
    Regenerates all dependencies for services.
    """
    pyproject_file = get_pyproject_content(file_path=context[ConfigVar.ROOT_DIR] / "pyproject.toml")

    for optional_deps in pyproject_file["project"]["optional-dependencies"]:
        compile_(context, f"requirements/requirements.{optional_deps}.txt", False, optional_deps)

    compile_(context, "requirements/requirements.txt", True, None)


@task(
    name="compile",
    help={
        "extra": "The additional packages section to install.",
        "all_deps": "Whether to install all extra dependencies.",
        "output_file": "The output file where compiled packages will be written.",
    },
    optional=["extra"],
    pre=[change_to_root_dir],
)
def compile_(
    context: Context,
    output_file: str,
    all_deps: bool = False,
    extra: str | None = None,
) -> None:
    """
    Compiles packages from the pyproject.toml file to the output file.
    """
    args = [
        "-q",
        f"-o {output_file}",
        "--no-header",
        "--no-annotate",
        "--no-strip-extras",
        "--unsafe-package",
        "pyproject.toml",
    ]

    if all_deps:
        args.insert(0, "--all-extras")
    elif extra:
        args.insert(0, f"--extra {extra}")

    pyproject_file = get_pyproject_content(file_path=context[ConfigVar.ROOT_DIR] / "pyproject.toml")
    project_name = pyproject_file["project"]["name"].replace("-", "_")

    context.run("mkdir -p requirements")
    context.run(f"pip-compile {' '.join(args)}")
    context.run(f"rm -rf src/{project_name}.egg-info")

    print(f"Successfully compiled packages to the '{output_file}'.")


@task(
    help={
        "packages": "The list of packages to upgrade. Must be separeted by whitespace.",
        "output_file": "The output file where compiled packages will be written.",
    },
    pre=[change_to_root_dir],
)
def upgrade(
    context: Context,
    packages: str,
    output_file: str,
) -> None:
    """
    Upgrades packages that are specified in the args and writes new packages' version to specified file.
    """
    packages_list = packages.split()
    args = [
        "-q",
        f"-o {output_file}",
        "--no-header",
        "--no-annotate",
        "--no-strip-extras",
        "--unsafe-package",
        *map(lambda package: f"--upgrade-package {package}", packages_list),
        "pyproject.toml",
    ]
    context.run(f"pip-compile {' '.join(args)}")
    context.run("rm -rf src/order_app.egg-info")
    print(
        f"Upgraded {' '.join(packages_list)} {'packages' if len(packages_list) > 1 else 'package'}"
        f"to the {output_file} file.",
    )


@task(
    help={
        "file": "The file containing the packages to install.",
    },
    pre=[change_to_root_dir],
)
def install(
    context: Context,
    file: str,
) -> None:
    """
    Install packages from the provided requirements file.
    """
    context.run(f"pip-sync {file} -q")
    print(f"Successfully installed packages from the '{file}'.")


collection = Collection(
    sync_shared_kernel,
    regenerate_dependencies,
    compile_,
    upgrade,
    install,
)
