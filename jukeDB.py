class JukeDB:
	'''
	A class to use crud actions to access a database and play a song.
	'''
	def __init__(self,host,user,db_name,dbpasswd):
		'''
		Initialises the JukeDB class
		
		host     = The MySQL host
		user     = The username of user
		db_name  = The database to connect to
		dbpasswd = Password for the database
		
		Connecting to database example
		
		connect = JukeDB("localhost","root","jukebox","jukebox")
		'''
		
		self.dbhost = host
		self.dbuser = user
		self.dbpasswd = dbpasswd
		self.db_name = db_name 
		self.ConnectDB()
		
	def ConnectDB(self):
		'''
		A method used to connect to the database
		'''
		
		#Import MySQLdb
		import MySQLdb
		self.db = MySQLdb.connect(self.dbhost,
							self.dbuser,
							self.dbpasswd,
							self.db_name)
		self.cur = self.db.cursor()
	
	def ViewDB(self,table,fname):
		'''
		A method used to view a specific file from a table
		
		table = Table name
		fname = File location
		
		ViewDB example
		
		connect = JukeDB("localhost","root","jukebox","jukebox")
		view = connect.viewFullDB()
		print view
		'''
		#This returns a result from the fullname column
		viewtable= "select * from %s where full_name = '%s'" % (table,fname)
		self.cur.execute(viewtable)
		#Return "Filename", "Artist", and "Album"
		for row in self.cur.fetchall():
			results = str(row[1])+' : '+str(row[2])+' : '+str(row[3])+'\n'
		#Return results
		return results

	def addToDB(self,table,fname,artist='none',title='none',album='none'):
		'''
		A method to add a song to a table
		
		table  = Table name
		fname  = File location
		artist = Artist (defaults to 'none' if nothing specified)
		title  = Title  (defaults to 'none' if nothing specified)
		album  = Album  (defaults to 'none' if nothing specified)
		
		Add a song to table example
		
		connect = JukeDB("localhost","root","jukebox","jukebox")
		add_song = connect.addToDB('music','/home/chris/Music/Aerodynamic.mp3','Daft Punk','Aerodynamic','Discovery')
		'''
		#View full table
		self.cur.execute("SELECT * FROM music")
		new_entry = True
		
		#This checks if the filename already exists in the table in row[1]
		for row in self.cur.fetchall() :
			if row[1] == fname:
				print "Cannot add song, already in database\n"
				new_entry = False
		
		#Checks if file is not in table
		if new_entry == True:
			#Insert into table
			new_value = "insert into %s values( null, '%s', '%s', '%s', '%s', null,1)" % (table,fname,artist,title,album)
			#Execute command
			self.cur.execute(new_value)
			self.cur.execute("select * from music")
			#View full table
			for row in self.cur.fetchall():
				results = str(row[1])+' : '+str(row[2])+' : '+str(row[3])+' : '+str(row[4])+'\n'
			#Commit will add changes to database, nothing changes until self.db.commit() is called
			self.db.commit()
			return results

	def updateDB(self,table,set_update_column,set_update_result,where_update,where_string):
		'''
		A method to update the database
		
		table             = Table name
		set_update_column = Column where update takes place
		set_update_result = New value
		where_update      = Where column is
		where_string      = Where detail is
		
		
		An example of how to update a song in the table.
		
		connect = JukeDB("localhost","root","jukebox","jukebox")
		val = connect.validateDB("music","full_name","Oasis.mp3")
		if val == True:
			update_song = connect.updateDB("music","artist","Oasis","full_name","Oasis.mp3")
			print update_song
		else:
			print "Song not in table, cannot update!"
		
		
		'''
		
		#Entry to be updated
		updated_value = "update %s set %s='%s' where %s='%s'" % (table,set_update_column,set_update_result,where_update,where_string)
		self.cur.execute(updated_value)
		
		#View updated table
		self.cur.execute("select * from music")
		for row in self.cur.fetchall():
			results = str(row[1])+' : '+str(row[2])+' : '+str(row[3])+' : '+str(row[4])+'\n'
		self.db.commit()
		#Return results
		return results

	def delFromDB(self,table,where_column,where_data):
		'''
		A method to delete an entry from the database
		
		table        = Table name
		where_column = Column where delete takes place
		where_data   = Name of entry to delete
		
		
		An example of how to delete a song from the table.
		
		connect = JukeDB("localhost","root","jukebox","jukebox")
		val = connect.validateDB("music","artist","Oasis")
		if val == True:
			del_song = connect.delFromDB("music","artist","Oasis")
			print del_song
		else:
			print "Song not in table, cannot delete!"
		'''
		
		#Entry to be deleted
		delete_value = "delete from %s where %s='%s'" % (table,where_column,where_data)
		self.cur.execute(delete_value)
		#Commit change
		self.db.commit()
		
		#Return message
		return "Deleted from table"

	def validateDB(self,table,column,value):
		'''
		A method used to validate if an entry already exists in the table
		
		table  = Table name
		column = Column where entry to be checked is
		value  = Entry to be checked
		
		Validation example
		
		connect = JukeDB("localhost","root","jukebox","jukebox")
		val = connect.validateDB("music","artist","Oasis")
		if val == True:
			print "Song exists"
		else:
			print "Song not in table!"
		'''
		
		#Check tables for entries
		
		if column == "id":
			column_no = 0
		elif column == "full_name":
			column_no = 1 
		elif column == "artist":
			column_no = 2
		elif column == "title":
			column_no = 3
		elif column == "album":
			column_no = 4
		self.cur.execute("SELECT * FROM music")
		#Checks if value is in the table
		for row in self.cur.fetchall() :
			if row[column_no] == value:
				#Return True if entry exists
				return True

	def viewFullDB(self):
		'''
		A method to view the full table
		
		Viewing the full table example
		
		connect = JukeDB("localhost","root","jukebox","jukebox")
		view = connect.viewFullDB()
		print view
		'''
		#View full table
		full = "select * from music"
		self.cur.execute(full)
		for row in self.cur.fetchall():
			print row[0],row[1],row[2],row[3],row[4],row[5],row[6]
	
	def getFilePath(self,song_id):
		'''
		A method to find the file path using the song id
		
		song_id = ID of the song
		
		Get the file path example
		
		connect = JukeDB("localhost","root","jukebox","jukebox")
		view = connect.viewFullDB()
		print view
		song_id = raw_input("Enter song id:")
		song_path = connect.getFilePath(song_id)
		print song_path
		'''
		
		#Return file path
		path = "select full_name from music where id=%s" % (song_id)
		self.cur.execute(path)
		for row in self.cur.fetchall():
			f_path = str(row[0])
		#Return file path
		return f_path

		
	
	def playSong(self,path):
		'''
		A method to play a song using mplayer
		
		path = File location
		
		Playing a song example
		
		connect = JukeDB("localhost","root","jukebox","jukebox")
		view = connect.viewFullDB()
		print view
		song_id = raw_input("Enter song id:")
		song_path = connect.getFilePath(song_id)
		print song_path
		go = connect.playSong(song_path)
		'''
		
		#Import os
		import os
		
		#Play song
		os.system("mplayer %s" % (path)) 
