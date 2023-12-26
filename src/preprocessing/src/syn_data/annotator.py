#!/usr/bin/env python3

# Reads USPTO patent jsons and adds a functional list annotation to all smiles found.
# Saves json files with annotations back.

import json
from pathlib import Path
from typing import List

import pandas as pd
from rdkit import Chem, RDLogger
from syn_data.path import ASSET_PATH
from tqdm import tqdm

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


def smi_to_list(smiles: str) -> List:
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


def rxn_smi_to_desc(rxn_smi: str) -> str:
    """Reaction smiles to the functional group descriptive str
    Reaction smiles are composed of reactants + solvent -> product
    in the following format:
    reactant_1.reactant_2.reactant_3>solvent_1.solvent_2.solvent_3>product
    or
    reactant_1.reactant_2.reactant_3>>product

    Args:
        rxn_smi (str): reaction smiles

    Returns:
        str : reactions explained to chemically descriptive language
            e.g., reactant 1 [A, B, C] and reactant 2 [A, G, F], are combined to be
            [A, B, G, F] in solvent [L,M]
    """
    rs, ss, ps = rxn_smi.split(">")
    reactants = [smi_to_list(smi) for smi in rs.split(".")]
    solvents = [smi_to_list(smi) for smi in ss.split(".")]
    products = [smi_to_list(smi) for smi in ps.split(".")]
    return (
        "This reaction combines "
        + " ".join(
            [f"reactant_{ii}: {reactant}" for ii, reactant in enumerate(reactants)]
        )
        + " to be "
        + " ".join([f"product_{ii}: {prod}" for ii, prod in enumerate(products)])
        + " in "
        + " ".join([f"solvent_{ii}: {solv}" for ii, solv in enumerate(solvents)])
    )


def annotate_file(json_path: Path, save_dir: Path):
    """Annotate json file's smiles to list of functional groups
    then, save to json file in save_dir

    Args:
        json_path (Path): Path to the json file
        save_dir (Path): save dir
    """
    save_dir.mkdir(exist_ok=True, parents=True)
    with open(json_path) as user_file:
        j = json.loads(user_file.read())
        # print(f"In file {name}")
        if "reaction" in j["reactionList"].keys():
            for nx, x in enumerate(j["reactionList"]["reaction"]):
                # add rxn_smi_to_desc
                rxn_smiles = x["dl:reactionSmiles"]
                j["reactionList"]["reaction"][nx][
                    "dl:reactionSmilesDesc"
                ] = rxn_smi_to_desc(rxn_smiles)
                pl = x["productList"]["product"]
                rl = x["reactantList"]["reactant"]

                if isinstance(pl, dict):
                    if "identifier" in pl.keys():
                        if len(pl["identifier"]) > 0:
                            smi_p = pl["identifier"][0]["@value"]
                            # print(smi_p, smi_to_list(smi_p))
                            j["reactionList"]["reaction"][nx]["productList"]["product"][
                                "funcgroups"
                            ] = smi_to_list(smi_p)
                elif isinstance(pl, list):
                    for nm, m in enumerate(pl):
                        if "identifier" in m.keys():
                            if (
                                isinstance(m["identifier"], list)
                                and len(m["identifier"]) > 0
                            ):
                                smi_p = m["identifier"][0]["@value"]
                                # print(smi_p, smi_to_list(smi_p))
                                j["reactionList"]["reaction"][nx]["productList"][
                                    "product"
                                ][nm]["funcgroups"] = smi_to_list(smi_p)

                if isinstance(rl, dict):
                    if "identifier" in rl.keys():
                        if len(rl["identifier"]) > 0:
                            # print(type(rl["identifier"]), rl["identifier"])
                            smi_r = rl["identifier"][0]["@value"]
                            # print(smi_r, smi_to_list(smi_r))
                            j["reactionList"]["reaction"][nx]["reactantList"][
                                "reactant"
                            ]["funcgroups"] = smi_to_list(smi_r)
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
                                j["reactionList"]["reaction"][nx]["reactantList"][
                                    "reactant"
                                ][nm]["funcgroups"] = smi_to_list(smi_r)

    with open(f"{save_dir/json_path.name}", "w+") as user_file:
        json.dump(j, user_file, indent=4)


if __name__ == "__main__":
    # define paths for data
    spath = Path("/datadrive/uspto_json/grants/")
    fpath = Path("/datadrive/uspto_json/new_grants/")

    for f in tqdm(list(spath.glob("*.json"))):
        # print(f"File {i}")
        if f.is_file():
            annotate_file(f, fpath)
