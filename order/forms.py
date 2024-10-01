from django import forms
from .models import Order, OrderRequest, Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('__all__')



class OrderRequestForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = [
            'company', 'name', 'phone_number', 'source', 'product', 
            'status', 'remark', 'logo', 'picture1', 
            'picture2', 'picture3', 'picture4', 'picture5'
        ]
    
    company = forms.CharField(label='Company Name', max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control', 'id': 'inputCompany', 'placeholder': 'Enter Company Name'
        })
    )
    
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control', 'id': 'inputName', 'placeholder': 'Enter Name'
        })
    )
    
    phone_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control', 'id': 'inputPhoneNumber', 'placeholder': 'Enter Phone Number'
        })
    )
    
    source = forms.ChoiceField(choices=OrderRequest.SOURCE, widget=forms.Select(attrs={
            'class': 'form-control', 'id': 'inputSource'
        })
    )
    
    product = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=forms.SelectMultiple(attrs={
            'class': 'form-control', 'id': 'inputProduct'
        })
    )
    
    status = forms.ChoiceField(choices=OrderRequest.STATUS_CHOICES, widget=forms.Select(attrs={
            'class': 'form-control', 'id': 'inputStatus'
        })
    )
    
    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={
            'class': 'form-control', 'id': 'inputRemark', 'placeholder': 'Enter Remark'
        })
    )
    
    logo = forms.URLField(required=False, max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control', 'id': 'inputLogo', 'placeholder': 'Enter Logo URL'
        })
    )
    
    picture1 = forms.URLField(label="Picture 01", required=False, max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control', 'id': 'inputPicture1', 'placeholder': 'Enter Picture 1 URL'
        })
    )
    
    picture2 = forms.URLField(label="Picture 02", required=False, max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control', 'id': 'inputPicture2', 'placeholder': 'Enter Picture 2 URL'
        })
    )
    
    picture3 = forms.URLField(label="Picture 03", required=False, max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control', 'id': 'inputPicture3', 'placeholder': 'Enter Picture 3 URL'
        })
    )
    
    picture4 = forms.URLField(label="Picture 04", required=False, max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control', 'id': 'inputPicture4', 'placeholder': 'Enter Picture 4 URL'
        })
    )
    
    picture5 = forms.URLField(label="Picture 05", required=False, max_length=50, widget=forms.TextInput(attrs={
            'class': 'form-control', 'id': 'inputPicture5', 'placeholder': 'Enter Picture 5 URL'
        })
    )



class OrderRequestStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = [
            'source', 'status', 'remark'
        ]
    
    source = forms.ChoiceField(choices=OrderRequest.SOURCE, widget=forms.Select(attrs={
            'class': 'form-control', 'id': 'inputSource'
        })
    )
    status = forms.ChoiceField(choices=OrderRequest.STATUS_CHOICES, widget=forms.Select(attrs={
                'class': 'form-control', 'id': 'inputStatus'
            })
    )
    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={
            'class': 'form-control', 'id': 'inputRemark', 'placeholder': 'Enter Remark', 'rows': 3
        })
    )




