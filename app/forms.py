from django import forms
from .models import Order, Product
from django.contrib.auth.forms import AuthenticationForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'product_name', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'onchange': 'calculate_order_value()'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set the choices for the product_name dropdown from the database
        self.fields['product_name'].queryset = Product.objects.all()

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if not product_name:
            raise forms.ValidationError("Please select a valid product.")
        return product_name

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Username'
        }),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Password'
        }),
        label="Password"
    )