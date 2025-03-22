Item = dict[str, str | int]


def use_item(item: Item) -> str:
    if item["type"] == "potion":
        return f"Grabbed potion with color {item.get('color', 'unknown')}"
    elif item["type"] == "scroll":
        return f"Grabbed scroll with spell {item.get('spell_name', 'unknown')}"
    elif item["type"] == "weapon":
        return f"Grabbed weapon named {item.get('name', 'unknown')}"
    else:
        raise ValueError(f"Unknown item type: {item}")
