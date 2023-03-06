import string
import random


from django import forms


class WorkTableForm(forms.Form):
    worktable_name = forms.CharField(
        required = True, 
        max_length=70, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'exampleInputName',
            }
        )
    )



    worktable_imagen = forms.ImageField( 
        max_length=255, 
        required = False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'exampleInputImage',
                'placeholder': 'imagen',
                'aria-describedby' : "imageHelp"
            }
        )
    )

class ClassForm(forms.Form):
    class_name = forms.CharField(
        required = True, 
        max_length=70, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'exampleInputName',
            }
        )
    )

    class_description = forms.CharField(
        required = False, 
        max_length=250, 
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'exampleInputName',
            }
        )
    )



    class_imagen = forms.ImageField( 
        max_length=255, 
        required = False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'exampleInputImage',
                'placeholder': 'imagen',
                'aria-describedby' : "imageHelp"
            }
        )
    )

class AnnouncementForm(forms.Form):
    class_name = forms.CharField(
        required = True, 
        max_length=250, 
        widget=forms.HiddenInput(
            attrs={
                'name' : 'editor',
                'id' : 'hidden-input'
            }
        )
    )


class GenerateUrlForm(forms.Form):

    urlTemporal = "Holi"

    CHOICES = (('A', '1 día'),('B', '3 días'), ('C', '7 días'))

    worktable_invite_url_expiration = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id' : 'url_expiration'
                
            }
        )
    )


    def setURlTemporal(self, new_url):
        self.urlTemporal = new_url


class ClassRegister(forms.Form):
    

    student_name = forms.CharField(
        required = False, 
        max_length=40, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'validationInputName',
            }
        )
    )
    student_username = forms.CharField(
        required = True, 
        max_length=40, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'validationInputUsername',
                
            }
        )
    )

    # <input type="text" class="form-control" id="validationCustom02" value="{{user_username}}" required>

    student_email = forms.CharField(
        required=True,
        max_length=40,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'validationInputEmail',
                
            }
        )
    )







    # worktable_invite_url  = forms.CharField(
    #     required = True, 
    #     max_length=16, 
    #     disabled=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'id': 'urlGenerated',
    #             'value': 'https://guenara.com/a/' + __url_generation
    #         }
    #     )
    # )



  
    
