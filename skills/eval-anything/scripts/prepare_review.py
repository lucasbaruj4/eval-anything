#!/usr/bin/env python3
"""Prepare anonymous text pairs and a separate identity key."""

import argparse
import json
from pathlib import Path
import secrets


def require_text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def prepare(data):
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    criteria = data.get("criteria")
    if not isinstance(criteria, list):
        raise ValueError("criteria must be a list of strings")
    for criterion in criteria:
        require_text(criterion, "criterion")
    pairs = data.get("pairs")
    if not isinstance(pairs, list) or not pairs:
        raise ValueError("pairs must be a nonempty list")

    pair_ids = set()
    checked = []
    for pair in pairs:
        if not isinstance(pair, dict):
            raise ValueError("each pair must be an object")
        pair_id = require_text(pair.get("id"), "pair id")
        if pair_id in pair_ids:
            raise ValueError("pair ids must be unique")
        pair_ids.add(pair_id)
        prompt = require_text(pair.get("prompt"), "prompt")
        outputs = pair.get("outputs")
        if not isinstance(outputs, list) or len(outputs) != 2:
            raise ValueError("each pair must contain exactly two outputs")
        for output in outputs:
            if not isinstance(output, dict):
                raise ValueError("each output must be an object")
            for field in ("condition", "model", "text"):
                require_text(output.get(field), field)
        if outputs[0]["condition"] == outputs[1]["condition"]:
            raise ValueError("each pair must compare different conditions")
        if outputs[0]["model"] != outputs[1]["model"]:
            raise ValueError("use the same model for both conditions")
        checked.append((pair_id, prompt, outputs))

    random = secrets.SystemRandom()
    random.shuffle(checked)
    items = []
    identities = {}
    for index, (pair_id, prompt, original) in enumerate(checked, start=1):
        outputs = list(original)
        random.shuffle(outputs)
        label = f"Item {index}"
        items.append({"label": label, "prompt": prompt,
                      "A": outputs[0]["text"], "B": outputs[1]["text"]})
        identities[label] = {
            "pair_id": pair_id,
            **{side: {field: output[field] for field in ("condition", "model")}
               for side, output in zip(("A", "B"), outputs)},
        }
    return {"criteria": criteria, "items": items}, identities


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON file with criteria and paired outputs")
    parser.add_argument("destination", type=Path, help="new folder for review copies and a private key")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        pack, key = prepare(data)
        args.destination.mkdir(mode=0o700)
        review = args.destination / "review"
        private = args.destination / "private"
        review.mkdir()
        private.mkdir(mode=0o700)
        for path, content in ((review / "pack.json", pack), (private / "key.json", key)):
            with path.open("x", encoding="utf-8") as file:
                json.dump(content, file, ensure_ascii=False, indent=2)
                file.write("\n")
    except (OSError, ValueError) as error:
        parser.exit(2, f"Cannot prepare review: {error}\n")
    print(f"Review file: {review / 'pack.json'}")
    print(f"Private key, keep from reviewers: {private / 'key.json'}")


if __name__ == "__main__":
    main()
