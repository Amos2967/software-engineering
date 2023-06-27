from django import forms


# 报名表单
class SignUpForm(forms.Form):
    name = forms.CharField(label="姓名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    school = forms.CharField(label="在读学校", max_length=18, widget=forms.TextInput(attrs={'class': 'form-control'}))
    id = forms.CharField(label="学号", max_length=18, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    place_id = forms.CharField(label="考点编号", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    major = forms.CharField(label="专业", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ID_type = forms.CharField(label="证件类型", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ID_no = forms.CharField(label="证件号码", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    degree = forms.CharField(label="学历", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))