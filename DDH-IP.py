import math
import random

# Author : Eathoublu_YixiaoLan
# Email : yixiaolan@foxmail.com
# Reference : Abdalla, Michel & Florian, Bourse & Caro, Angelo & Pointcheval, David. (2015). Simple Functional Encryption Schemes for Inner Products. 10.1007/978-3-662-46447-2_33. https://www.researchgate.net/publication/278630111_Simple_Functional_Encryption_Schemes_for_Inner_Products

class power:
	def __init__(self, a, N):
		self.a = a
		self.N = N
		if isinstance(self.a, power) and isinstance(self.N, int):
			self.a = a.a
			self.N = a.N*N
		if isinstance(self.N, power):
			raise Exception('Not support power on top.') 
	def __str__(self):
		return '{}^{}'.format(self.a, self.N)
	def value(self):
			return self.a**self.N
#print(isinstance(1, int))
#quit()	
			
class powmultiply:
	def __init__(self, a, b):
		if isinstance(a, int):
			self.a = pow(a, 1)
		if isinstance(b, int):
			self.b = pow(b, 1)
		self.a = a
		self.b = b	
		if self.a.a == self.b.a:
			self.a = power(self.a.a, self.a.N+self.b.N)
			self.b = power(1, 1)
	def __str__(self):
		return '{}*{}'.format(self.a, self.b)
	def value(self):
		if isinstance(self.a, power) and isinstance(self.b, power):
			return self.a.value() * self.b.value()
	def to_power(self):
		if self.b.value() == 1:
			return self.a
		else:
			raise Exception('cannot transform to power')
			
class powdiv:
	def __init__(self, a, b):
		if isinstance(a, int):
			self.a = pow(a, 1)
		if isinstance(b, int):
			self.b = pow(b, 1)
		self.a = a
		self.b = b	
		if self.a.a == self.b.a:
			self.a = power(self.a.a, self.a.N-self.b.N)
			self.b = power(1, 1)
	def __str__(self):
		return '{}*{}'.format(self.a, self.b)
	def value(self):
		if isinstance(self.a, power) and isinstance(self.b, power):
			return self.a.value() / self.b.value()
	def to_power(self):
		if self.b.value() == 1:
			return self.a
		else:
			raise Exception('cannot transform to power.')
		
#print(powmultiply(power(2, 2), power(2, 3)))
#quit()

class DDHIP_Setup(object):
	def __init__(self, l, p=0b010, g=5):
		self.p = p
		self.msk = s = [random.randint(1, p) for _ in range(l)]
		self.mpk = [power(g, si) for si in s]
	
	def setup(self):
		return self.mpk, self.msk
	

class DDHIP_Encrypt(object):
	def __init__(self, x, mpk, msk, g=5, p=0b010):
		if len(msk) < len(x) or len(msk) != len(mpk):
			raise Exception('length not match.')
		self.l = len(x)
		self.p = p
		self.g = g
		self.x = x
		self.r = random.randint(1, p)
		self.mpk = mpk
		self.msk = msk
	
	def encrypt(self, ):
		ct = [power(self.g, self.r)] + [powmultiply(power(self.g, self.x[i]),power(self.mpk[i], self.r)).to_power() for i in range(self.l)]
		return ct
		
class DDHIP_Decrypt(object):
	def __init__(self, y, msk, ct):
		self.ct = ct
		self.sk_y = 0
		self.y = y
		self.msk = msk
		self.keyder()
	
	def keyder(self):
		for i in range(len(self.y)):
			self.sk_y += self.y[i]*self.msk[i]
			
	def decrypt(self, ):
		ct0_y = power(self.ct[0], self.sk_y)
		ct = self.ct[1:]
		_pi = power(ct[0], self.y[0])
		for i in range(1, len(ct)):
			_pi = powmultiply(_pi, power(ct[i], self.y[i])).to_power()
		return powdiv(_pi, ct0_y).to_power().N
		  
		
		
		
		
# The following example shows how to calculate [1, 2, 5]x[2, 4, 5] make sure l = len(vector)
if __name__ == '__main__':
		setup = DDHIP_Setup(l=3)
		mpk, msk = setup.setup()
		encrypt = DDHIP_Encrypt([1,2,5], mpk, msk)
		ct = encrypt.encrypt()
		
		decrypt = DDHIP_Decrypt([2,4,5], msk, ct)
		print(decrypt.decrypt())
		
quit()

