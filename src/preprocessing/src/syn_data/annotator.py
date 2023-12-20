#!/usr/bin/env python3

# Reads USPTO patent jsons and adds a functional list annotation to all smiles found.
# Saves json files with annotations back.

import json

# Imports
import os

import pandas as pd
import progressbar
from rdkit import Chem, RDLogger
from syn_data.path import ASSET_PATH

RDLogger.DisableLog("rdApp.*")

# import the filter list
filter_list = pd.read_csv(
    ASSET_PATH / "funcgroups_list.csv", names=("SMARTS", "label", "void")
)
filter_list["mols"] = filter_list.SMARTS.apply(Chem.MolFromSmarts)


def lister(mol):
    # substructure search
    results = []
    for i in range(len(filter_list)):
        if mol.HasSubstructMatch(filter_list.mols[i]):
            results.append(filter_list.label[i])
    results = [s.lower().strip() for s in results]
    return list(set(results))


def smi_to_list(smiles):
    if smiles == "None":
        return []
    else:
        try:
            mol = Chem.MolFromSmiles(smiles)
        except:  # noqa: E722
            return []
        if mol is None:
            return []
        else:
            return lister(mol)


# define paths for data

spath = "/datadrive/uspto_json/grants/"
fpath = "/datadrive/uspto_json/new_grants/"

if __name__ == "__main__":
    with progressbar.ProgressBar(max_value=2460) as bar:
        for f in list(os.scandir(spath))[::-1]:
            # print(f"File {i}")
            if f.is_file():
                with open(f.path) as user_file:
                    j = json.loads(user_file.read())
                    name = os.path.basename(f)
                    # print(f"In file {name}")
                    if "reaction" in j["reactionList"].keys():
                        for nx, x in enumerate(j["reactionList"]["reaction"]):
                            pl = x["productList"]["product"]
                            rl = x["reactantList"]["reactant"]

                            if isinstance(pl, dict):
                                if "identifier" in pl.keys():
                                    if len(pl["identifier"]) > 0:
                                        smi_p = pl["identifier"][0]["@value"]
                                        # print(smi_p, smi_to_list(smi_p))
                                        j["reactionList"]["reaction"][nx][
                                            "productList"
                                        ]["product"]["funcgroups"] = smi_to_list(smi_p)
                            elif isinstance(pl, list):
                                for nm, m in enumerate(pl):
                                    if "identifier" in m.keys():
                                        if (
                                            isinstance(m["identifier"], list)
                                            and len(m["identifier"]) > 0
                                        ):
                                            smi_p = m["identifier"][0]["@value"]
                                            # print(smi_p, smi_to_list(smi_p))
                                            j["reactionList"]["reaction"][nx][
                                                "productList"
                                            ]["product"][nm][
                                                "funcgroups"
                                            ] = smi_to_list(
                                                smi_p
                                            )

                            if isinstance(rl, dict):
                                if "identifier" in rl.keys():
                                    if len(rl["identifier"]) > 0:
                                        # print(type(rl["identifier"]), rl["identifier"])
                                        smi_r = rl["identifier"][0]["@value"]
                                        # print(smi_r, smi_to_list(smi_r))
                                        j["reactionList"]["reaction"][nx][
                                            "reactantList"
                                        ]["reactant"]["funcgroups"] = smi_to_list(smi_r)
                            elif isinstance(rl, list):
                                for nm, m in enumerate(rl):
                                    if "identifier" in m.keys():
                                        if (
                                            isinstance(m["identifier"], list)
                                            and len(m["identifier"]) > 0
                                        ):
                                            # print(type(m["identifier"]), m["identifier"])
                                            smi_r = m["identifier"][0]["@value"]
                                            # print(smi_r, smi_to_list(smi_r))
                                            j["reactionList"]["reaction"][nx][
                                                "reactantList"
                                            ]["reactant"][nm][
                                                "funcgroups"
                                            ] = smi_to_list(
                                                smi_r
                                            )

                with open(f"{fpath}{name}", "w+") as user_file:
                    json.dump(j, user_file, indent=4)
