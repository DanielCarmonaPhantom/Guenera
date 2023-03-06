from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()



class RegisterForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", required = True, min_length=4, max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'placeholder': 'Usuario'
        }))
    email = forms.EmailField(label="Correo Electrónico",required = True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'placeholder': 'example@exmaple.org'
        }))
    
    password = forms.CharField(label="Contraseña",required = True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        }))
    password2 = forms.CharField(
        label= 'Confirmar Contraseña',
        required = True, 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
        }))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya se encuentra en uso')
        
        if username.isspace():
            raise forms.ValidationError("El usuario no puede contener espacios")

        if not username.isalnum():
            raise forms.ValidationError('El usuario no puede contener espacios o caracteres')
        
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'El password no coincide')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )