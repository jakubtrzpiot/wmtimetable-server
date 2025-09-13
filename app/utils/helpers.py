from .types import List, Dict, Any

def transpose(array: List[List[Any]]) -> List[List[Any]]:
    return [list(row) for row in zip(*array)]

def strip_null_values_from_edges(array: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    while array and array[0].get('subject') is None:
        array.pop(0)
    while array and array[-1].get('subject') is None:
        array.pop()
    return array
