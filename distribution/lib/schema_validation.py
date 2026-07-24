"""Dependency-free JSON Schema validation for Stewards contract fixtures.

This implements the complete keyword subset used by the provisioner v1
schemas and their common-types dependency. It is a test/verification utility,
not a replacement schema dialect.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Optional


class SchemaValidationError(ValueError):
    """A document does not satisfy its complete checked-in schema."""


class Validator:
    """Resolve local schema references and validate the used 2020-12 subset."""

    def __init__(self, schema_root: Path) -> None:
        self.schema_root = schema_root
        self.documents: dict[str, dict[str, Any]] = {}

    def load(self, name: str) -> dict[str, Any]:
        """Load and cache one checked-in schema document."""
        if name not in self.documents:
            value = json.loads(
                (self.schema_root / name).read_text(encoding="utf-8")
            )
            if not isinstance(value, dict):
                raise SchemaValidationError(f"{name}: schema is not an object")
            self.documents[name] = value
        return self.documents[name]

    def resolve_pointer(
        self,
        document: dict[str, Any],
        pointer: str,
        where: str,
    ) -> dict[str, Any]:
        """Resolve one RFC 6901 schema pointer."""
        value: Any = document
        if pointer:
            if not pointer.startswith("/"):
                raise SchemaValidationError(f"{where}: invalid schema pointer")
            for raw_part in pointer[1:].split("/"):
                part = raw_part.replace("~1", "/").replace("~0", "~")
                if not isinstance(value, dict) or part not in value:
                    raise SchemaValidationError(
                        f"{where}: unresolved schema pointer"
                    )
                value = value[part]
        if not isinstance(value, dict):
            raise SchemaValidationError(
                f"{where}: schema pointer does not select an object"
            )
        return value

    def resolve_ref(
        self,
        reference: str,
        current_name: str,
    ) -> tuple[dict[str, Any], str]:
        """Resolve a local or sibling-file reference."""
        file_name, separator, fragment = reference.partition("#")
        target_name = file_name or current_name
        target = self.load(target_name)
        pointer = fragment if separator else ""
        return self.resolve_pointer(target, pointer, reference), target_name

    def fail(self, path: str, message: str) -> None:
        """Raise one deterministic validation error."""
        raise SchemaValidationError(f"{path}: {message}")

    def type_matches(self, expected: str, value: Any) -> bool:
        """Apply JSON type semantics without treating booleans as integers."""
        if expected == "object":
            return isinstance(value, dict)
        if expected == "array":
            return isinstance(value, list)
        if expected == "string":
            return isinstance(value, str)
        if expected == "integer":
            return isinstance(value, int) and not isinstance(value, bool)
        if expected == "number":
            return isinstance(value, (int, float)) and not isinstance(
                value,
                bool,
            )
        if expected == "boolean":
            return isinstance(value, bool)
        if expected == "null":
            return value is None
        self.fail("$schema", f"unsupported type keyword {expected}")
        return False

    def trial(
        self,
        schema: dict[str, Any],
        instance: Any,
        current_name: str,
        path: str,
    ) -> tuple[bool, set[str], Optional[SchemaValidationError]]:
        """Try one applicator branch without losing its first error."""
        try:
            evaluated = self.validate(schema, instance, current_name, path)
            return True, evaluated, None
        except SchemaValidationError as exc:
            return False, set(), exc

    def validate(
        self,
        schema: dict[str, Any],
        instance: Any,
        current_name: str,
        path: str = "$",
    ) -> set[str]:
        """Validate one instance and return evaluated object-property names."""
        evaluated: set[str] = set()

        reference = schema.get("$ref")
        if isinstance(reference, str):
            target, target_name = self.resolve_ref(reference, current_name)
            evaluated.update(
                self.validate(target, instance, target_name, path)
            )

        all_of = schema.get("allOf", [])
        if isinstance(all_of, list):
            for branch in all_of:
                evaluated.update(
                    self.validate(branch, instance, current_name, path)
                )

        one_of = schema.get("oneOf")
        if isinstance(one_of, list):
            matches = [
                self.trial(branch, instance, current_name, path)
                for branch in one_of
            ]
            successful = [match for match in matches if match[0]]
            if len(successful) != 1:
                errors = [
                    str(match[2])
                    for match in matches
                    if match[2] is not None
                ]
                detail = errors[0] if errors else "multiple branches matched"
                self.fail(path, f"oneOf expected one match: {detail}")
            evaluated.update(successful[0][1])

        any_of = schema.get("anyOf")
        if isinstance(any_of, list):
            matches = [
                self.trial(branch, instance, current_name, path)
                for branch in any_of
            ]
            successful = [match for match in matches if match[0]]
            if not successful:
                detail = str(matches[0][2]) if matches else "no branches"
                self.fail(path, f"anyOf found no match: {detail}")
            for match in successful:
                evaluated.update(match[1])

        negated = schema.get("not")
        if isinstance(negated, dict):
            matched, _, _ = self.trial(
                negated,
                instance,
                current_name,
                path,
            )
            if matched:
                self.fail(path, "not schema matched")

        condition = schema.get("if")
        if isinstance(condition, dict):
            matched, condition_evaluated, _ = self.trial(
                condition,
                instance,
                current_name,
                path,
            )
            evaluated.update(condition_evaluated)
            selected = schema.get("then" if matched else "else")
            if isinstance(selected, dict):
                evaluated.update(
                    self.validate(selected, instance, current_name, path)
                )

        expected_type = schema.get("type")
        if isinstance(expected_type, str) and not self.type_matches(
            expected_type,
            instance,
        ):
            self.fail(path, f"expected {expected_type}")

        if "const" in schema and instance != schema["const"]:
            self.fail(path, "const mismatch")
        enum = schema.get("enum")
        if isinstance(enum, list) and instance not in enum:
            self.fail(path, "value is not in enum")

        if isinstance(instance, str):
            minimum_length = schema.get("minLength")
            maximum_length = schema.get("maxLength")
            if isinstance(minimum_length, int) and len(instance) < minimum_length:
                self.fail(path, "string is shorter than minLength")
            if isinstance(maximum_length, int) and len(instance) > maximum_length:
                self.fail(path, "string is longer than maxLength")
            pattern = schema.get("pattern")
            if isinstance(pattern, str) and re.search(pattern, instance) is None:
                self.fail(path, "string does not match pattern")

        minimum = schema.get("minimum")
        if (
            isinstance(minimum, (int, float))
            and isinstance(instance, (int, float))
            and not isinstance(instance, bool)
            and instance < minimum
        ):
            self.fail(path, "number is below minimum")

        if isinstance(instance, list):
            minimum_items = schema.get("minItems")
            maximum_items = schema.get("maxItems")
            if isinstance(minimum_items, int) and len(instance) < minimum_items:
                self.fail(path, "array is shorter than minItems")
            if isinstance(maximum_items, int) and len(instance) > maximum_items:
                self.fail(path, "array is longer than maxItems")
            if schema.get("uniqueItems") is True:
                canonical = [
                    json.dumps(
                        item,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                    for item in instance
                ]
                if len(canonical) != len(set(canonical)):
                    self.fail(path, "array items are not unique")
            item_schema = schema.get("items")
            if isinstance(item_schema, dict):
                for index, item in enumerate(instance):
                    self.validate(
                        item_schema,
                        item,
                        current_name,
                        f"{path}/{index}",
                    )
            contains = schema.get("contains")
            if isinstance(contains, dict):
                count = sum(
                    1
                    for item in instance
                    if self.trial(
                        contains,
                        item,
                        current_name,
                        path,
                    )[0]
                )
                minimum_contains = schema.get("minContains", 1)
                maximum_contains = schema.get("maxContains")
                if isinstance(minimum_contains, int) and count < minimum_contains:
                    self.fail(path, "contains matched too few items")
                if isinstance(maximum_contains, int) and count > maximum_contains:
                    self.fail(path, "contains matched too many items")

        if isinstance(instance, dict):
            required = schema.get("required", [])
            if isinstance(required, list):
                missing = [key for key in required if key not in instance]
                if missing:
                    self.fail(path, f"missing required property {missing[0]}")
            properties = schema.get("properties", {})
            if isinstance(properties, dict):
                for key, property_schema in properties.items():
                    if key in instance and isinstance(property_schema, dict):
                        self.validate(
                            property_schema,
                            instance[key],
                            current_name,
                            f"{path}/{key}",
                        )
                        evaluated.add(key)
            extras = set(instance) - set(properties)
            additional = schema.get("additionalProperties", True)
            if additional is False and extras:
                self.fail(path, f"unexpected property {sorted(extras)[0]}")
            if isinstance(additional, dict):
                for key in extras:
                    self.validate(
                        additional,
                        instance[key],
                        current_name,
                        f"{path}/{key}",
                    )
                    evaluated.add(key)
            if schema.get("unevaluatedProperties") is False:
                unevaluated = set(instance) - evaluated
                if unevaluated:
                    self.fail(
                        path,
                        f"unevaluated property {sorted(unevaluated)[0]}",
                    )
        return evaluated


def validate_document(
    repository_root: Path,
    schema_name: str,
    document: Any,
) -> None:
    """Validate a document against one complete provisioner schema."""
    schema_root = repository_root / "distribution" / "schemas"
    validator = Validator(schema_root)
    schema = validator.load(schema_name)
    validator.validate(schema, document, schema_name)
