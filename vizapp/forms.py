from django import forms

class VizForm(forms.Form):
    serie1 = forms.CharField(label='Serie1', max_length=20,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Serie1',
                             }))
    serie2 = forms.CharField(label='Serie2', max_length=20,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Serie2',
                             }))
    serie3 = forms.CharField(label='Serie3', max_length=20,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Serie3',
                             }))
    serie4 = forms.CharField(label='Serie4', max_length=20,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Serie4',
                             }),
                             required=False)

    datepicker1 = forms.DateField(label='Start Date',
                                  input_formats=["%Y-%m", "%Y", "%Y-%m-%d"],
                                  widget=forms.TextInput(attrs={
                                      'class': 'form-control datepicker',
                                      'placeholder': 'Start Date',
                                  }))
    datepicker2 = forms.DateField(label='End Date',
                                  input_formats=["%Y-%m", "%Y", "%Y-%m-%d"],
                                  widget=forms.TextInput(attrs={
                                      'class': 'form-control datepicker',
                                      'placeholder': 'End Date',
                                  }))

    def get_periodo(self):
        return "{}/{}".format(self.cleaned_data.get('datepicker1'),
                              self.cleaned_data.get('datepicker2'))
