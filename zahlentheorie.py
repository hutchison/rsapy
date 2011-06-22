#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
from math import ceil, sqrt

def ggt(a,b):
	if b==0:
		return a
	else:
		return ggt(b, a % b)

"""
Berechnet den Wert des Polynoms p an der Stelle x.
"""
def horner(x,p):
	r = 0
	for c in p:
		r = r*x + c
	return r

def hornermod(x,p,m):
	r = 0
	for c in p:
		r = (r*x + c) % m
	return r

def rho(n, p, x0):
	x = [x0]
	d = 1
	j = 0
	while d == 1:
		xn = hornermod(x[j], p, n)
		x.append(xn)
		j += 1
		for k in range(j):
			d = ggt(x[j] - x[k], n)
			if 1 < d < n:
				return d
	if d == n:
		return False

def factorize_rho(n, p, x0):
	x = [x0]
	d = 1
	j = 0
	while d == 1:
		x.append( hornermod(x[j], p, n) )
		for k in range(j):
			d = ggt(x[j] - x[k], n)
		j += 1
	return d

def is_square(n):
	if (n & 7 == 1) or (n & 31 == 4) or (n & 127 == 16) or (n & 191 == 0):
		return True
	else:
		return False

def factorize_fermat(n):
	x = int(ceil(sqrt(n)))
	r = x*x - n
	while(not(is_square(r))):
		r += 2*x + 1
		x += 1
	y = int(sqrt(r))
	return (x+y,x-y)

def anzahlprimzahlen(n):
	if n < 2:
		return 0
	return len(filter(prim,range(2,n+1)))

def jacobi(a,n):
	if a == 1:
		return 1
	if n % 2 == 0:
		return False
	if a % n == 0:
		return 0
	if a == 2:
		if (n % 8 == 1) or (n % 8 == 7):
			return 1
		else:
			return -1
	if a == (n-1):
		if n % 4 == 1:
			return 1
		else:
			return -1
	if a % 2 == 0:
		return jacobi(2,n) * jacobi(a/2,n)
	if a > n:
		return jacobi(a % n, n)
	if (a % 4 == 3) and (n % 4 == 3):
		return (-1) * jacobi(n,a)
	if (a % 4 == 1) or (n % 4 == 1):
		return jacobi(n,a)

def solovaystrassen(n,k):
	if n < 2:
		return False
	if n == 2:
		return True
	# Liste mit zu überprüfenden Zahlen:
	l = set()
	while len(l) < k:
		l.add(random.randint(2,n-1))
	for a in l:
		x = jacobi(a,n)
		if x == 0:
			return False
		m = (n-1)/2
		if (pow(a,m,n) != (x % n)):
			return False
	return True

def prim(n):
	if n < 2:
		return False
	if n == 2:
		return True
	if n % 2 == 0:
		return False
	else:
		i = 3
		while i*i <= n:
			if n % i == 0:
				return False
			i += 2
	return True

def erweiterter_ggt(a,b):
	if b == 0:
		return (1,0)
	else:
		(q,r) = divmod(a,b)
		(s,t) = erweiterter_ggt(b,r)
		return (t,s-q*t)

def main():
	if len(sys.argv) >= 2:
		M = sys.argv[1]
	else:
		M = "grießbrei"

	print "Wähle zufällig p und q..."

	p,q = 0,0
	while not(solovaystrassen(p,100)):
		p = random.randint(2,10**40)
	while not(solovaystrassen(q,100)):
		q = random.randint(2,10**40)

	print "\tp\t=", p
	print "\tq\t=", q

	# Unicode ftw!
	print "Berechne n und φ(n)..."

	n = p*q

	print "\tn\t=", n

	phin = (p-1)*(q-1)

	print "\tφ(n)\t=", phin

	print "Berechne e..."
	e = 0
	while not(ggt(e,phin) == 1):
		e = random.randint(2,phin-1)
	print "\te\t=", e

	print "Berechne d..."
	(x,y) = erweiterter_ggt(e,phin)
	d = x % phin
	print "\td\t=", d

	print "Verschlüsselung..."
	print "  Klartext:\t", M

	C = []
	for m in M:
		C.append(pow(ord(m),e,n))
	print "  Geheimtext:\t", C

	print "Entschlüsselung..."
	M = ""
	for c in C:
		M += chr(pow(c,d,n))
	print "  Klartext:\t", M

if __name__ == "__main__":
	for i in range(7):
		print anzahlprimzahlen(10**i)
	print factorize_rho(290377,[1,1,1],1)
	print factorize_fermat(290377)
	#main()
