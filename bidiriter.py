class BiDirIterator(object):
	class Stop(object):
		def __init__(self, next=None, prev=None):
			self._next = next
			self._prev = prev

		def next(self):
			if self._next:
				return self._next
			else:
				raise StopIteration

		def prev(self):
			if self._prev:
				return self._prev
			else:
				raise StopIteration

		def __nonzero__(self):
			return False


	def __init__(self, obj_list):
		iter_obj_list = [BiDirIteratorObject(obj) for obj in obj_list]
		self._head = self.__build(iter_obj_list)
		self._ptr = self.Stop(next=self._head)
		self._cur = self._head
	
	def __build(self, iter_obj_list):
		try:
			head = iter_obj_list[0]
			ptr = head
			for iter_obj in iter_obj_list[1:]:
				ptr._next = iter_obj
				iter_obj._prev = ptr
				ptr = iter_obj
		except IndexError:
			head = self.Stop()
		return head

	def __iter__(self):
		return self
	
	def next(self):
		next = self._ptr.next()
		if not next:
			self._ptr = self.Stop(prev=self._ptr)
		self._ptr = self._ptr.next()
		if not isinstance(self._ptr,self.Stop):
			self._cur = self._ptr
		return self._ptr.obj

	def prev(self):
		prev = self._ptr.prev()
		if not prev:
			self._ptr = self.Stop(next=self._ptr)
		self._ptr = self._ptr.prev()
		if not isinstance(self._ptr,self.Stop):
			self._cur = self._ptr
		return self._ptr.obj

	def fastforward(self):
		while True:
			try:
				self.next()
			except StopIteration:
				break
		return self._cur

	def rewind(self):
		while True:
			try:
				self.prev()
			except StopIteration:
				break
		return self._cur

	def current(self):
		return self._cur.obj

class BiDirIteratorObject(object):
	def __init__(self, obj, next=None, prev=None):
		self.obj = obj
		self._next = next
		self._prev = prev
	
	def next(self):
		return self._next

	def prev(self):
		return self._prev
