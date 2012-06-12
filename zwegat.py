#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
from itertools import combinations

def parse(s):
    # remove comments
    s = re.sub(r'//.*\n',r'\n', s)
    # remove whitespace
    s = re.sub(r'[ \t\f]','', s)
    # remove blank lines
    s = re.sub(r'^\n','', s).strip()
    ret = []
    # TODO: Teste Format. Falls falsch, Fehlermeldung
    for l in s.splitlines():
        [creditor, debtors, amount] = l.split(';')
        debtors = set(debtors.split(','))
        amount = float(amount)
        ret.append((creditor, debtors, amount))
    return ret

def getPersons(p):
    ret = set()
    for (creditor, debtors, _) in p:
        ret.add(creditor)
        ret |= debtors
    return ret

def getDebtsFor(p, debtor):
    ret = {}
    for person in getPersons(p): ret[person] = 0
    for (creditor, debtors, amount) in p:
        if debtor in debtors:
            ret[creditor] += amount / len(debtors)
    # remove superflous information
    ret = {k: ret[k] for k in ret.keys() if ret[k] != 0}
    return ret

def getDebts(p):
    ret = {}
    for person in getPersons(p):
        ret[person] = getDebtsFor(p, person)
    return ret

def normalizeDebts(d):
    for (d1, d2) in combinations(d.keys(), 2):
        if d2 in d[d1] and d1 in d[d2]:
            d1_debt = d[d1][d2]
            d2_debt = d[d2][d1]
            if d1_debt < d2_debt:
                del d[d1][d2]
                d[d2][d1] = d2_debt - d1_debt
            elif d2_debt < d1_debt:
                del d[d2][d1]
                d[d1][d2] = d1_debt - d2_debt
            else:
                del d[d1][d2]
                del d[d2][d1]
    return d

def printDebts(d):
    print ""
    for debtor, debts in d.iteritems():
        if len(debts) == 0:
            pass
        elif len(debts) == 1 and debtor in debts:
            amount = debts[debtor]
            print "%s hat Kosten für sich selbst von %0.2f€" % (debtor, amount)
            print ""
        else:
            print debtor + " schuldet"
            for creditor, amount in debts.iteritems():
                if creditor != debtor:
                    print "  %s %0.2f€" % (creditor, amount)
            if debtor in debts:
                amount = debts[debtor]
                print "  und hat Kosten für sich selbst von %0.2f€" % (amount)
            print ""

if __name__ == '__main__':
    filename = ""
    if len(sys.argv) <= 1: filename = raw_input("Gib Dateinamen ein: ")
    else: filename = sys.argv[1]
    f = open(filename, 'r').read()
    p = parse(f)
    d = normalizeDebts(getDebts(p))
    printDebts(d)
    raw_input("Drücke eine Taste...")
