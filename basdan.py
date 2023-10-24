import sqlite3

db=sqlite3.connect('fpa.db')
cursor=db.cursor()

def new_tabl_question(name_tabl): #создаем новую таблицу с именем name_tabl
	string="""CREATE TABLE IF NOT EXISTS """ + name_tabl + """(
				id INT PRIMARY KEY,
				question TEXT,
				radio_checkbox TEXT,
				FTA TEXT);
			"""

	cursor.execute(string)
	db.commit()

def add_tabl_question(name_tabl, сort):#добовляем строку в таблицу name_tabl
	try:
		cursor.execute("INSERT INTO " + name_tabl + " VALUES(?, ?, ?, ?);", сort)
		db.commit()
	except sqlite3.IntegrityError:
			print('такой вопрос уже внесен в таблицу')

def new_tabl_answer(name_tabl, radio_checkbox, k ): #создаем новую таблицу с именем name_tabl=a+номер вопроса
	string="""CREATE TABLE IF NOT EXISTS """ + name_tabl + """(
				id INT PRIMARY KEY,
				answer TEXT,
				"""

	if radio_checkbox=='один':
		for i in range(k):                        # k - количество ответов
			string+='var'+str(i+1)+' TEXT,\n'
	else:
		for i in range(2**k):
			string+='var'+str(i+1)+' TEXT,\n'

	string=string[0:-2]
	string+=');'

	cursor.execute(string)
	db.commit()

def add_tabl_answer(name_tabl, spcort, radio_checkbox, k):#добовляем строки в таблицу name_tabl
	string="INSERT INTO " + name_tabl + " VALUES("

	if radio_checkbox=='один':
		for i in range(k+2):                        # k - количество ответов
			string+='?, '
	else:
		for i in range(2**k+2):
			string+='?, '

	string=string[0:-2]
	string+=');'

	cursor.executemany(string, spcort)
	db.commit()

def set_question_FTA(name_tabl, id1, res): # значения известности ответа на данный вопрос 
	update_sql = "UPDATE " + name_tabl+ " SET FTA = ? WHERE id = ?"
	cursor.execute(update_sql, (res, id1))
	db.commit()

def get_question_FTA(name_tabl, id1):
	fta="SELECT FTA FROM " + name_tabl + " WHERE id = ?" 
	cursor.execute(fta, (id1,))
	cur=cursor.fetchone()
	db.commit()
	if cur is None:
		return 'err'
	else:
		return cur[0]

def get_answer_tabl(name_tabl):
	try:
		cursor.execute('select * from ' + name_tabl)
		cur=cursor.fetchall()
		db.commit()
		return cur
	except sqlite3.OperationalError:
		return False

def set_answer(name_tabl, id1, num, res): # значения известности ответа на данный вопрос 
	update_sql = "UPDATE " + name_tabl+ " SET " + num + " = ? WHERE id = ?"
	cursor.execute(update_sql, (res, id1))
	db.commit()
