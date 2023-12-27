from django import forms

from content.models import Publication


class StyleFormMixin:
    """
    Миксин для стилей формы
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != "is_active":
                field.widget.attrs['class'] = 'form-control'


class PublicationForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания и редактирования публикации
    """
    class Meta:
        model = Publication
        exclude = ('publication_date', 'author', 'views', )
