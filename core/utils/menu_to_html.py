text = """<li class="nav-item has-treeview {}">
    <a href="{}" class="nav-link {}">
    <i class="nav-icon {}"></i>
    <p>{}{}</p>
    </a>"""


def menu_to_html(menus, segmen: str, parent_id=0):
    resText = """<ul class="nav nav-treeview">"""
    if parent_id == 0:
        resText = """<ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu" data-accordion="false">"""
    for item in menus:
        menu_open = "menu-open" if item["segment"] in segmen else ""
        menu_active = "active" if item["segment"] in segmen else ""
        if len(item["children"]) > 0:
            resText = resText + text.format(
                menu_open,
                item["href"],
                menu_active,
                item["icon"],
                item["text"],
                '<i class="right fas fa-angle-left"></i>',
            )
            resText = resText + menu_to_html(item["children"], segmen, item["parent_id"])
        else:
            resText = resText + text.format(
                menu_open,
                item["href"],
                menu_active,
                item["icon"],
                item["text"],
                "",
            )
        resText = resText + "</li>"
    resText = resText + "</ul>"
    return resText
