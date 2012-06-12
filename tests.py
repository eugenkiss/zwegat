#! /usr/bin/env python
import nose
from zwegat import *

def test1():
    p = parse("""
        e; e; 5.00
        """)
    assert p == [('e', set(['e']), 5)]
    assert getPersons(p) == set(['e'])
    assert getDebtsFor(p, 'e') == {'e': 5}
    assert normalizeDebts(getDebts(p)) == {'e': {'e': 5}}

def test2():
    p = parse("""
        e; e,p,w;   2.70    // 01.06: Kuchenpapier
        """)
    assert p == [('e', set(['e','p','w']), 2.70)]
    assert getPersons(p) == set(['e','p','w'])
    assert getDebtsFor(p, 'e') == {'e': 0.90}
    assert getDebtsFor(p, 'p') == {'e': 0.90}
    assert getDebtsFor(p, 'w') == {'e': 0.90}
    assert getDebts(p) == {'e': {'e': 0.90},
                           'p': {'e': 0.90},
                           'w': {'e': 0.90}}
    assert normalizeDebts(getDebts(p)) == getDebts(p)

def test3():
    p = parse("""
        e; e,p,w;   2.70    // 01.06: Kuchenpapier
        p; e,p,w;   0.90    // 01.06: Duft
        """)
    assert p == [('e', set(['e','p','w']), 2.70),
                 ('p', set(['e','p','w']), 0.90)]
    assert getPersons(p) == set(['e','p','w'])
    assert getDebts(p) == {'e': {'e': 0.90, 'p': 0.30},
                           'p': {'e': 0.90, 'p': 0.30},
                           'w': {'e': 0.90, 'p': 0.30}}
    assert normalizeDebts(getDebts(p)) == \
                          {'e': {'e': 0.90},
                           'p': {'e': 0.6000000000000001, 'p': 0.30},
                           'w': {'e': 0.90, 'p': 0.30}}

def test4():
    p = parse("""
        e; e,p,w; 90
        p; e,p  ; 20
        p;   p  ; 10
        w; e,  w; 40
        w; e,p,w; 120
        p; e,  w; 50
        """)
    print normalizeDebts(getDebts(p))
    assert normalizeDebts(getDebts(p)) == \
            {'e': {'p': 5, 'w': 30, 'e': 30},
             'p': {'w': 15, 'p': 20},
             'w': {'w': 60}}

nose.main()
