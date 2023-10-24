from parsfpa import Parsfpa
import pickle
from itertools import combinations, product
import time
from selenium.common.exceptions import NoAlertPresentException

import basdan

class Search_ot_fpa(Parsfpa):
	
	txt='C:\\Users\\Михаил\\YandexDisk\\Рабочие\\FPA\\resh.txt'
	name_tabl='fpa'

	def __init__(self):
		basdan.new_tabl_question(self.name_tabl)#таблица в бд для вопросов
		self.in_site()
		self.authorization('keebirg','1q2w3e4r5')
		self.click_start()
		
   
	def set_bd_question(self):#записывает в бд текущей номер вопроса, сам вопрос, радио\чекбокс и есть на него ответ или нет
		cort=(self.get_question_number(), self.get_text(), self.get_rr(), 'false')
		basdan.add_tabl_question(self.name_tabl, cort)

	def set_bd_answer(self):#записываеи в вд, сами ответы, и все возможные сочетания, и текущей результат 
		name_tabl_answer='a'+str(self.get_question_number())
		basdan.new_tabl_answer(name_tabl_answer, self.get_rr(), len(self.get_var_ot()))
		spcort=self.spcort_form()
		basdan.add_tabl_answer(name_tabl_answer, spcort, self.get_rr(), len(self.get_var_ot()))
		
	def spcort_form(self):

		var_ot=self.get_var_ot()
		gg1=[]
		gg2=[]
		a_bool=['true', 'false']
		temp=list(product(a_bool, repeat=len(self.get_var_ot())))
		
		if self.get_rr()=='один':
			for coun in range(len(var_ot)):
				gg1.append(coun+1)
				gg1.append(var_ot[coun])
				for i in range(len(var_ot)):
					if coun==i:
						gg1.append('true')
					else:
						gg1.append('false')

				gg2.append(tuple(gg1))
				gg1=[]

			gg1.append(len(var_ot)+1)
			gg1.append('проверили?')
			for i in range(len(var_ot)):
				gg1.append('false')
			gg2.append(tuple(gg1))
			gg1=[]

			gg1.append(len(var_ot)+2)
			gg1.append('Это и есть решение?')
			for i in range(len(var_ot)):
				gg1.append('false')
			gg2.append(tuple(gg1))
			gg1=[]

		else:
			for coun in range(len(var_ot)):
				gg1.append(coun+1)
				gg1.append(var_ot[coun])
				for i in range(len(temp)):
					gg1.append(temp[i][coun])

				gg2.append(tuple(gg1))
				gg1=[]

			gg1.append(len(var_ot)+1)
			gg1.append('проверили?')
			for i in range(len(temp)):
				gg1.append('false')
			gg2.append(tuple(gg1))
			gg1=[]

			gg1.append(len(var_ot)+2)
			gg1.append('Это и есть решение?')
			for i in range(len(temp)):
				gg1.append('false')
			gg2.append(tuple(gg1))
			gg1=[]

		return gg2

	def search_FTA(self): # если найдет хотя бы один неизвестный отправляем True
		for i in range(500):
			if basdan.get_question_FTA(self.name_tabl, i)=='false':
				return True
			if basdan.get_question_FTA(self.name_tabl, i)=='err' and i<100:
				return True
		return False

	def sf_ot(self, temp): #формирует список ответов + номер столбца с текущем вариантом ответа 
		sp=[]
		for j in range(2, len(temp[0])):
			if temp[len(temp)-2][j]=='false':
				for i in range(len(temp)):
					if temp[i][j]=='true':       #если ответ истина
						sp.append(temp[i][1])	 #добавили ответ в конец списка
				#basdan.set_answer('a'+str(self.get_question_number()), len(temp)-1, 'var'+str(j-1), 'true')#записали в бд что проверили
				sp.append('var'+str(j-1))
				return sp



	def search(self, coun=0):#поиск вопрса, на который неизвестен ответ, coun кол-во вопросов
		while self.search_FTA():#пока не найдет все вопросы
			if basdan.get_question_FTA(self.name_tabl, self.get_question_number())=='err': # существует ли вопрос в бд
				self.set_bd_question()
				self.set_bd_answer()

			if basdan.get_question_FTA(self.name_tabl, self.get_question_number())=='false': # есть ли на него ответ
				i=self.get_question_number()#номер текущего вопроса
				num='a'+str(i) #названия таблицы с ответами
				temp=basdan.get_answer_tabl(num) #получение этой таблице
				sp=self.sf_ot(temp) #получение списков текущех ответов и номер текущего варианта
				j=sp[-1]
				sp=sp[0:-1]
				self.click_var_ot(sp)
				
				self.click_finish()
				if self.get_result_finish():
					print(i, '-найден ответ')
					basdan.set_answer(num, len(temp)-1, j, 'true')#записали в бд что проверили
					basdan.set_answer(num, len(temp), j, 'true')#записали в бд что верный вариант
					basdan.set_question_FTA(self.name_tabl, i, 'true')#записали в бд что результат найден
					self.in_site()
					self.click_start()
				else:
					basdan.set_answer(num, len(temp)-1, j, 'true')#записали в бд что проверили
					self.in_site()
					self.click_start()

			else: 
				if self.get_counter():                  # если ответ известен, то
					self.click_finish()					# проверяем на конец теста
					self.in_site()						# если не конец то на следующей вопрос
					self.click_start()					# если конец то закончить и заново 
				else:
					self.click_next()


			
	def form_sp_ot(self):
		num='a'+str(self.get_question_number()) #названия таблицы с ответами
		temp=basdan.get_answer_tabl(num) #получение этой таблице
		sp=[]
		for j in range(2, len(temp[0])):
			if temp[len(temp)-1][j]=='true':
				for i in range(len(temp)):
					if temp[i][j]=='true':       #если ответ истина
						sp.append(temp[i][1])	 #добавили ответ в конец списка
				return sp

	def go_answer(self):
		self.click_finish()
		self.in_site()
		self.click_start()
		while not self.get_counter():
			self.click_var_ot(self.form_sp_ot())
			self.click_next()
		else:
			self.click_finish()
			print('\n результат: ',self.get_result_finish())

					
	def search_question(self, num):#поиск num вопроса (оставляет стр, на этом вопросе)
		self.in_site()
		self.click_start()
		while True:
			if num==self.get_question_number():
				break
			else:
				if self.get_counter():
					self.click_finish()
					self.in_site()
					self.click_start()
				else:
					self.click_next()
				
				
	def search_answer(self): #поиск ответа на вопрос
		gen_ot=self.list_gen_ot()
		num=self.get_question_number()
		for ot in gen_ot:
			self.click_var_ot(ot)
			self.click_finish()
			if self.get_result_finish():
				self.resh[num]=ot
				print('\n\n-----------------------------------------------------------------------------')
				self.display_resh()
				temp=open(txt, 'wb')
				pickle.dump(self.resh,temp)
				break
			else:
				self.search_question(num)               
			   			

		
		


