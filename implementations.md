# Implementations

| Platform | Language | Where | Reads | Writes | Specification version |
|---|---|---|---|---|---|
| openalea.fspm_tf (reference) | Python | this repository, `src/openalea/fspm_tf` | yes | yes | 0.1 |
| openalea.metafspm | Python | `openalea.metafspm.io.fspm_tf` (branch release2026) | yes: its own frames, rebuilt bit for bit | yes | 0.1 |
| CPlantBox | C++ / Python | planned (phase P4) | | | |
| GroIMP | Java | | | | |
| VirtualPlantLab | Julia | | | | |

An implementation is listed with the version it passes: it reads every conformance file as expected, and writes
files that the validator accepts (specification, §9).
