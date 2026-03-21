#!/usr/bin/env python3
"""
本体图操作：创建、查询、关联、验证。

用法：
    python ontology.py create --type Person --props '{"name":"Alice"}'
    python ontology.py get --id p_001
    python ontology.py query --type Task --where '{"status":"open"}'
    python ontology.py relate --from proj_001 --rel has_task --to task_001
    python ontology.py related --id proj_001 --rel has_task
    python ontology.py list --type Person
    python ontology.py delete --id p_001
    python ontology.py validate
"""

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_GRAPH_PATH = "memory/ontology/graph.jsonl"
DEFAULT_SCHEMA_PATH = "memory/ontology/schema.yaml"


def resolve_safe_path(
    user_path: str,
    *,
    root: Path | None = None,
    must_exist: bool = False,
    label: str = "path",
) -> Path:
    """在根目录内解析用户路径，拒绝根目录外的路径遍历。"""
    if not user_path or not user_path.strip():
        raise SystemExit(f"无效的 {label}：路径为空")

    safe_root = (root or Path.cwd()).resolve()
    candidate = Path(user_path).expanduser()
    if not candidate.is_absolute():
        candidate = safe_root / candidate

    try:
        resolved = candidate.resolve(strict=False)
    except OSError as exc:
        raise SystemExit(f"无效的 {label}：{exc}") from exc

    try:
        resolved.relative_to(safe_root)
    except ValueError:
        raise SystemExit(
            f"无效的 {label}：必须在工作区根目录 '{safe_root}' 内"
        )

    if must_exist and not resolved.exists():
        raise SystemExit(f"无效的 {label}：未找到文件 '{resolved}'")

    return resolved


def generate_id(type_name: str) -> str:
    """为实体生成唯一 ID。"""
    prefix = type_name.lower()[:4]
    suffix = uuid.uuid4().hex[:8]
    return f"{prefix}_{suffix}"


def load_graph(path: str) -> tuple[dict, list]:
    """从图文件中加载实体和关系。"""
    entities = {}
    relations = []
    
    graph_path = Path(path)
    if not graph_path.exists():
        return entities, relations
    
    with open(graph_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            op = record.get("op")
            
            if op == "create":
                entity = record["entity"]
                entities[entity["id"]] = entity
            elif op == "update":
                entity_id = record["id"]
                if entity_id in entities:
                    entities[entity_id]["properties"].update(record.get("properties", {}))
                    entities[entity_id]["updated"] = record.get("timestamp")
            elif op == "delete":
                entity_id = record["id"]
                entities.pop(entity_id, None)
            elif op == "relate":
                relations.append({
                    "from": record["from"],
                    "rel": record["rel"],
                    "to": record["to"],
                    "properties": record.get("properties", {})
                })
            elif op == "unrelate":
                relations = [r for r in relations 
                           if not (r["from"] == record["from"] 
                                  and r["rel"] == record["rel"] 
                                  and r["to"] == record["to"])]
    
    return entities, relations


def append_op(path: str, record: dict):
    """将操作追加到图文件。"""
    graph_path = Path(path)
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(graph_path, "a") as f:
        f.write(json.dumps(record) + "\n")


def create_entity(type_name: str, properties: dict, graph_path: str, entity_id: str = None) -> dict:
    """创建新实体。"""
    entity_id = entity_id or generate_id(type_name)
    timestamp = datetime.now(timezone.utc).isoformat()
    
    entity = {
        "id": entity_id,
        "type": type_name,
        "properties": properties,
        "created": timestamp,
        "updated": timestamp
    }
    
    record = {"op": "create", "entity": entity, "timestamp": timestamp}
    append_op(graph_path, record)
    
    return entity


def get_entity(entity_id: str, graph_path: str) -> dict | None:
    """根据 ID 获取实体。"""
    entities, _ = load_graph(graph_path)
    return entities.get(entity_id)


def query_entities(type_name: str, where: dict, graph_path: str) -> list:
    """根据类型和属性查询实体。"""
    entities, _ = load_graph(graph_path)
    results = []
    
    for entity in entities.values():
        if type_name and entity["type"] != type_name:
            continue
        
        match = True
        for key, value in where.items():
            if entity["properties"].get(key) != value:
                match = False
                break
        
        if match:
            results.append(entity)
    
    return results


def list_entities(type_name: str, graph_path: str) -> list:
    """列出指定类型的所有实体。"""
    entities, _ = load_graph(graph_path)
    if type_name:
        return [e for e in entities.values() if e["type"] == type_name]
    return list(entities.values())


def update_entity(entity_id: str, properties: dict, graph_path: str) -> dict | None:
    """更新实体属性。"""
    entities, _ = load_graph(graph_path)
    if entity_id not in entities:
        return None
    
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {"op": "update", "id": entity_id, "properties": properties, "timestamp": timestamp}
    append_op(graph_path, record)
    
    entities[entity_id]["properties"].update(properties)
    entities[entity_id]["updated"] = timestamp
    return entities[entity_id]


def delete_entity(entity_id: str, graph_path: str) -> bool:
    """删除实体。"""
    entities, _ = load_graph(graph_path)
    if entity_id not in entities:
        return False
    
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {"op": "delete", "id": entity_id, "timestamp": timestamp}
    append_op(graph_path, record)
    return True


def create_relation(from_id: str, rel_type: str, to_id: str, properties: dict, graph_path: str):
    """在实体之间创建关系。"""
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {
        "op": "relate",
        "from": from_id,
        "rel": rel_type,
        "to": to_id,
        "properties": properties,
        "timestamp": timestamp
    }
    append_op(graph_path, record)
    return record


def get_related(entity_id: str, rel_type: str, graph_path: str, direction: str = "outgoing") -> list:
    """获取关联实体。"""
    entities, relations = load_graph(graph_path)
    results = []
    
    for rel in relations:
        if direction == "outgoing" and rel["from"] == entity_id:
            if not rel_type or rel["rel"] == rel_type:
                if rel["to"] in entities:
                    results.append({
                        "relation": rel["rel"],
                        "entity": entities[rel["to"]]
                    })
        elif direction == "incoming" and rel["to"] == entity_id:
            if not rel_type or rel["rel"] == rel_type:
                if rel["from"] in entities:
                    results.append({
                        "relation": rel["rel"],
                        "entity": entities[rel["from"]]
                    })
        elif direction == "both":
            if rel["from"] == entity_id or rel["to"] == entity_id:
                if not rel_type or rel["rel"] == rel_type:
                    other_id = rel["to"] if rel["from"] == entity_id else rel["from"]
                    if other_id in entities:
                        results.append({
                            "relation": rel["rel"],
                            "direction": "outgoing" if rel["from"] == entity_id else "incoming",
                            "entity": entities[other_id]
                        })
    
    return results


def validate_graph(graph_path: str, schema_path: str) -> list:
    """根据 schema 约束验证图。"""
    entities, relations = load_graph(graph_path)
    errors = []
    
    # 如果存在 schema 则加载
    schema = load_schema(schema_path)
    
    type_schemas = schema.get("types", {})
    relation_schemas = schema.get("relations", {})
    global_constraints = schema.get("constraints", [])
    
    for entity_id, entity in entities.items():
        type_name = entity["type"]
        type_schema = type_schemas.get(type_name, {})
        
        # 检查必填属性
        required = type_schema.get("required", [])
        for prop in required:
            if prop not in entity["properties"]:
                errors.append(f"{entity_id}：缺少必填属性 '{prop}'")
        
        # 检查禁止属性
        forbidden = type_schema.get("forbidden_properties", [])
        for prop in forbidden:
            if prop in entity["properties"]:
                errors.append(f"{entity_id}：包含禁止属性 '{prop}'")
        
        # 检查枚举值
        for prop, allowed in type_schema.items():
            if prop.endswith("_enum"):
                field = prop.replace("_enum", "")
                value = entity["properties"].get(field)
                if value and value not in allowed:
                    errors.append(f"{entity_id}：'{field}' 必须是 {allowed} 之一，实际为 '{value}'")
    
    # 关系约束（类型 + 基数 + 无环性）
    rel_index = {}
    for rel in relations:
        rel_index.setdefault(rel["rel"], []).append(rel)
    
    for rel_type, rel_schema in relation_schemas.items():
        rels = rel_index.get(rel_type, [])
        from_types = rel_schema.get("from_types", [])
        to_types = rel_schema.get("to_types", [])
        cardinality = rel_schema.get("cardinality")
        acyclic = rel_schema.get("acyclic", False)
        
        # 类型检查
        for rel in rels:
            from_entity = entities.get(rel["from"])
            to_entity = entities.get(rel["to"])
            if not from_entity or not to_entity:
                errors.append(f"{rel_type}：关系引用了不存在的实体 ({rel['from']} -> {rel['to']})")
                continue
            if from_types and from_entity["type"] not in from_types:
                errors.append(
                    f"{rel_type}：来源实体 {rel['from']} 类型 {from_entity['type']} 不在 {from_types} 中"
                )
            if to_types and to_entity["type"] not in to_types:
                errors.append(
                    f"{rel_type}：目标实体 {rel['to']} 类型 {to_entity['type']} 不在 {to_types} 中"
                )
        
        # 基数检查
        if cardinality in ("one_to_one", "one_to_many", "many_to_one"):
            from_counts = {}
            to_counts = {}
            for rel in rels:
                from_counts[rel["from"]] = from_counts.get(rel["from"], 0) + 1
                to_counts[rel["to"]] = to_counts.get(rel["to"], 0) + 1
            
            if cardinality in ("one_to_one", "many_to_one"):
                for from_id, count in from_counts.items():
                    if count > 1:
                        errors.append(f"{rel_type}：来源实体 {from_id} 违反基数约束 {cardinality}")
            if cardinality in ("one_to_one", "one_to_many"):
                for to_id, count in to_counts.items():
                    if count > 1:
                        errors.append(f"{rel_type}：目标实体 {to_id} 违反基数约束 {cardinality}")
        
        # 无环检查
        if acyclic:
            graph = {}
            for rel in rels:
                graph.setdefault(rel["from"], []).append(rel["to"])
            
            visited = {}
            
            def dfs(node, stack):
                visited[node] = True
                stack.add(node)
                for nxt in graph.get(node, []):
                    if nxt in stack:
                        return True
                    if not visited.get(nxt, False):
                        if dfs(nxt, stack):
                            return True
                stack.remove(node)
                return False
            
            for node in graph:
                if not visited.get(node, False):
                    if dfs(node, set()):
                        errors.append(f"{rel_type}：检测到循环依赖")
                        break
    
    # 全局约束（有限执行）
    for constraint in global_constraints:
        ctype = constraint.get("type")
        relation = constraint.get("relation")
        rule = (constraint.get("rule") or "").strip().lower()
        if ctype == "Event" and "end" in rule and "start" in rule:
            for entity_id, entity in entities.items():
                if entity["type"] != "Event":
                    continue
                start = entity["properties"].get("start")
                end = entity["properties"].get("end")
                if start and end:
                    try:
                        start_dt = datetime.fromisoformat(start)
                        end_dt = datetime.fromisoformat(end)
                        if end_dt < start_dt:
                            errors.append(f"{entity_id}：结束时间必须大于等于开始时间")
                    except ValueError:
                        errors.append(f"{entity_id}：start/end 的日期时间格式无效")
        if relation and rule == "acyclic":
            # 已通过关系 schema 在上方执行
            continue
    
    return errors


def load_schema(schema_path: str) -> dict:
    """如果 schema 文件存在，从 YAML 加载。"""
    schema = {}
    schema_file = Path(schema_path)
    if schema_file.exists():
        import yaml
        with open(schema_file) as f:
            schema = yaml.safe_load(f) or {}
    return schema


def write_schema(schema_path: str, schema: dict) -> None:
    """将 schema 写入 YAML 文件。"""
    schema_file = Path(schema_path)
    schema_file.parent.mkdir(parents=True, exist_ok=True)
    import yaml
    with open(schema_file, "w") as f:
        yaml.safe_dump(schema, f, sort_keys=False)


def merge_schema(base: dict, incoming: dict) -> dict:
    """将传入的 schema 合并到基础 schema 中，追加列表并深度合并字典。"""
    for key, value in (incoming or {}).items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            base[key] = merge_schema(base[key], value)
        elif key in base and isinstance(base[key], list) and isinstance(value, list):
            base[key] = base[key] + [v for v in value if v not in base[key]]
        else:
            base[key] = value
    return base


def append_schema(schema_path: str, incoming: dict) -> dict:
    """将 schema 片段追加/合并到现有 schema 中。"""
    base = load_schema(schema_path)
    merged = merge_schema(base, incoming)
    write_schema(schema_path, merged)
    return merged


def main():
    parser = argparse.ArgumentParser(description="本体图操作")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # 创建
    create_p = subparsers.add_parser("create", help="创建实体")
    create_p.add_argument("--type", "-t", required=True, help="实体类型")
    create_p.add_argument("--props", "-p", default="{}", help="属性 JSON")
    create_p.add_argument("--id", help="实体 ID（未提供时自动生成）")
    create_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # 获取
    get_p = subparsers.add_parser("get", help="根据 ID 获取实体")
    get_p.add_argument("--id", required=True, help="实体 ID")
    get_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # 查询
    query_p = subparsers.add_parser("query", help="查询实体")
    query_p.add_argument("--type", "-t", help="实体类型")
    query_p.add_argument("--where", "-w", default="{}", help="过滤条件 JSON")
    query_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # 列表
    list_p = subparsers.add_parser("list", help="列出实体")
    list_p.add_argument("--type", "-t", help="实体类型")
    list_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # 更新
    update_p = subparsers.add_parser("update", help="更新实体")
    update_p.add_argument("--id", required=True, help="实体 ID")
    update_p.add_argument("--props", "-p", required=True, help="属性 JSON")
    update_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # 删除
    delete_p = subparsers.add_parser("delete", help="删除实体")
    delete_p.add_argument("--id", required=True, help="实体 ID")
    delete_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # 关联
    relate_p = subparsers.add_parser("relate", help="创建关系")
    relate_p.add_argument("--from", dest="from_id", required=True, help="来源实体 ID")
    relate_p.add_argument("--rel", "-r", required=True, help="关系类型")
    relate_p.add_argument("--to", dest="to_id", required=True, help="目标实体 ID")
    relate_p.add_argument("--props", "-p", default="{}", help="关系属性 JSON")
    relate_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # 查询关联
    related_p = subparsers.add_parser("related", help="获取关联实体")
    related_p.add_argument("--id", required=True, help="实体 ID")
    related_p.add_argument("--rel", "-r", help="关系类型过滤")
    related_p.add_argument("--dir", "-d", choices=["outgoing", "incoming", "both"], default="outgoing")
    related_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    
    # 验证
    validate_p = subparsers.add_parser("validate", help="验证图")
    validate_p.add_argument("--graph", "-g", default=DEFAULT_GRAPH_PATH)
    validate_p.add_argument("--schema", "-s", default=DEFAULT_SCHEMA_PATH)

    # Schema 追加
    schema_p = subparsers.add_parser("schema-append", help="追加/合并 schema 片段")
    schema_p.add_argument("--schema", "-s", default=DEFAULT_SCHEMA_PATH)
    schema_p.add_argument("--data", "-d", help="Schema 片段（JSON 格式）")
    schema_p.add_argument("--file", "-f", help="Schema 片段文件（YAML 或 JSON）")
    
    args = parser.parse_args()
    workspace_root = Path.cwd().resolve()

    if hasattr(args, "graph"):
        args.graph = str(
            resolve_safe_path(args.graph, root=workspace_root, label="graph 路径")
        )
    if hasattr(args, "schema"):
        args.schema = str(
            resolve_safe_path(args.schema, root=workspace_root, label="schema 路径")
        )
    if hasattr(args, "file") and args.file:
        args.file = str(
            resolve_safe_path(
                args.file, root=workspace_root, must_exist=True, label="schema 文件"
            )
        )
    
    if args.command == "create":
        props = json.loads(args.props)
        entity = create_entity(args.type, props, args.graph, args.id)
        print(json.dumps(entity, indent=2))
    
    elif args.command == "get":
        entity = get_entity(args.id, args.graph)
        if entity:
            print(json.dumps(entity, indent=2))
        else:
            print(f"未找到实体：{args.id}")
    
    elif args.command == "query":
        where = json.loads(args.where)
        results = query_entities(args.type, where, args.graph)
        print(json.dumps(results, indent=2))
    
    elif args.command == "list":
        results = list_entities(args.type, args.graph)
        print(json.dumps(results, indent=2))
    
    elif args.command == "update":
        props = json.loads(args.props)
        entity = update_entity(args.id, props, args.graph)
        if entity:
            print(json.dumps(entity, indent=2))
        else:
            print(f"未找到实体：{args.id}")
    
    elif args.command == "delete":
        if delete_entity(args.id, args.graph):
            print(f"已删除：{args.id}")
        else:
            print(f"未找到实体：{args.id}")
    
    elif args.command == "relate":
        props = json.loads(args.props)
        rel = create_relation(args.from_id, args.rel, args.to_id, props, args.graph)
        print(json.dumps(rel, indent=2))
    
    elif args.command == "related":
        results = get_related(args.id, args.rel, args.graph, args.dir)
        print(json.dumps(results, indent=2))
    
    elif args.command == "validate":
        errors = validate_graph(args.graph, args.schema)
        if errors:
            print("验证错误：")
            for err in errors:
                print(f"  - {err}")
        else:
            print("图结构验证通过。")
    
    elif args.command == "schema-append":
        if not args.data and not args.file:
            raise SystemExit("schema-append 需要 --data 或 --file 参数")
        
        incoming = {}
        if args.data:
            incoming = json.loads(args.data)
        else:
            path = Path(args.file)
            if path.suffix.lower() == ".json":
                with open(path) as f:
                    incoming = json.load(f)
            else:
                import yaml
                with open(path) as f:
                    incoming = yaml.safe_load(f) or {}
        
        merged = append_schema(args.schema, incoming)
        print(json.dumps(merged, indent=2))


if __name__ == "__main__":
    main()
