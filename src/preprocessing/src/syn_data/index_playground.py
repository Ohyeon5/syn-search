# from llama_index.indices.composability import ComposableGraph
from syn_data.index_builder import build_index_per_file
from syn_data.path import MODULE_PATH

# In this script, explore different index loaders
# 1. JSON/XML loader
# 2. combine multiple indices
# 3. Test with examples

if __name__ == "__main__":
    data_root_dir = MODULE_PATH / ".." / ".." / ".." / ".." / "data"
    data_dir = data_root_dir / "uspto_json" / "grants"
    json_files = list(data_dir.glob("*.json"))

    val_set = [
        data_dir / "I20160906.json",
        data_dir / "I20160913.json",
        data_dir / "I20160920.json",
    ]

    save_dir = data_root_dir / "index"
    save_dir.mkdir(exist_ok=True)

    # Build index per file
    for json_file in val_set:
        build_index_per_file(
            json_file,
            save_dir / f"{str(json_file.name).split('.')[0]}.index",
        )

    # query from the index

    # # Combine indices
    # # todo what is ComposableGraph
    # grapg = ComposableGraph.from_indices()
