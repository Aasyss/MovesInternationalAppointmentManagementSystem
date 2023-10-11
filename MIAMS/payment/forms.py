from django import forms
import re

class PaymentForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    card_number = forms.CharField(max_length=16, min_length=16, required=True)
    expiry_date = forms.CharField(max_length=5, min_length=5, required=True)
    cvv = forms.CharField(max_length=3, min_length=3, required=True)

    # Add hidden fields for student and consultant email addresses
    # student_email = forms.EmailField(widget=forms.HiddenInput)
    # consultant_email = forms.EmailField(widget=forms.HiddenInput)

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        print(f'Card number: {card_number}')
        if not card_number.isdigit():
            raise forms.ValidationError("Card number should only contain digits.")
        return card_number

    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if not expiry_date or not re.match(r'^\d{2}/\d{2}$', expiry_date):
            raise forms.ValidationError("Expiry date should be in MM/YY format.")
        return expiry_date

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv')
        if not cvv.isdigit() or len(cvv) != 3:
            raise forms.ValidationError("CVV should be a 3-digit number.")
        return cvv
