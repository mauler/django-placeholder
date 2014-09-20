def get_template_name(request, obj):
    template_name = request.GET.get("template_name")

    if not template_name and obj:
        template_name = obj.template_name

    return template_name
