"""Evaluate the rules for the Googlebot product token in a fetched robots.txt."""

import re
from urllib.parse import quote

UNRESERVED = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")


def normalize_path(value):
    def normalize_escape(match):
        character = chr(int(match[0][1:], 16))
        return character if character in UNRESERVED else match[0].upper()

    value = quote(value, safe="/%?&=+!$'()*,:;[]@")
    return re.sub(r"%[0-9a-fA-F]{2}", normalize_escape, value)


def matches_rule(path, pattern):
    anchored = pattern.endswith("$")
    pattern = pattern[:-1] if anchored else pattern
    literal = pattern.split("*")
    if not path.startswith(literal[0]):
        return False
    if len(literal) == 1:
        return not anchored or path == pattern

    position = len(literal[0])
    for segment in literal[1:-1] if anchored else literal[1:]:
        found = path.find(segment, position)
        if found == -1:
            return False
        position = found + len(segment)
    if anchored:
        return path.endswith(literal[-1]) and len(path) - len(literal[-1]) >= position
    return True


def googlebot_rules(source):
    agents, rules = [], []
    groups = []
    for line in source.splitlines():
        name, separator, value = line.partition("#")[0].partition(":")
        if not separator:
            continue
        name, value = name.strip().lower(), value.strip()
        if name == "user-agent" and value:
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value.split()[0].lower())
        elif agents and name in {"allow", "disallow"}:
            rules.append((name == "allow", value))
    groups.append((agents, rules))
    specific = any("googlebot" in agents or "googlebot*" in agents for agents, _ in groups)
    tokens = {"googlebot", "googlebot*"} if specific else {"*"}
    return [
        (allowed, normalize_path(pattern))
        for agents, rules in groups if tokens.intersection(agents)
        for allowed, pattern in rules if pattern.startswith("/")
    ]


def googlebot_decision(path, rules):
    normalized = normalize_path(path)
    # A longer matching rule wins; Allow wins at equal specificity.
    matches = ((len(pattern), allowed, pattern) for allowed, pattern in rules if matches_rule(normalized, pattern))
    _, allowed, pattern = max(matches, default=(0, True, None))
    return {"googlebot_allowed": allowed, "matching_rule": pattern}
