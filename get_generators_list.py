"""
Run in top level of libEnsemble repo to extract list of generators as json file.
Output goes in data/generators.json

"""
import os
import ast
import json

gen_dir = "libensemble/gen_funcs"
result = {}

for fname in os.listdir(gen_dir):
    if fname.endswith(".py") and not fname.startswith("_"):
        modname = fname[:-3]
        path = os.path.join(gen_dir, fname)

        with open(path, "r") as f:
            source = f.read()

        tree = ast.parse(source, filename=fname)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        if isinstance(node.value, (ast.List, ast.Tuple)):
                            result[modname] = [elt.s for elt in node.value.elts if isinstance(elt, ast.Str)]

# Save to JSON
with open("generators.json", "w") as out:
    json.dump(result, out, indent=2)
