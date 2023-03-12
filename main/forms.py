from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import UserOfFacility, CaseReport

class DateInput(forms.DateInput):
    input_type = 'date'

# アカウント登録
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# アカウント編集
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# ログイン
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# 利用者
class UserOfFacilityForm(forms.ModelForm):
    class Meta:
        model = UserOfFacility
        fields = ("name", "organization", "group", "address", "tel", "mail", "handicap_name", "handicap_level")
        widgets = {
            'address': forms.Textarea(attrs={'rows':1}),
            'handicap_name': forms.Textarea(attrs={'rows':1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

# 事例記録
class CaseReportForm(forms.ModelForm):
    class Meta:
        model = CaseReport
        fields = ("occurrence_date", "case_name", "content", "method", "result")
        widgets = {
            "occurrence_date": DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'