zwegat: A debts calculator
==========================

**zwegat** is a small program I have written for my flat share to simplify
debts calculations. It can read text files in a certain format and
output the debts of the persons inside the text file. The debts are
simplified in case person *x* owes person *y* a certain amount of money
person *y* owes person *x* a certain amount of money.


Installation
------------

Install **zwegat** with `sudo pip install
git+git://github.com/eugenkiss/zwegat.git` (you need to have
[python](http://www.python.org/getit/) and
[pip](http://www.pip-installer.org/en/latest/index.html) on your
system). A command line tool `zwegat` will be registered.

Alternatively, simply copy the python script `zwegat.py` to a
folder of your choice and execute it with `python zwegat.py` or just
`zwegat.py` if you marked `zwegat.py` as executable.


Usage
-----

Provide a filename *x* as a command line argument like so `zwegat
x`.


File Format
-----------

The following exemplary segment could be the content of a correctly
formatted file:

    eugen;  eugen,polina,wadim; 2.70  # 01.06: Plutonium
    wadim;  polina,wadim;       9.13  # 02.06: Cocaine
    polina; eugen;              1.80  # 04.06: Shark fin

As you can see every line constitutes an entry. Each entry consists of
three `;`-separated values. The first one is the person that bought the
stuff. The second value is a list of persons for whom the stuff was
bought and the third value is the amount of money that the buyer (the
first value) spent. Everything after `#` is a comment.

See also the file `example.txt`.


Output
------

So what would **zwegat**'s output for the above segment look like? Here
it is:

    eugen owes
      polina 0.90
      and spent 1.80

    wadim owes
      eugen 0.90
      and spent 5.46

    polina owes
      wadim 4.57
      and spent 4.57

As you can see there are no redundant debts. The amount that is listed
as "spent" is the amount of money that the person "owes himself" plus
all the other debts of that person. A currency symbol is deliberately
left out.


Features
--------

- Simplicity
- No redundant debts
- High precision arithmetic with python's Decimal library
- Okay error messages for syntax errors thanks to pyparsing


Miscellaneous
-------------

Run tests with `python tests.py`. You need to have
[nose](http://readthedocs.org/docs/nose/en/latest/) installed.
