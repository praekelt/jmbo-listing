from django.forms.widgets import RadioChoiceInput, RadioFieldRenderer, RadioSelect
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.encoding import force_text

from django.conf import settings


class RadioImageInput(RadioChoiceInput):

    def __init__(self, name, value, attrs, choice, index, image_path=None):
        super(RadioImageInput, self).__init__(name, value, attrs, choice, index)
        self.image_path = image_path

    def tag(self, attrs=None):
        result = super(RadioImageInput, self).tag(attrs)
        if self.image_path:
            aaa = " ".join([""" %s="%s" """ % (k, v) for k, v in attrs["image_attrs"].items()])
            return mark_safe(
                result + """<img src="%s%s" %s />""" % (
                    settings.STATIC_URL, self.image_path, aaa
                )
            )
        else:
            return result


class RadioImageFieldRenderer(RadioFieldRenderer):

    def render(self):
        id_ = self.attrs.get("id")
        output = []
        for i, choice in enumerate(self.choices):
            choice_value, choice_label, image_path = choice
            w = RadioImageInput(
                self.name, self.value, self.attrs.copy(), choice, i,
                image_path=image_path
            )
            output.append(format_html(self.inner_html,
                                      choice_value=force_text(w), sub_widgets=""))
        return format_html(
            self.outer_html,
            id_attr=format_html(""" id="{}" """, id_) if id_ else "",
            content=mark_safe("\n".join(output))
        )


class RadioImageSelect(RadioSelect):
    renderer = RadioImageFieldRenderer
