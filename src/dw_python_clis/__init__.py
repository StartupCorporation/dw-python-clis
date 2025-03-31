from invoke.collection import Collection

from dw_python_clis.config import ConfigVar
from dw_python_clis.deps import collection as deps_collection
from dw_python_clis.internal import change_to_root_dir


__all__ = (
    "inner",
    "ConfigVar",
    "change_to_root_dir",
)

inner = Collection()

inner.add_collection(
    coll=deps_collection,
    name="deps",
)
