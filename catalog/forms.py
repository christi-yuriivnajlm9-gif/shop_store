from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'address', 'comment']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': "Ім'я та прізвище"}),
            'phone': forms.TextInput(attrs={'placeholder': '+380...'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com (необов’язково)'}),
            'address': forms.TextInput(attrs={'placeholder': 'Місто, відділення НП або адреса'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Коментар до замовлення'}),
        }
