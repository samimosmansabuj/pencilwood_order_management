from django import forms
from .models import Order, OrderRequest, Product, OrderCustomer, OrderItem
from account.models import Custom_User
from django.core.files.storage import default_storage
import os

# ----------------Order Section Start----------------
class OrderCustomerForm(forms.ModelForm):
    class Meta:
        model = OrderCustomer
        fields = ['company', 'name', 'phone_number', 'second_phone_number', 'source', 'product', 'logo', 'picture1']
        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'inputCompany', 'placeholder': 'Enter Company Name'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'inputName', 'placeholder': 'Enter Your Name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'inputPhone', 'placeholder': 'Enter Phone Number'
            }),
            'second_phone_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'inputSecondPhoneNumber', 'placeholder': 'Second Phone Number'
            }),
            'source': forms.Select(attrs={
                'class': 'form-control', 'id': 'inputSource'
            }),
            'product': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-inline', 'id': 'inputProduct'
            }),
            'logo': forms.URLInput(attrs={
                'class': 'form-control', 'id': 'inputLogo', 'placeholder': 'Enter Logo URL'
            }),
            'picture1': forms.URLInput(attrs={
                'class': 'form-control', 'id': 'inputPicture1', 'placeholder': 'Enter Picture URL'
            }),
        }
        labels = {
            'picture1': 'Picture 01',
        }
        
    def __init__(self, *args, **kwargs):
        super(OrderCustomerForm, self).__init__(*args, **kwargs)
        self.fields['company'].required = False
        self.fields['second_phone_number'].required = False
        self.fields['source'].required = False
        self.fields['product'].required = False
        self.fields['logo'].required = False
        self.fields['picture1'].required = False


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'delivery_address', 'special_instructions', 'advance_amount', 'delivery_charge', 'payment_number', 'transaction_id', 'payment_method', 'payment_status', 'status', 'urgent', 'work_assign', 'remark', 'delivery_date', 'delivery_charge_cost', 'design_file'
        ]

    delivery_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputDeliveryAddress', 'placeholder': 'Enter Delivery Address'
    }))

    special_instructions = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'id': 'inputSpecialInstructions', 'placeholder': 'Enter Special Instructions (optional)', 'rows': 3
    }))

    advance_amount = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'id': 'inputAdvanceAmount', 'placeholder': 'Enter Advance Amount'
    }))

    due_amount = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'id': 'inputDueAmount', 'readonly': 'readonly', 'placeholder': 'Calculated Due Amount'
    }))

    delivery_charge = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'id': 'inputDeliveryCharge', 'placeholder': 'Enter Delivery Charge'
    }))
    
    delivery_charge_cost = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'id': 'inputDeliveryChargeCost', 'placeholder': 'Enter Delivery Charge Cost'
    }))

    payment_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPaymentNumber', 'placeholder': 'Enter Payment Number'
    }))

    transaction_id = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputTransactionId', 'placeholder': 'Enter Transaction ID'
    }))

    payment_method = forms.ChoiceField(required=False, choices=Order.PAYMENT_METHOD, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputPaymentMethod'
    }))

    payment_status = forms.ChoiceField(required=False, choices=Order.PAYMENT_STATUS, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputPaymentStatus'
    }))

    status = forms.ChoiceField(required=False, choices=Order.STATUS, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputStatus'
    }))
    urgent = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-inline', 'id': 'inputUrgent'
    }))

    work_assign = forms.ModelChoiceField(required=False, queryset=Custom_User.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputWorkAssign'
    }))

    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'id': 'inputRemark', 'placeholder': 'Enter Remark (optional)', 'rows': 3
    }))

    delivery_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'form-control', 'id': 'inputDeliveryDate', 'placeholder': 'Select Delivery Date', 'type': 'date'
    }))
    design_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control', 'id': 'inputDesignFile', 'placeholder': 'Upload Design File'
    }))


class OrderStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'status', 'urgent', 'work_assign', 'remark', 'delivery_date', 'delivery_address', 'design_file'
        ]

    status = forms.ChoiceField(required=False, choices=Order.STATUS, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputStatus'
    }))
    urgent = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-inline', 'id': 'inputUrgent'
    }))
    work_assign = forms.ModelChoiceField(required=False, queryset=Custom_User.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputWorkAssign'
    }))
    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'id': 'inputRemark', 'placeholder': 'Enter Remark', 'rows': 3
    }))
    delivery_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputDeliveryAddress', 'placeholder': 'Enter Delivery Address'
    }))
    delivery_date = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'form-control', 'id': 'inputDeliveryDate', 'placeholder': 'Select Delivery Date', 'type': 'date'
    }))
    design_file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control', 'id': 'inputDesignFile', 'placeholder': 'Upload Design File'
    }))
    
    def clean(self):
        cleaned_data = super().clean()
        new_design_file = self.cleaned_data.get('design_file')
        clear_file = self.data.get('design_file-clear')

        if clear_file:
            if self.instance.design_file:
                self.instance.design_file.delete(save=False)

        elif new_design_file and new_design_file != self.instance.design_file:
            if self.instance.design_file:
                self.instance.design_file.delete(save=False)
        
        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            # order.add_missing_order_items()  # Add missing OrderItems if needed
            order.save()  # Save changes to Order instance
        return order


class OrderPaymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['advance_amount', 'delivery_charge', 'delivery_charge_cost']
    
    advance_amount = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'id': 'inputAdvanceAmount', 'placeholder': 'Enter Advance Amount'
    }))

    delivery_charge = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'id': 'inputDeliveryCharge', 'placeholder': 'Enter Delivery Charge'
    }))
    
    delivery_charge_cost = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'id': 'inputDeliveryChargeCost', 'placeholder': 'Enter Delivery Charge Cost'
    }))


class OrderItemUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'unit_price']
    
    quantity = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'id': 'inputQuantity', 'placeholder': 'Enter Quantity'
    }))

    unit_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'id': 'inputUnitPrice', 'placeholder': 'Enter Unit Price'
    }))

# ----------------Order Section End----------------


# ----------------Order Request Section Start----------------
class OrderRequestForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = [
            'company', 'name', 'phone_number', 'second_phone_number', 'source', 'product',
            'status', 'remark', 'logo', 'picture1',
            'picture2', 'picture3', 'picture4', 'picture5', 'work_assign'
        ]

    company = forms.CharField(label='Company Name', max_length=50, required=False, widget=forms.TextInput(attrs={
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
    
    second_phone_number = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputSecondPhoneNumber', 'placeholder': 'Second Phone Number'
    })
    )

    source = forms.ChoiceField(choices=OrderRequest.SOURCE, required=False, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputSource'
    })
    )

    product = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), required=False, widget=forms.CheckboxSelectMultiple(attrs={
        'class': 'form-check-inline', 'id': 'inputProduct'
    })
    )

    status = forms.ChoiceField(choices=OrderRequest.STATUS_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputStatus'
    })
    )

    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'id': 'inputRemark', 'placeholder': 'Enter Remark'
    })
    )
    
    work_assign = forms.ModelChoiceField(queryset=Custom_User.objects.all(), required=False, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputWorkAssign'
    }))

    logo = forms.URLField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputLogo', 'placeholder': 'Enter Logo URL'
    })
    )

    picture1 = forms.URLField(label="Picture 01", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture1', 'placeholder': 'Enter Picture 1 URL'
    })
    )

    picture2 = forms.URLField(label="Picture 02", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture2', 'placeholder': 'Enter Picture 2 URL'
    })
    )

    picture3 = forms.URLField(label="Picture 03", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture3', 'placeholder': 'Enter Picture 3 URL'
    })
    )

    picture4 = forms.URLField(label="Picture 04", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture4', 'placeholder': 'Enter Picture 4 URL'
    })
    )

    picture5 = forms.URLField(label="Picture 05", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture5', 'placeholder': 'Enter Picture 5 URL'
    })
    )


class OrderRequestStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = [
            'company', 'name', 'phone_number', 'second_phone_number', 'source', 'status', 'remark', 'product', 'work_assign'
        ]
    company = forms.CharField(required=False, label='Company Name', max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputCompany', 'placeholder': 'Enter Company Name'
    })
    )
    product = forms.ModelMultipleChoiceField(required=False, queryset=Product.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={
        'class': 'form-check-inline', 'id': 'inputProduct'
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
    second_phone_number = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputSecondPhoneNumber', 'placeholder': 'Second Phone Number'
    })
    )
    source = forms.ChoiceField(required=False, choices=OrderRequest.SOURCE, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputSource'
    })
    )
    status = forms.ChoiceField(required=False, choices=OrderRequest.STATUS_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputStatus'
    })
    )
    work_assign = forms.ModelChoiceField(queryset=Custom_User.objects.all(), required=False, widget=forms.Select(attrs={
        'class': 'form-control', 'id': 'inputWorkAssign'
    }))
    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control', 'id': 'inputRemark', 'placeholder': 'Enter Remark', 'rows': 3
    })
    )
  
    
class OrderRequestPictureUpdateForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = [
            'logo', 'picture1', 'picture2', 'picture3', 'picture4', 'picture5'
        ]
    logo = forms.URLField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputLogo', 'placeholder': 'Enter Logo URL'
    }))
    picture1 = forms.URLField(label="Picture 01", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture1', 'placeholder': 'Enter Picture 1 URL'
    }))
    picture2 = forms.URLField(label="Picture 02", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture2', 'placeholder': 'Enter Picture 2 URL'
    }))
    picture3 = forms.URLField(label="Picture 03", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture3', 'placeholder': 'Enter Picture 3 URL'
    }))
    picture4 = forms.URLField(label="Picture 04", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture4', 'placeholder': 'Enter Picture 4 URL'
    }))
    picture5 = forms.URLField(label="Picture 05", required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'inputPicture5', 'placeholder': 'Enter Picture 5 URL'
    })
    )


# ----------------Order Request Section End----------------
