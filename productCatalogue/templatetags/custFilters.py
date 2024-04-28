from django import template

register = template.Library()


@register.filter(name="parseBoolData")
def parseBoolData(value):
    return "Yes" if value == True else "No"


@register.filter(name="defaultChecked")
def defaultChecked(id, args):
    return "checked" if args.get(id) == "checked" else ""


@register.filter(name="arrayLen")
def arrayLen(arr):
    return len(arr)
