# fspm-TF

An exchange format for whole functional-structural plant model (FSPM) scenes, across platforms and languages
(openalea.metafspm, CPlantBox, GroIMP, VirtualPlantLab). It holds:

- multiscale plant graphs;
- their state variables and parameters;
- their geometry;
- the environment's grids.

Each time step is one glTF file, and the variables share one vocabulary. It also aims to serve as an in-memory
interface for coupling components across platforms.

Status: specification 0.1, draft.

- [The specification](spec/fspm_tf_0.1.md)
- [The design note](docs/design_note.md): the review of existing formats and the decisions taken
- [Implementations](implementations.md)

## The repository

| Folder | Content |
|---|---|
| `spec/` | the specification |
| `src/openalea/fspm_tf/schema/`, `src/openalea/fspm_tf/vocabulary/` | the language-neutral files of the specification: JSON Schemas, standard names, labels, enums |
| `conformance/` | reference files, each a GLB with its expected values as JSON, and `generate.py`, which writes them |
| `src/openalea/fspm_tf/` | `openalea.fspm_tf`, the Python reference implementation: codec, validator, display copies, command line |
| `paraview/` | the ParaView reader plugin, and the script checking it in a `pvpython` |

## The Python package

```bash
git clone https://github.com/openalea/fspm-TF.git
cd fspm-TF
mamba env create -f conda/environment.yml        # or: pip install -e . (numpy and jsonschema only)
mamba activate fspm_tf
pytest
```

```python
from openalea import fspm_tf

frame = fspm_tf.read("scene.glb")                # data structures, entity sets as numpy columns, meshes
fspm_tf.write("copy.glb", frame)
```

```bash
fspm-tf validate scene.glb                       # or a sequence: fspm-tf validate run/scene.fspm.json
fspm-tf info scene.glb
fspm-tf display scene.glb water_potential        # float32 per-vertex copies, for viewers such as ParaView
```

## Viewing in ParaView

`paraview/fspm_tf_reader.py` is a ParaView reader plugin (ParaView ≥ 5.10):

1. In ParaView, open Tools → Manage Plugins → Load New…, and choose the file. Tick "Auto Load" to keep it loaded.
2. File → Open a `.glb` frame or a sequence's `scene.fspm.json`, and pick "fspm-TF reader".

What it shows:

- Each data structure is a block: its meshes, its segments as lines (for a Tube filter on `radius`) and its grid.
- Every variable of every scale is a data array named `<entity set>.<variable>`, at full precision, with no display
  copies needed. A sequence's frames are the time steps.
- Text columns such as labels become integer codes, `<entity set>.<column>_code`; the names behind the codes are in
  the block's field data.

The plugin finds `openalea.fspm_tf` in ParaView's Python if it is installed there, otherwise in this clone's `src/`.
It needs nothing beyond what ParaView ships (numpy). In `pvpython` scripts the reader is
`fspmTFreader(FileName=...)`, after `LoadPlugin("paraview/fspm_tf_reader.py", ns=globals())`. Checked with
ParaView 6.0.1: `pvpython paraview/check_in_paraview.py conformance` (also run by the tests when
`FSPM_TF_PVPYTHON` names a pvpython).

## For another platform

A platform implements fspm-TF in its own language and repository. It reads the conformance GLBs and compares what it
reads with their `*.expected.json`. It runs `fspm-tf validate` on what it writes, in its own CI. The steps are in the
[specification, §9](spec/fspm_tf_0.1.md#9-conformance).
