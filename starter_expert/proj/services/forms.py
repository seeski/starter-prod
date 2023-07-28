from django import forms


class Upload_nmids_form(forms.Form):
    file = forms.FileField()


class QueryForm(forms.Form):

    query = forms.CharField()
    depth = forms.IntegerField()
