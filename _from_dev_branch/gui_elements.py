from urllib import parse
#from collections import namedtuple

#Поле для ввода
class InputField:
	'''
	Класс определяет интерфейс преобразования строки в 
	часть юрл-ссылки, по определенным правилам. Хранит как и
	преобразованную строку, так и оригинальную. 
	field_type - тэг, стоящий в начале строки
	additional - доп. инфа, стоящая в конце строки
	Основное действие выполняется посредством вызова
	экземпляра класса с превичной строкой
	'''
	text_reform = ''
	text_orig = ''
	def __init__(self, field_type, additional=''):
		self.field_type = field_type
		if additional=='':
			self.additional = additional
		else:
			self.additional = '&'+additional
	def __call__(self, text):
		self.text_reform=text.lower()
		self.text_orig=text
	def reform(self, mode='full'):
		return '{0}={1}{2}&'.format(self.field_type, self.text_reform, self.additional)
	def orig(self):
		return self.text_orig

class URLQuoteFiled(InputField):
	'''
	Подкласс реализующий преобразование стандартных
	символов в url код
	'''
	def __call__(self, text):
		super(URLQuoteFiled, self).__call__(text)
		self.text_reform=parse.quote(text)

class CompareField(InputField):
	'''
	Подкласс реализующий замену строки на соответствующую
	ей строку из словаря, записанного при инцилизациии
	экземпляра класса 
	'''
	def __init__(self, field_type, dictionary, additional=''):
		super(CompareField, self).__init__(field_type,additional=additional)
		self.dictionary = dictionary
	def __call__(self, text):
		if text in self.dictionary:
			self.text_reform=self.dictionary[text]
			self.text_orig=text

if __name__ == '__main__':
	test = {'Нет Опыта':'noExperience',
			'Есть Опыт':'between1And3'}
	InputText = URLQuoteFiled('text')
	InputText('Data science#')
	InputExp = CompareField('experience', test, additional='from=cluster_experience')
	InputExp('Нет Опыта')
	print("{0} => {1}".format(InputText.orig(), InputText.reform()))
	print("{0} => {1}".format(InputExp.orig(), InputExp.reform()))