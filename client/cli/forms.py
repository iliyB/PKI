from django import forms

from cli.models import File


class AddSubjectCertificateForm(forms.Form):
    subject_name = forms.CharField()


class FileForm(forms.ModelForm):
    subject_name = forms.CharField()

    class Meta:
        model = File
        fields = ('subject_name', 'source_file')
