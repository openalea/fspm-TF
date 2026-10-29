# Implementations

| Platform | Language | Where | Reads | Writes | Specification version |
|---|---|---|---|---|---|
| fspm-tf (reference) | Python | this repository, `src/fspm_tf` | yes | yes | 0.1 |
| openalea.metafspm | Python | planned: `openalea.metafspm.io.fspm_tf` (phase P2) | planned | planned | |
| CPlantBox | C++ / Python | planned (phase P4) | | | |
| GroIMP | Java | | | | |
| VirtualPlantLab | Julia | | | | |

An implementation is listed with the version it passes: it reads every conformance file as expected, and writes
files that the validator accepts (specification, §9).
