#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
from itertools import combinations
from decimal import *
from pyparsing import Word, Literal, LineEnd, ZeroOrMore, OneOrMore, Regex, \
                      Group, ParseException, ParseSyntaxException, Combine, \
                      restOfLine, alphas, alphanums, delimitedList, nums

comma       = Literal(',').suppress().setName('comma')
semicolon   = Literal(';').suppress().setName('semicolon')
decimal     = Combine(Word(nums).setName('number') + '.' + Word(nums)).setName('decimal') | \
              Word(nums).setName('decimal')
decimal.setParseAction(lambda s,l,t: [Decimal(t[0]).normalize()])
comment     = Literal('#') + restOfLine
name        = Word(alphas + "_", alphanums + "_").setName('name')
names       = Group(delimitedList(name)).setName('names')
entry       = name - semicolon - names - semicolon - decimal - LineEnd().suppress()
entry.setParseAction(lambda s,l,t: [(t[0],set(t[1]),t[2])])
parser      = ZeroOrMore(entry | LineEnd().suppress())
parser.setWhitespaceChars(r' \t\f')
parser.ignore(comment)

def parse(s):
    return parser.parseString(s, parseAll=True)

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
            ret[creditor] += amount / Decimal(len(debtors))
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
            print "%s spent %0.2f" % (debtor, amount)
            print ""
        else:
            spent = 0
            print debtor + " owes"
            for creditor, amount in debts.iteritems():
                if creditor != debtor:
                    spent += amount
                    print "  %s %0.2f" % (creditor, amount)
            if debtor in debts:
                spent += debts[debtor]
            print "  and spent %0.2f" % (spent)
            print ""

def main():
    filename = ""
    if len(sys.argv) <= 1:
        print "Please enter a filename as a command line argument."
        sys.exit(0)
    else:
        filename = sys.argv[1]

    try:
        f = open(filename, 'r').read()
    except IOError:
        print 'Cannot open', filename
        sys.exit(-1)

    try:
        p = parse(f)
    except ParseException, err:
        print err.line
        print " "*(err.column-1) + "^"
        print err
        sys.exit(-1)
    except ParseSyntaxException, err:
        print err.line
        print " "*(err.column-1) + "^"
        print err
        sys.exit(-1)

    d = normalizeDebts(getDebts(p))
    printDebts(d)

if __name__ == '__main__': main()
