hydrocarbon
====

Simple board service which written in django, python.

Originally written for `hero·comics
<http://herocomics.kr/>`_.


Dependency
----------

* python >= 3.4.0
* see ``requirements.txt``


How to install
--------------

.. code-block:: console

   $ git clone git://github.com.devunt/hydrocarbon.git
   $ cd hydrocarbon
   $ pip install -r requirements.txt
   $ python manage.py syncdb
   $ python manage.py migrate
   $ python manage.py compilemessages
   $ python manage.py runserver


License
-------

see ``LICENSE`` file
