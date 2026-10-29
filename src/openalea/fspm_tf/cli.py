"""
The fspm-tf command line:

    fspm-tf validate FILE...                    check .glb frames or sequences (scene.fspm.json); exit 1 on errors
    fspm-tf info FILE                           what a frame holds
    fspm-tf display FILE NAME... [-o OUT]       add display copies of variables (in place, or to OUT)
    fspm-tf display FILE --remove [-o OUT]      remove them
"""
import argparse
import sys

from openalea.fspm_tf import read, write
from openalea.fspm_tf.display import add_display, remove_display
from openalea.fspm_tf.validate import validate_file


def _validate(arguments) -> int:
    failed = False
    for path in arguments.files:
        report = validate_file(path)
        print(report)
        failed = failed or not report.ok
    return 1 if failed else 0


def _info(arguments) -> int:
    frame = read(arguments.file)
    print(f"{arguments.file}: time {frame.time} {frame.time_unit}, step {frame.step}, writer {frame.writer or '-'}")
    for data_structure in frame.data_structures:
        print(f"  {data_structure.id} ({data_structure.kind}{', ' + data_structure.model if data_structure.model else ''})")
        for entity_set in data_structure.entity_sets:
            rank = "" if entity_set.rank is None else f" rank {entity_set.rank}"
            print(f"    {entity_set.name}{rank}: {entity_set.count} entities, variables "
                  f"{', '.join(entity_set.variable_names()) or '-'}")
        for relation in data_structure.relations:
            print(f"    relation {relation.name} ({relation.source_set} -> {relation.target_set}): {relation.count}")
        if data_structure.scalars is not None:
            print(f"    scalars: {', '.join(data_structure.scalars.columns)}")
        for mesh in data_structure.meshes:
            print(f"    mesh {mesh.name}: {len(mesh.positions)} vertices, entity sets {', '.join(mesh.feature_rows)}"
                  f"{', display ' + ', '.join(mesh.display) if mesh.display else ''}")
    for mapping in frame.mappings:
        print(f"  mapping {mapping.name}: {mapping.source[0]}/{mapping.source[1]} -> "
              f"{mapping.target[0]}/{mapping.target[1]}, {mapping.count} pairs")
    return 0


def _display(arguments) -> int:
    frame = read(arguments.file)
    if arguments.remove:
        remove_display(frame, arguments.names or None)
    else:
        if not arguments.names:
            print("give the names of the variables to copy, or --remove", file=sys.stderr)
            return 2
        add_display(frame, arguments.names, entity_set=arguments.entity_set)
    write(arguments.output or arguments.file, frame)
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="fspm-tf", description="fspm-TF files: validate, inspect, display")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="check frames (.glb) or sequences (scene.fspm.json)")
    validate.add_argument("files", nargs="+")
    validate.set_defaults(run=_validate)
    info = commands.add_parser("info", help="what a frame holds")
    info.add_argument("file")
    info.set_defaults(run=_info)
    display = commands.add_parser("display", help="add or remove display copies of variables")
    display.add_argument("file")
    display.add_argument("names", nargs="*")
    display.add_argument("--entity-set", default=None, help="the entity set the variables come from")
    display.add_argument("--remove", action="store_true", help="remove display copies (all, or the names given)")
    display.add_argument("-o", "--output", default=None, help="write to this file instead of in place")
    display.set_defaults(run=_display)
    arguments = parser.parse_args(argv)
    return arguments.run(arguments)


if __name__ == "__main__":
    sys.exit(main())
