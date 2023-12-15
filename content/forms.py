from django import forms

from content.models import Publication


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        exclude = ('publication_date', 'author', )
