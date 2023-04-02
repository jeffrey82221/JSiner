"""
Processing Json files in a folder 

XXX:
- [X] args.jsonl -> `in`
"""
import os
from .filter import FileFilter
from .batch import Batcher
from .jskiner import InferenceEngine
from .reduce import SchemaReducer


class JsonFileProcessor:
    def __init__(self, args):
        self._args = args
        self._file_filter = FileFilter(
            set_size=args.cuckoo_size,
            dump_file_path=args.cuckoo_path,
            error_rate=args.cuckoo_fpr,
            verbose=args.verbose,
        )
        self._batcher = Batcher(batch_size=args.batch_size)
        self._engine = InferenceEngine(args.nworkers)
        if os.path.exists(args.cuckoo_path):
            with open(args.out, "r") as f:
                schema_string = f.read()
        else:
            schema_string = "Unknown()"
        self._reducer = SchemaReducer(schema_str=schema_string)

    def run(self):
        all_files = os.listdir(self._args.in_path)
        if self._args.verbose:
            print("number of files:", len(all_files))
        files = list(self._file_filter.connect(all_files))
        if self._args.verbose:
            print("number of new files:", len(files))
        paths = map(lambda x: f"{self._args.in_path}/{x}", files)
        jsons = map(JsonFileProcessor.path_to_json, paths)
        json_batches = self._batcher.connect(jsons)
        schema_strings = map(self._engine.run, json_batches)
        schema_str = self._reducer.reduce(schema_strings)
        self.update_filter(files)
        return schema_str

    @staticmethod
    def path_to_json(path):
        with open(path, "r") as f:
            result = f.read()
        return result

    def update_filter(self, files):
        updated_files = list(map(self._file_filter.insert, files))
        print("number of updated files:", len(updated_files))
        self._file_filter.save()
