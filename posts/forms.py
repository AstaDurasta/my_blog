from django import forms
from posts.models import Category

class PostForm(forms.Form):
    header = forms.CharField(max_length=50, label="Заголовок")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label=None)
    text = forms.CharField(widget=forms.Textarea, label="Текст") 
    image = forms.ImageField(label="", required=False)
    uploaded_image = forms.CharField(widget=forms.HiddenInput(), required=False)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)