#!/usr/bin/env python3
import json
import argparse
from pathlib import Path
from typing import List, Dict

DATA_FILE = Path.home() / ".hacktober_todo.json"

def load_todos() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text())

def save_todos(todos: List[Dict]):
    DATA_FILE.write_text(json.dumps(todos, indent=2))

def add_task(text: str):
    todos = load_todos()
    todos.append({"id": len(todos) + 1, "task": text, "done": False})
    save_todos(todos)

def list_tasks(show_all=False):
    todos = load_todos()
    for t in todos:
        if not show_all and t["done"]:
            continue
        print(f'[{ "x" if t["done"] else " " }] {t["id"]}: {t["task"]}')

def mark_done(task_id: int):
    todos = load_todos()
    for t in todos:
        if t["id"] == task_id:
            t["done"] = True
            break
    save_todos(todos)

def main():
    parser = argparse.ArgumentParser(description="Tiny TODO CLI")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("list")
    sub.add_parser("list-all")
    add = sub.add_parser("add")
    add.add_argument("text", nargs="+")
    done = sub.add_parser("done")
    done.add_argument("id", type=int)

    args = parser.parse_args()
    if args.cmd == "add":
        add_task(" ".join(args.text))
    elif args.cmd == "list":
        list_tasks(show_all=False)
    elif args.cmd == "list-all":
        list_tasks(show_all=True)
    elif args.cmd == "done":
        mark_done(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
