
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User
from django import forms

from django.forms.widgets import PasswordInput, TextInput

# registration form


class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']



    def __init__(self, *args, **kwargs):

        super(CreateUserForm, self).__init__(*args, **kwargs)

        #mark email field required

        self.fields['email'].required = True


    #Email validation

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email = email).exists():

            raise forms.ValidationError('Diese Email ist ungültig')
        

        if len(email) >= 350:

            raise forms.ValidationError("Ihre Email ist zu lang")
        
        return email 
    


#login form

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


#update form

class UpdateUserForm(forms.ModelForm):

    password = None

    class Meta:

        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']

    def __init__(self, *args, **kwargs):

        super(UpdateUserForm, self).__init__(*args, **kwargs)

        #mark email field required

        self.fields['email'].required = True 


      #Email validation

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email = email).exclude(pk=self.instance.pk).exists():

            raise forms.ValidationError('Diese Email ist ungültig')
        

        if len(email) >= 350:

            raise forms.ValidationError("Ihre Email ist zu lang")
        
        return email

    