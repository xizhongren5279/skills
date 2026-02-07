#!/usr/bin/env python3
"""Validate JSON research plan structure."""

import json
import sys
from typing import Dict, List, Set

def validate_plan(plan: Dict) -> List[str]:
    """Validate plan structure and dependencies. Returns list of errors."""
    errors = []

    # Check required top-level fields
    required_fields = ['research_type', 'topic', 'objectives', 'tasks']
    for field in required_fields:
        if field not in plan:
            errors.append(f"Missing required field: {field}")

    if 'tasks' not in plan:
        return errors  # Can't continue without tasks

    # Check research_type value
    valid_types = ['company', 'industry', 'strategy', 'macro', 'quantitative']
    if plan.get('research_type') not in valid_types:
        errors.append(f"Invalid research_type: {plan.get('research_type')}")

    # Validate tasks
    task_ids: Set[int] = set()
    for i, task in enumerate(plan['tasks']):
        # Check required task fields
        task_required = ['id', 'description', 'dependencies']
        for field in task_required:
            if field not in task:
                errors.append(f"Task {i}: Missing required field '{field}'")

        # Check task ID
        if 'id' in task:
            task_id = task['id']
            if not isinstance(task_id, int) or task_id <= 0:
                errors.append(f"Task {i}: Invalid ID {task_id} (must be positive integer)")
            if task_id in task_ids:
                errors.append(f"Task {i}: Duplicate ID {task_id}")
            task_ids.add(task_id)

        # Check dependencies type
        if 'dependencies' in task:
            deps = task['dependencies']
            if not isinstance(deps, list):
                errors.append(f"Task {task.get('id', i)}: dependencies must be array")

    # Validate task IDs are sequential
    if task_ids:
        expected_ids = set(range(1, len(task_ids) + 1))
        if task_ids != expected_ids:
            errors.append(f"Task IDs not sequential: expected {expected_ids}, got {task_ids}")

    # Validate dependency references
    for task in plan['tasks']:
        if 'dependencies' in task and 'id' in task:
            task_id = task['id']
            for dep_id in task['dependencies']:
                if dep_id not in task_ids:
                    errors.append(f"Task {task_id}: Invalid dependency {dep_id}")
                if dep_id == task_id:
                    errors.append(f"Task {task_id}: Self-dependency not allowed")

    # Check for circular dependencies (topological sort)
    if not errors:  # Only check if structure is valid
        if has_circular_dependency(plan['tasks']):
            errors.append("Circular dependency detected")

    return errors

def has_circular_dependency(tasks: List[Dict]) -> bool:
    """Check for circular dependencies using DFS."""
    # Build adjacency list
    graph = {task['id']: task['dependencies'] for task in tasks}

    # Track visit states: 0=unvisited, 1=visiting, 2=visited
    state = {task_id: 0 for task_id in graph}

    def dfs(node: int) -> bool:
        if state[node] == 1:  # Currently visiting - cycle detected
            return True
        if state[node] == 2:  # Already visited
            return False

        state[node] = 1  # Mark as visiting
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
        state[node] = 2  # Mark as visited
        return False

    for node in graph:
        if state[node] == 0:
            if dfs(node):
                return True
    return False

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <plan.json>")
        sys.exit(1)

    plan_file = sys.argv[1]

    try:
        with open(plan_file, 'r', encoding='utf-8') as f:
            plan = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ File not found: {plan_file}")
        sys.exit(1)

    errors = validate_plan(plan)

    if errors:
        print(f"❌ Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"✅ Plan validation passed!")
        print(f"   Research Type: {plan['research_type']}")
        print(f"   Topic: {plan['topic']}")
        print(f"   Tasks: {len(plan['tasks'])}")

        # Calculate waves
        completed = set()
        wave_num = 1
        while len(completed) < len(plan['tasks']):
            current_wave = [
                task for task in plan['tasks']
                if task['id'] not in completed
                and all(dep in completed for dep in task['dependencies'])
            ]
            if not current_wave:
                break
            print(f"   Wave {wave_num}: Tasks {[t['id'] for t in current_wave]}")
            completed.update(t['id'] for t in current_wave)
            wave_num += 1

if __name__ == '__main__':
    main()
