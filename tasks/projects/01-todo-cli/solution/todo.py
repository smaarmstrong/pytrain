"""todo — a tiny JSON-backed task manager (argparse + pathlib + json)."""
import argparse
import os
import sys

from storage import load, save


def build_parser():
    ap = argparse.ArgumentParser(prog="todo")
    ap.add_argument(
        "--data-file",
        default=os.environ.get("TODO_DATA_FILE", "todo.json"),
        help="path to the JSON data file",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    p.add_argument("text")
    p = sub.add_parser("list")
    p.add_argument("--pending", action="store_true")
    p = sub.add_parser("done")
    p.add_argument("id", type=int)
    p = sub.add_parser("delete")
    p.add_argument("id", type=int)
    return ap


def find(tasks, tid):
    for t in tasks:
        if t["id"] == tid:
            return t
    return None


def main(argv=None):
    args = build_parser().parse_args(argv)
    tasks = load(args.data_file)

    if args.cmd == "add":
        new_id = max((t["id"] for t in tasks), default=0) + 1
        tasks.append({"id": new_id, "text": args.text, "done": False})
        save(args.data_file, tasks)
        print(f"Added {new_id}: {args.text}")
        return 0

    if args.cmd == "list":
        for t in sorted(tasks, key=lambda t: t["id"]):
            if args.pending and t["done"]:
                continue
            mark = "x" if t["done"] else " "
            print(f"[{mark}] {t['id']} {t['text']}")
        return 0

    # done / delete
    task = find(tasks, args.id)
    if task is None:
        print(f"error: no task {args.id}", file=sys.stderr)
        return 1
    if args.cmd == "done":
        task["done"] = True
        save(args.data_file, tasks)
        print(f"Done {task['id']}: {task['text']}")
    else:
        tasks.remove(task)
        save(args.data_file, tasks)
        print(f"Deleted {task['id']}: {task['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
