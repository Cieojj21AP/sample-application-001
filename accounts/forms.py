from django import forms
from accounts.models import CustomUser

#
# ユーザー情報更新フォーム
#
class AccountsUpdateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'last_name', 
            'first_name',
            'zipcode',
            'address1',
            'address2',)
        labels = {
            'username':'UserName',
            'email':'E-mail',
            'last_name':'LastName',
            'first_name':'FirstName',
            'zipcode':'Zipcode',
            'address1':'Address1',
            'address2':'Address2',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Emailは編集不可
        self.fields['email'].widget.attrs['readonly'] = 'readonly'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'