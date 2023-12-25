from django import forms

from content.models import Publication


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_active":
                field.widget.attrs['class'] = 'form-control'


class PublicationForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Publication
        exclude = ('publication_date', 'author', 'views', )
