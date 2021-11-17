from django import forms


class AddSubjectCertificateForm(forms.Form):
    subject_name = forms.CharField()
