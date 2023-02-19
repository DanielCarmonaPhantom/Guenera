from django import forms

class WorkTableForm(forms.Form):
    worktable_name = forms.CharField(
        required = True, 
        max_length=200, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'exampleInputName',
            }
        )
    )



    # imagen = forms.ImageField( 
    #     max_length=255, 
    #     required = False,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'id': 'exampleInputImage',
    #             'placeholder': 'imagen',
    #             'aria-describedby' : "imageHelp"
    #         }
    #     )
    # )

    
