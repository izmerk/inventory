import jingo


@jingo.register.filter
def url(view_name, *args, **kwargs):
    from django.core.urlresolvers import reverse, NoReverseMatch
    try:
        return reverse(view_name, args=args, kwargs=kwargs)
    except NoReverseMatch:
        try:
            project_name = 'inventory'
            return reverse(project_name + '.' + view_name,
                           args=args, kwargs=kwargs)
        except NoReverseMatch:
            return ''


@jingo.register.filter
def humanized_class_name(obj, *args, **kwargs):
    """
    Adds spaces to camel-case class names.
    """
    humanized = ""

    class_name = obj.__class__.__name__

    # insert space between every camel hump
    for i in range(len(class_name)):
        humanized += class_name[i]
        if i + 1 < len(class_name) and class_name[i].islower() and class_name[i + 1].isupper():
            humanized += ' '

    return humanized
