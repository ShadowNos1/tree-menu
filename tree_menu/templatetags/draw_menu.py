from django import template
from django.urls import reverse, NoReverseMatch
from ..models import MenuItem

register = template.Library()

@register.inclusion_tag("tree_menu/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    """Отрисовать меню по его уникальному имени.
    Выполняется ровно один запрос к БД  мы получаем все `MenuItem` для меню и собираем дерево в памяти."""
    request = context.get("request")
    items_qs = MenuItem.objects.filter(menu__name=menu_name).select_related("parent").order_by("order")
    items = list(items_qs)
    nodes_by_id = {}
    for item in items:
        resolved_url = ""
        if item.named_url:
            try:
                resolved_url = reverse(item.named_url)
            except NoReverseMatch:
                resolved_url = ""
        else:
            resolved_url = item.url or ""
        node = {"id": item.id, "title": item.title, "children": [], "parent_id": item.parent_id, "url": resolved_url, "item": item, "active": False, "expanded": False}
        nodes_by_id[item.id] = node
    roots = []
    for node in nodes_by_id.values():
        pid = node["parent_id"]
        if pid and pid in nodes_by_id:
            nodes_by_id[pid]["children"].append(node)
        else:
            roots.append(node)
    active_node = None
    if request is not None:
        path = request.path
        best_len = -1
        for node in nodes_by_id.values():
            url = node["url"]
            if not url:
                continue
            if path == url:
                match = True
            else:
                if url == "/":
                    match = (path == "/")
                else:
                    match = path.startswith(url.rstrip("/") + "/")
            if match and len(url) > best_len:
                active_node = node
                best_len = len(url)
    if active_node:
        active_node["active"] = True
        pid = active_node["parent_id"]
        while pid and pid in nodes_by_id:
            nodes_by_id[pid]["expanded"] = True
            pid = nodes_by_id[pid]["parent_id"]
        for child in active_node["children"]:
            child["expanded"] = True
    return {"menu_name": menu_name, "nodes": roots, "request": request}
