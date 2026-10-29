"""
fspm-TF: an exchange format for whole FSPM scenes. This package is its Python reference implementation: the codec
(fspm_tf.codec), the validator (fspm_tf.validate), the display copies (fspm_tf.display) and the vocabulary
(fspm_tf.vocabulary). See the specification in the repository's spec/ folder.
"""
SPECIFICATION_VERSION = "0.1"

from fspm_tf.model import (DataStructure, EntitySet, Frame, Grid, Mapping, Mesh, NO_ID, Relation,  # noqa: E402
                           Table, Variable)
from fspm_tf.codec import (from_bytes, read, read_index, read_sequence, to_bytes, write,  # noqa: E402
                           write_index, write_sequence)

__all__ = ["SPECIFICATION_VERSION", "DataStructure", "EntitySet", "Frame", "Grid", "Mapping", "Mesh", "NO_ID",
           "Relation", "Table", "Variable", "from_bytes", "read", "read_index", "read_sequence", "to_bytes", "write",
           "write_index", "write_sequence"]
