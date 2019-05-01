from urllib import parse
#from collections import namedtuple

#Поле для ввода
class InputField:
	#в field_type хранится тэг - название, с помощью которого формируется стркоа
	text_reform = ''
	text_orig = ''
	def __init__(self, field_type, additional=''):
		self.field_type = field_type
		self.additional = '&'+additional
	def __call__(self, text):
		self.text_reform=text.lower()
		self.text_orig=text
	def reform(self, mode='full'):
		if mode=='no-type':
			return '{0}{1}&'.format(self.text_reform, self.additional)
		else:
			return '{0}={1}{2}&'.format(self.field_type, self.text_reform, self.additional)
	def orig(self):
		return self.text_orig

class URLQuoteFiled(InputField):
	def __call__(self, text):
		super(URLQuoteFiled, self).__call__(text)
		self.text_reform=parse.quote(text)

class CompareField(InputField):
	def __init__(self, field_type, transform_vals, additional=''):
		super(CompareField, self).__init__(field_type,additional=additional)
		self.transform_vals = transform_vals
	def __call__(self, text):
		for x in self.transform_vals:
			if text.lower() in x:
				self.text_reform=x[1]
				self.text_orig=text
				break

test = (('нет опыта','noExperience'),
		('есть опыт','between1And3'))
InputText = URLQuoteFiled('text')
InputText('Data science#')
InputExp = CompareField('experience', test, additional='from=cluster_experience')
InputExp('Нет Опыта')
print(InputText.reform(), InputText.orig())
print(InputExp.reform(), InputExp.orig())