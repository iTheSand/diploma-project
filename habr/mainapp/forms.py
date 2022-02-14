from datetime import date, timedelta

from django import forms

from mainapp.models import Article, ArticleComment, ModeratorNotification
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from authapp.models import UserProfile, User, NotificationUsersAboutBlocking
from mainapp.models import ArticleComment


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('likes',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['categories'].label = 'Выберете категорию'
        self.fields['title'].label = 'Укажите заголовок статьи'
        self.fields['subtitle'].label = 'Укажите краткое описание статьи'
        self.fields['main_img'].label = 'Загрузите картинку к статье'
        self.fields['text'].label = 'Напишите статью'
        self.fields['categories'].widget.attrs['value'] = 'Укажите раздел'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'

    def clean_title(self):
        data = self.cleaned_data['title']
        split_data = data.split()
        for word in split_data:
            if len(word) > 35:
                print(split_data)
                raise forms.ValidationError("Максимальная длинна слова в заголовке не должна превышать 35 символов")
        return data

    def clean_subtitle(self):
        data = self.cleaned_data['subtitle']
        split_data = data.split()
        for word in split_data:
            if len(word) > 48:
                print(split_data)
                raise forms.ValidationError("Максимальная длинна слова в описании не должна превышать 48 символов")
        return data

    # """ временно спрятал, не удаляйте пжлст"""
    # def clean_text(self):
    #     data = self.cleaned_data['text']
    #     split_data = data.split()
    #     for word in split_data:
    #         if len(word) > 84:
    #             print(split_data)
    #             raise forms.ValidationError("Максимальная длинна слова в статье не должна превышать 84 символа")
    #     return data


class CreationCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ('article_comment', 'text', 'user')

    def __init__(self, *args, **kwargs):
        super(CreationCommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'Напишите свой комментарий'
        self.fields['text'].widget.attrs['name'] = 'text'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            self.fields['text'].widget.attrs['class'] = 'comment_input'


class SearchForm(forms.Form):
    query = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs['placeholder'] = 'Искать здесь...'
        self.fields['query'].widget.attrs['class'] = 'search'


# --_--
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ivanov2019'
        self.fields['email'].widget.attrs['placeholder'] = 'ivanov2019@gmail.com'
        self.fields['password'].widget.attrs['placeholder'] = ' • • • • • • • • • •'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'form-input'


class UserProfileForm(UserCreationForm):
    # class UserProfileEditForm(UserChangeForm):
    """Чтение и изменение объекта пользователя"""

    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # self.fields['user'].widget = forms.HiddenInput()
        self.fields['name'].widget.attrs['placeholder'] = 'Имя Фамилия'
        self.fields['name'].widget.attrs['type'] = 'text'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['birthday'].widget.attrs['name'] = 'birthday'
        self.fields['birthday'].widget = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})
        # self.fields['bio'].widget.attrs['type'] = 'textarea'
        self.fields['bio'].widget = forms.Textarea(attrs={'rows': 3, 'cols:': 60})
        self.fields['bio'].widget.attrs['name'] = 'bio'
        self.fields['bio'].widget.attrs['placeholder'] = 'Краткое описание'
        self.fields['avatar'].widget.attrs['name'] = 'avatar'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'inputFild'


class UserProfileEditForm(forms.ModelForm):
    """Чтение и изменение объекта пользователя"""

    class Meta:
        model = UserProfile
        fields = ('name', 'birthday', 'bio', 'avatar')

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Имя Фамилия'
        self.fields['name'].widget.attrs['type'] = 'text'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['birthday'].widget.attrs['name'] = 'birthday'
        self.fields['birthday'].widget = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})
        # self.fields['bio'].widget.attrs['type'] = 'textarea'
        self.fields['bio'].widget = forms.Textarea(attrs={'rows': 3, 'cols:': 60})
        self.fields['bio'].widget.attrs['name'] = 'bio'
        self.fields['bio'].widget.attrs['placeholder'] = 'Краткое описание'
        self.fields['avatar'].widget.attrs['name'] = 'avatar'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'inputFild'

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        # return_date = datetime.date.today() + datetime.timedelta(days=5)
        # 2555 - 7 лет
        dates = date.today() - timedelta(days=2555)
        if data > dates:
            raise forms.ValidationError("Вы слишком молоды!")
        return data


class ModeratorNotificationEditForm(forms.ModelForm):
    class Meta:
        model = ModeratorNotification
        fields = ('responsible_moderator', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsible_moderator'].widget = forms.HiddenInput()
        self.fields['status'].widget = forms.HiddenInput()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''


class MessageEditForm(forms.ModelForm):
    class Meta:
        model = NotificationUsersAboutBlocking
        fields = ('is_read',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_read'].widget = forms.HiddenInput()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
            field.help_text = ''
