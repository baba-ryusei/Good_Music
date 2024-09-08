from django import forms
from .models import Group
from .models import Song

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        labels = {
            'name': 'グループ名',
        }

class SongForm(forms.ModelForm):
    group_name = forms.CharField(label='グループ名', required=False)
    class Meta:
        model = Song
        fields = ['title','url']
        labels = {
            'title': '曲名',
            'url': '曲のURL'
        }
