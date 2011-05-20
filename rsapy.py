#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random

def ggt(a,b):
    if b==0:
        return a
    else:
        return ggt(b, a % b)

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
    while k>0:
        a = random.randint(2,n-1)
        x = jacobi(a,n)
        if x == 0:
            return False
        m = (n-1)/2
        if (pow(a,m,n) != (x % n)):
            return False
        k -= 1
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

    print "\tp =", p
    print "\tq =", q

    print "Berechne n und phi(n)..."

    n = p*q

    print "\tn =", n

    phin = (p-1)*(q-1)

    print "\tphi(n) =", phin

    print "Berechne e..."
    e = 0
    while not(ggt(e,phin) == 1):
        e = random.randint(2,phin-1)
    print "\te =", e

    print "Berechne d..."
    (x,y) = erweiterter_ggt(e,phin)
    d = x % phin
    print "\td =", d

    print

    print "n\t", n
    print "p\t", p
    print "q\t", q
    print "phin\t", phin
    print "e\t", e
    print "d\t", d

    print

    print "Verschlüsselung..."
    print "Klartext:\t", M

    C = []
    for m in M:
        C.append(pow(ord(m),e,n))
    print "Geheimtext:\t", C

    print

    print "Entschlüsselung..."
    M = ""
    for c in C:
        M += chr(pow(c,d,n))
    print "Klartext:\t", M

if __name__ == "__main__":
    main()
