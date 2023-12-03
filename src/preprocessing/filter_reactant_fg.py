import json
from pathlib import Path


def filter_reactant_fg(json_file):
    fg_list = [
        "alpha aryl carboxylic acid",
        "acidic groups",
        "primary amine",
        "secondary amine",
        "aldehyde",
        "ketone",
        "alcohol",
    ]
    with open(json_file, "r") as f:
        json_content = json.load(f)
    reaction_list = json_content["reactionList"].get("reaction")
    good_reactions = []
    if reaction_list:
        for reaction in reaction_list:
            reactant_fg = []
            if "reactant" in reaction["reactantList"].keys():
                reactant_list = reaction["reactantList"].get("reactant")
                # among reactant we want at list one of the fg_list exists
                if isinstance(reactant_list, list):
                    for reactant in reactant_list:
                        if "funcgroups" in reactant.keys():
                            reactant_fg.extend(reactant["funcgroups"])
                elif isinstance(reactant_list, dict):
                    reactant_fg.extend(reactant_list["funcgroups"])
            checker = any([fg in reactant_fg for fg in fg_list])
            if checker:
                good_reactions.append(reaction)
    print(f"after removing: {len(good_reactions)}")
    return good_reactions


if __name__ == "__main__":
    data_path = Path("/datadrive/uspto_json/new_grants/")
    prefix = "I2010"

    sum = 0
    print(f"there are {len(list(data_path.glob('I2010*.json')))}")
    for filepath in data_path.glob(f"{prefix}*.json"):
        good_reactions = filter_reactant_fg(filepath)
