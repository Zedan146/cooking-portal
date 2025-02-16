from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import Post, Comment


class PostAddForm(forms.ModelForm):
    """Форма для добавления новой статьи от пользователя"""

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }


class LoginForm(AuthenticationForm):
    """Форма для аунтификации пользователя"""
    username = forms.CharField(label='Имя пользователя',
                               max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                               max_length=150,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(max_length=150,
                               label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label='Электронная почта',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Электронная почта'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Повторите пароль'}))


class CommentForm(forms.ModelForm):
    """Форма для написания комментариев"""

    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш комментарий'
            })
        }


class ChangePasswordForm(PasswordChangeForm):
    """Форма для смены пароля"""

    old_password = forms.CharField(label='Старый пароль',
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Повторите пароль',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))
