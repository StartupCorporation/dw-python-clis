from pathlib import Path

from dw_python_clis import ConfigVar, inner


ns = inner
ns.configure({ConfigVar.ROOT_DIR: Path(__file__).parent.parent})
