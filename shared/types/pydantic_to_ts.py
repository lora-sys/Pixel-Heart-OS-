#!/usr/bin/env python3
"""
Script to generate TypeScript interfaces from Pydantic schemas.
Primitive implementation - extracts class definitions and converts to TS.
"""
import ast
import sys
from pathlib import Path
from typing import Dict, Any

# Type mapping
PYTHON_TO_TS = {
    'str': 'string',
    'int': 'number',
    'float': 'number',
    'bool': 'boolean',
    'Any': 'any',
    'dict': 'Record<string, any>',
    'list': 'Array',
    'Dict': 'Record<string, any>',
    'List': 'Array',
    'Optional': 'null | ',
    'None': 'null',
    'datetime': 'string',
}

def parse_pydantic_model(source: str) -> Dict[str, Any]:
    """Extract fields from a Pydantic BaseModel class."""
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check if it inherits from BaseModel
            bases = [base.id if isinstance(base, ast.Name) else None for base in node.bases]
            if 'BaseModel' in bases:
                fields = {}
                for item in node.body:
                    if isinstance(item, ast.AnnAssign):
                        field_name = item.target.id if isinstance(item.target, ast.Name) else None
                        if field_name:
                            # Parse type annotation
                            annotation = ast.unparse(item.annotation) if hasattr(ast, 'unparse') else str(item.annotation)
                            fields[field_name] = annotation
                return {
                    'name': node.name,
                    'fields': fields
                }
    return {}

def python_type_to_ts(py_type: str) -> str:
    """Convert Python type annotation to TypeScript."""
    py_type = py_type.strip()

    # Handle Optional[T]
    if py_type.startswith('Optional['):
        inner = py_type[9:-1]  # Extract T from Optional[T]
        return f"{python_type_to_ts(inner)} | null"

    # Handle Union types like Union[str, None]
    if 'Union[' in py_type:
        # Simplified: just extract types
        return py_type  # TODO: proper conversion

    # Handle List[T] or list[T]
    if 'List[' in py_type or py_type.startswith('list['):
        inner = py_type[py_type.find('[')+1:-1]
        return f"{python_type_to_ts(inner)}[]"

    # Direct mapping
    for py, ts in PYTHON_TO_TS.items():
        if py in py_type:
            return ts.replace('{', '').replace('}', '')  # Simple cleanup

    # Unknown types remain as any
    return 'any'

def generate_ts_interface(model: Dict[str, Any]) -> str:
    """Generate TypeScript interface from model."""
    lines = [f"export interface {model['name']} {{"]
    for field_name, py_type in model['fields'].items():
        ts_type = python_type_to_ts(py_type)
        lines.append(f"  {field_name}: {ts_type};")
    lines.append("}")
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: pydantic_to_ts.py <schema_file.py> [output.ts]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.with_suffix('.ts')

    source = input_file.read_text()

    # Parse all models
    interfaces = []
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = [base.id if isinstance(base, ast.Name) else None for base in node.bases]
            if 'BaseModel' in bases:
                model = parse_pydantic_model(ast.unparse(node) if hasattr(ast, 'unparse') else source)
                if model:
                    interfaces.append(generate_ts_interface(model))

    output = "\n\n".join(interfaces)
    output_file.write_text(output)
    print(f"Generated {len(interfaces)} interfaces to {output_file}")

if __name__ == "__main__":
    main()
