from django import forms

AXIS_CHOICES = [
    ('No', 'No'),
    ('Si', 'Si'),
]

class VizForm(forms.Form):
    serie1 = forms.CharField(label='Serie1', max_length=20,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                             }))
    serie2 = forms.CharField(label='Serie2', max_length=20,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                             }),
                             required=False)
    serie3 = forms.CharField(label='Serie3', max_length=20,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                             }),
                             required=False)
    serie4 = forms.CharField(label='Serie4', max_length=20,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                             }),
                             required=False)

    datepicker1 = forms.DateField(label='Start Date',
                                  input_formats=["%Y-%m", "%Y", "%Y-%m-%d"],
                                  widget=forms.TextInput(attrs={
                                      'class': 'form-control datepicker',
                                  }))
    datepicker2 = forms.DateField(label='End Date',
                                  input_formats=["%Y-%m", "%Y", "%Y-%m-%d"],
                                  widget=forms.TextInput(attrs={
                                      'class': 'form-control datepicker',
                                  }))

    color_fondo = forms.CharField(label='color_fondo', max_length=20,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                 }))

    Marcar_recesiones = forms.CharField(label='Marcar_recesiones',
                                      widget=forms.Select(
                                      choices=AXIS_CHOICES,
                                      attrs={'class': 'form-control'}))

    Linea_cero = forms.CharField(label='Linea_cero',
                                      widget=forms.Select(
                                      choices=AXIS_CHOICES,
                                      attrs={'class': 'form-control'}))

    Eje_secundario2 = forms.CharField(label='Eje_secundario2',
                                     widget=forms.Select(
                                         choices=AXIS_CHOICES,
                                         attrs={'class': 'form-control'}))
    Eje_secundario3 = forms.CharField(label='Eje_secundario3',
                                      widget=forms.Select(
                                          choices=AXIS_CHOICES,
                                          attrs={'class': 'form-control'}))
    Eje_secundario4 = forms.CharField(label='Eje_secundario4',
                                      widget=forms.Select(
                                          choices=AXIS_CHOICES,
                                          attrs={'class': 'form-control'}))
    Tipo1 = forms.CharField(label='Tipo1', max_length=20,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                            }))
    Tipo2 = forms.CharField(label='Tipo2', max_length=20,
                          widget=forms.TextInput(attrs={
                              'class': 'form-control',
                          }))
    Tipo3 = forms.CharField(label='Tipo3', max_length=20,
                          widget=forms.TextInput(attrs={
                              'class': 'form-control',
                          }))
    Tipo4 = forms.CharField(label='Tipo4', max_length=20,
                          widget=forms.TextInput(attrs={
                              'class': 'form-control',
                          }))

    color_linea1 = forms.CharField(label='color_linea1', max_length=20,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                            }))
    color_linea2 = forms.CharField(label='color_linea2', max_length=20,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                            }))
    color_linea3 = forms.CharField(label='color_linea3', max_length=20,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                            }))
    color_linea4 = forms.CharField(label='color_linea4', max_length=20,
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                            }))


    def get_periodo(self):
        return "{}/{}".format(self.cleaned_data.get('datepicker1'),
                              self.cleaned_data.get('datepicker2'))
