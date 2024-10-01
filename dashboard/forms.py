from django import forms
from .models import Site_Settings
from order.models import Product


class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputName', 'placeholder': 'Enter Product Name',
    }))
    class Meta:
        model = Product
        fields = ['name']


class WebsiteSettingsForm(forms.ModelForm):
    fav_icon = forms.ImageField(max_length=50, required=False, widget=forms.FileInput(attrs={
        'class': 'form-control', 'id': 'inputFavIcon'
    }))
    logo = forms.ImageField(max_length=50, required=False, widget=forms.FileInput(attrs={
        'class': 'form-control', 'id': 'inputLogo'
    }))
    website_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputWebsiteName', 'placeholder': 'Enter website name',
    }))
    website_title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputWebsiteTitle', 'placeholder': 'Enter website title',
    }))
    copyright_company = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputCompanyName', 'placeholder': 'Enter company name',
    }))
    copyright_year = forms.CharField(max_length=4, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputCopyrightYear', 'placeholder': 'Enter copyright year',
    }))
    class Meta:
        model = Site_Settings
        fields = ['website_name', 'website_title', 'copyright_company', 'copyright_year']
    
    def __init__(self, *args, **kwargs):
        super(WebsiteSettingsForm, self).__init__(*args, **kwargs)
        self.fields['fav_icon'].help_text = "Leave blank if you don't want to change the fav icon"
        self.fields['logo'].help_text = "Leave blank if you don't want to change the logo"
    
    def clean_fav_icon(self):
        fav_icon = self.cleaned_data.get('fav_icon')
        if fav_icon:
            return fav_icon
        return None
    
    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo:
            return logo
        return None
    
    


