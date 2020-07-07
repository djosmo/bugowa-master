
from django import forms
from .models import Post
class PostForm(forms.ModelForm):
	class Meta:
		model = Post      
		fields = ('title', 'slug','body')         #author zamiast slug
		labels = {'title':'Wpisz kwotę:', 
                  'slug': 'Potwierdź:',            #author zamiast slug
                  'body' : 'Wydane na:'}
		widgets = {'body' : forms.TextInput(attrs={'size': '20'})}   #'#'
                           
                                    
class EmailPostForm(forms.Form):                                                                   
    Podpis = forms.CharField(max_length=25)
    Email = forms.EmailField()
    Odbiorca = forms.EmailField()
    Komentarz = forms.CharField(required=False, 
                               widget=forms.Textarea)

class EPostForm(forms.ModelForm):
    	class Meta:
            model = Post
            fields = ('title', 'body')
            labels = {'title': 'Popraw kwotę:',
                      'body': 'Popraw opis:'}
		

		   


