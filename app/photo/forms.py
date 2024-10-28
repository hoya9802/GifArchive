from django import forms
from .models import GifArchive, Category

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search')

class GifUpdateForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Category 모델의 모든 객체를 가져옴
        empty_label='Choose the category',  # 빈 선택지 추가
        widget=forms.Select(attrs={'class': 'form-select'})  # 선택 필드에 추가 속성 부여
    )

    class Meta:
        model = GifArchive
        fields = ['category', 'name', 'gif_image']
    
class GifArchiveForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Category 모델의 모든 객체를 가져옴
        empty_label='Choose the category',  # 빈 선택지 추가
        widget=forms.Select(attrs={'class': 'form-select'})  # 선택 필드에 추가 속성 부여
    )
    class Meta:
        model = GifArchive
        fields = ['category', 'name', 'gif_image']