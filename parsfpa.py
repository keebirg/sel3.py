from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert
import time

class Parsfpa():
	
	link='https://fparf.ru/learning/course/course2/test2/'
	options=webdriver.ChromeOptions()
	options.add_argument("disable-notifications")
	driver=webdriver.Chrome(options=options)
	counter=0

	

	def error_name(self, locator):#поиск по ферме через тег name
		try:
			temp=self.driver.find_element_by_name(locator)
			print('yes', locator)
		except NoSuchElementException:
			return self.error_name(locator)
			print('no', locator)
		return temp

	def in_site(self):
		self.driver.get(self.link)
		
	def authorization(self, login, password): 

		username_form = self.error_name('USER_LOGIN')
		password_form = self.error_name('USER_PASSWORD')
		go = self.error_name('Login')
		confirm=self.error_name('confirm')

		
		username_form.send_keys(login)
		password_form.send_keys(password)
		confirm.click()
		go.click()
	
	def click_start(self):# начать тест, если не вернул элемент тест закончен по времени.
		try:
			self.click_next()
			# self.click_next()
			# self.click_previous()
		except NoSuchElementException:
			self.in_site()
			self.click_next()

	def get_text(self):
		text = self.driver.find_element_by_class_name('learn-question-name')
		return text.text
	
	def get_question_number(self):
		
		text=self.get_text()
		for line in text.split(' '):
			flag=0
			for s in line:
				if s.isdigit():
					flag=1
					temp=line[0]+line[1]+line[2]
					self.question_number=int(temp)#-1 # - чтобы адоптировать под список
					break
			if flag:
				break

		return self.question_number

	def get_result_finish(self):#возвращаем кол-во правильных ответов
		result=self.driver.find_element_by_class_name('learn-result-table')
		ver=result.text
		ver=ver.split('\n')
		ver=ver[1].split(' ')
		return int(ver[3])

	def get_rr(self):#возвращает сколько ответов можно поставить в этом вопросе
		try:
			d=self.driver.find_element_by_xpath("//input[@type='radio']")
			return 'один'
		except NoSuchElementException:
			return 'несколько'
		
	def get_var_ot(self):#возвращает список вариантов ответов
		var_ot=self.driver.find_elements_by_class_name('checkboxes-group__item')
		gg=[]
		for x in var_ot:
			gg.append(x.text)
		return gg

	def click_var_ot(self, ot=[]):#кликает по ответам исходя из списка ответов
		index_ot=self.driver.find_elements_by_class_name('checkboxes-group__item')
		var_ot=self.get_var_ot()
		for (key, value) in enumerate(var_ot):
			if value in ot:
				index_ot[key].click()
				
	def get_counter(self):
		if self.counter==100+1:
			return True
		else:
			return False
	def set_counter(self):
		self.counter=0
		
	def click_previous(self):#предыдущий вопрос
		go = self.driver.find_element_by_name('previous')
		go.click()
		self.counter-=1
		
	def click_next(self):#следующей вопрос
		go = self.driver.find_element_by_name('next')
		go.click()
		self.counter+=1

	def click_finish(self):#финиш
		self.set_counter()
		go = self.driver.find_element_by_name('finish')
		go.click()
		time.sleep(1)
		alert = Alert(self.driver)
		alert.accept()

	def finish(self):# закрытия окна и удоления из памяти 
		self.driver.close()
		self.driver.quit()