from django import forms
from .models import FruitModel, Vendor, Comment

class FruitForm(forms.ModelForm):
    class Meta:
        model=FruitModel
        fields= '__all__'

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields= '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['image', 'review', 'rate']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter Your review here'}),
            'rate': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }

    def clean(self):
        cleaned_data = super().clean()
        review = cleaned_data.get('review')
        rate = cleaned_data.get('rate')

        if not review:
            self.add_error('review', 'This field is required.')
        if not rate:
            self.add_error('rate', 'This field is required.')

        return cleaned_data
