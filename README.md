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
| `src/fspm_tf/schema/`, `src/fspm_tf/vocabulary/` | the language-neutral files of the specification: JSON Schemas, standard names, labels, enums |
| `conformance/` | reference files, each a GLB with its expected values as JSON, and `generate.py`, which writes them |
| `src/fspm_tf/` | `fspm-tf`, the Python reference implementation: codec, validator, display copies, command line |

## The Python package

```bash
git clone https://github.com/openalea/fspm-TF.git
cd fspm-TF
mamba env create -f conda/environment.yml        # or: pip install -e . (numpy and jsonschema only)
mamba activate fspm_tf
pytest
```

```python
import fspm_tf

frame = fspm_tf.read("scene.glb")                # data structures, entity sets as numpy columns, meshes
fspm_tf.write("copy.glb", frame)
```

```bash
fspm-tf validate scene.glb                       # or a sequence: fspm-tf validate run/scene.fspm.json
fspm-tf info scene.glb
fspm-tf display scene.glb water_potential        # float32 per-vertex copies, for viewers such as ParaView
```

## For another platform

A platform implements fspm-TF in its own language and repository. It reads the conformance GLBs and compares what it
reads with their `*.expected.json`. It runs `fspm-tf validate` on what it writes, in its own CI. The steps are in the
[specification, §9](spec/fspm_tf_0.1.md#9-conformance).
