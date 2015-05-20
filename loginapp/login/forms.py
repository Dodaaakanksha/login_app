import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import os

def upload_profile_pic(instance, filename):
	path = 'login/media/images/profile_pic/'
	ext = filename.split('.')[-1]
	username=instance.username
	filename='{}.{}'.format(username,ext)
	return os.path.join(path, filename)

class RegistrationForm(forms.Form):
	#user = forms.OneToOneField(User , unique=True)
	username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("username"), error_messages={ 'invalid': _("this value must contain only letters, numbers and underscores.") })
	email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("email address"))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password(again)"))
	#profile_pic = forms.ImageField(upload_to = 'login/media/images/profile_pic/' )
	 

	def clean_username(self):
		try:
			user = User.objects.get(username__iexact=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError(_("the username already exist. please try another one."))

	def clean(self):
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError(_("the two passwords do not match"))
		return self.cleaned_data

	def clean_profile_pic(self):
		profile_pic = self.cleaned_data['profile_pic']
		try:
			w, h = get_image_dimensions(profile_pic)
			max_width = max_height = 100
			if w > max_width or h > max_height:
				raise forms.ValidationError(
					u'Please use an image that is '
					 '%s * %s pixels or smaller.'%(max_width, max_height))

			main, sub = profile_pic.content_type.split('/')
			if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
				raise forms.ValidationError(u'please use a JPEG, '
					'GIF or PNG image.')

			if len(profile_pic) > (20*1024):
				raise forms.ValidationError(
					u'Profile pic file size may not exceed 20k.')

		except AttributeError:
			pass

		return profile_pic 
