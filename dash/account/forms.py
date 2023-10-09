from django import forms
from django.contrib.auth.models import User
from django.forms import Widget
from django.utils.safestring import mark_safe


class PrependWidget(Widget):
    """ Widget that prepend boostrap-style span with data to specified base widget """

    def __init__(self, base_widget, data, *args, **kwargs):
        u"""Initialise widget and get base instance"""
        super(PrependWidget, self).__init__(*args, **kwargs)
        self.base_widget = base_widget(*args, **kwargs)
        self.data = data

    def render(self, name, value, attrs=None):
        u"""Render base widget and add bootstrap spans"""
        field = self.base_widget.render(name, value, attrs)
        return mark_safe((
            u'<div class="input-group mb-3">'
            u'  <div class="input-group-prepend">'
            u'    <span class="input-group-text" id="basic-addon1">%(data)s</span>'
            u'  </div>'
            u'  <input type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">'
            u'</div>'
        ) % {'field': field, 'data': self.data})


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    email = forms.CharField(label='Email address', required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if cd['email']:
            # cek email in table User
            if User.objects.filter(email=cd['email']).exists():
                raise forms.ValidationError(
                    'Email already exist. Use another one.')
        return cd
