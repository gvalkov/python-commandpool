Commandpool
===========

.. class:: no-web no-pdf

|pypi| |build| |license|

Functions for running subprocesses in parallel without fuss or threads.

.. code-block:: python

  from commandpool import run

  commands = [...]

  # Start all commands at the same time.
  run(commands)

  # Run at most 5 commands at a time.
  run(commands, concurrency=5)

  # run() returns a generator that yields completed commands.
  for proc, cmd in run(commands):
      assert proc.returncode != None

Please refer to the *usage* section for more information.


Installation
------------

The latest stable version of commandpool can be installed from pypi:

.. code-block:: bash

  $ pip install commandpool


Usage
-----

.. code-block:: python

  from commandpool import run

  # Run at most 5 commands at a time.
  run(commands, concurrency=5)

  # Start all commands at the same time (this is the default).
  run(commands, concurrency=None)

  # The command-check interval is configurable though `sleep_seconds`.
  run(commands, sleep_seconds=0.1)

  # Processing commands as they are done.
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


Todo
----

- Add tests.

- Complete documentation.


Alternatives
------------

The ``run()`` function can be implemented in a few lines with the help
of `concurrent.futures`_, assuming that spawning a thread per command
is acceptable.

.. code-block:: python

  from concurrent.futures import ThreadPoolExecutor, as_completed
  from subprocess import run

  with ThreadPoolExecutor(max_workers=10) as pool:
     futures = {pool.submit(run, cmd): cmd for cmd in commands}
     for res in as_completed(futures):
         print(futures[res], res.returncode)

The above also has the advantage of yielding as soon as commands are done
instead of at ``sleep_seconds`` intervals, as is the case with ``run()``.

There is also nothing wrong with just shelling-out to ``xargs`` if you don't
need the extra flexibility that commandpool provides.

.. code-block:: python

  from subprocess import run
  run('xargs -0P 5 sh -c', shell=True, stdin=b'\0'.join(commands))


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
