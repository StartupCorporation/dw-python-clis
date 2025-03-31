from invoke.collection import Collection

from dw_python_clis.config import ConfigVar
from dw_python_clis.deps import collection as deps_collection


__all__ = (
    "inner",
    "ConfigVar",
)

inner = Collection()

inner.add_collection(
    coll=deps_collection,
    name="deps",
)
