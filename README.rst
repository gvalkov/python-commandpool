Commandpool
===========

.. class:: no-web no-pdf

|pypi| |build| |license|

Utility classes and functions for running subprocess commands in parallel:

.. code-block:: python

  >>> from random import randrange
  >>> from commandpool import run

  >>> commands = ['sleep %s' % randrange(5) for _ in range(100)]

  >>> for proc, cmd in run(commands):
  ...    print(proc.returncode, proc, cmd, sep=', ')
  0, <subprocess.Popen object at 0x7fa470b5e278>, sleep 1
  0, <subprocess.Popen object at 0x7fa470b449b0>, sleep 2
  0, <subprocess.Popen object at 0x7fa470b53d30>, sleep 2
  0, <subprocess.Popen object at 0x7fa470b44b70>, sleep 3
  0, <subprocess.Popen object at 0x7fa470b53cf8>, sleep 3
  0, <subprocess.Popen object at 0x7fa470b53d68>, sleep 4

One way to look at the functionality provided by this library is like a
`subprocess`_ equivalent of:

.. code-block:: shell

  echo $commands | xargs -P $concurrency sh -c

This library works by periodically checking if started processes have finished
and then starting new ones in their place.

Installation
------------

The latest stable version of commandpool can be installed from pypi:

.. code-block:: bash

  $ pip install commandpool


Usage
-----

Functional
~~~~~~~~~~

.. code-block:: python

  from commandpool import run

  # Run at most 5 commands at a time.
  run(commands, concurrency=5)

  # Start all commands at the same time (this is the default).
  run(commands, concurrency=None)

  # The duration between 'ticks' is configurable.
  run(commands, sleep_seconds=0.1)

  # Processing commands as they are finished.
  for proc, cmd in run(commands):
      assert isinstance(proc, subprocess.Popen)

  # The way commands are started is configurable through `start_command`.
  from subprocess import Popen, PIPE

  commands = {i: ('echo', i*i) for i in range(5, 10)}
  start_command = lambda num: Popen(commands[num], stdout=PIPE)

  for proc, cmd in run(commands, start_command=start_command):
      print(proc.stdout, cmd, commands[cmd])
  # b'25', 5, ('echo', 25)
  # b'36', 6, ('echo', 36)
  # ...


Subclassing
~~~~~~~~~~~

.. code-block:: python

  from commandpool import ConcurrentCommandRunner

  class MyCommandRunner(ConcurrentCommandRunner):
     def start_command(self, cmd):
         ...

     def command_finished(self, proc, cmd):
         ...

  runner = MyCommandRunner(commands, sleep_interval=1.0)
  runner.run()


Todo
----

- Add tests.

- Complete documentation.


Alternatives
------------

``ConcurrentCommandRunner`` can be implemented in a few lines with the help of
`concurrent.futures`_, assuming that spawning a thread per command is
acceptable. This also has the added benefit of yielding as soon as a command
(wrapped in a future) is complete, instead of at ``sleep_seconds`` intervals, as
is the case with ``ConcurrentCommandRunner``.

.. code-block:: python

  from concurrent.futures import ThreadPoolExecutor, as_completed
  from subprocess import run

  with ThreadPoolExecutor(max_workers=10) as pool:
     futures = {pool.submit(run, cmd): cmd for cmd in commands}
     for res in as_completed(futures):
         print(futures[res], res.returncode)


License
-------

Released under the terms of the `Revised BSD License`_.


.. |pypi| image:: https://img.shields.io/pypi/v/commandpool.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/commandpool
    :alt: Latest version released on PyPi

.. |license| image:: https://img.shields.io/pypi/l/commandpool.svg?style=flat-square&label=license
    :target: https://pypi.python.org/pypi/commandpool
    :alt: BSD 3-Clause

.. |build| image:: https://img.shields.io/travis/gvalkov/python-commandpool/master.svg?style=flat-square&label=build
    :target: http://travis-ci.org/gvalkov/python-commandpool
    :alt: Build status

.. _`Revised BSD License`: https://raw.github.com/gvalkov/python-commandpool/master/LICENSE
.. _subprocess: https://docs.python.org/3/library/subprocess.html
.. _`concurrent.futures`: https://docs.python.org/3/library/concurrent.futures.html
