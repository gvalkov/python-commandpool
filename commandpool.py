import time
import subprocess


#-------------------------------------------------------------------------------
# API
#-------------------------------------------------------------------------------

class ConcurrentCommandRunner:
    '''Run subprocess commands in parallel.'''

    def __init__(self, commands, concurrency=None, sleep_seconds=0.5):
        '''
        Parameters
        ----------
        commands: iterable
            The commands to execute.
        concurrency: int or None
            Maximum number of commands to run at any given time. If None,
            all commands are started simultaneously.
        sleep_seconds: float
            Seconds to sleep in-between checking the status of commands.
        '''

        self.commands = commands
        self.commands_iter = iter(commands)
        self.sleep_seconds = sleep_seconds

        self.concurrency = concurrency if concurrency else len(commands)

        self.processes = {}
        self.finished_processes = {}
        self.finished = False

    def run(self):
        '''
        Run until all processes are completed. Returns the sum of the exit-codes
        of all commands.
        '''
        if not self.commands:
            return

        for _ in range(self.concurrency):
            self.start_next_cmd()

        while not self.finished or self.processes:
            self.tick()

        return self.returncode

    def returncode(self):
        '''The sum of the exit-codes of all commands.'''
        return sum(proc.returncode for proc in self.finished_processes)

    def tick(self):
        proc_to_remove = []
        for proc in self.processes:
            if proc.poll() is not None:
                proc_to_remove.append(proc)

        # We're done with these processes - don't check their status again.
        for proc in proc_to_remove:
            self.command_finished(proc, self.processes[proc])
            self.finished_processes[proc] = self.processes[proc]
            del self.processes[proc]

        # Start as many processes as have finished.
        for _ in range(len(proc_to_remove)):
            self.start_next_cmd()

        time.sleep(self.sleep_seconds)

    def start_next_cmd(self):
        try:
            cmd = next(self.commands_iter)
        except StopIteration:
            self.finished = True
            return

        proc = self.start_command(cmd)
        self.processes[proc] = cmd

    def start_command(self, cmd):
        '''
        Start a command - must return a subprocess.Popen object.
        The single 'cmd' argument is an element of self.commands.
        '''
        return subprocess.Popen(cmd, shell=isinstance(cmd, str))

    def command_finished(self, proc, cmd):
        '''
        Ran when a command has finished. Receives the subprocess.Popen
        object and the corresponding command element from which it was
        created.
        '''
        pass


#-------------------------------------------------------------------------------
# Functional interface
#-------------------------------------------------------------------------------

def run(commands, concurrency=None, sleep_seconds=0.5, start_command=None):
    '''
    Run subprocess commands in parallel and yield the results kj

    Parameters
    ----------
    commands: iterable
        The commands to execute.
    concurrency: int or None
        Maximum number of commands to run at any given time. If None,
        all commands are started simultaneously.
    sleep_seconds: float
        Seconds to sleep in-between checking the status of commands.
    start_command: callable
        Function used to start commands. Must return a subprocess.Popen object.

    Yields
    ------
    (subprocess.Popen, cmd)
        Yields the completed subprocess.Popen object and the command element
        from which it was created.
    '''
    import queue
    import threading

    result_queue = queue.Queue()

    def command_finished(proc, cmd):
        result_queue.put((proc, cmd))

    def run_commands():
        run_with_callback(commands, concurrency, sleep_seconds, command_finished, start_command)
        result_queue.put(None)

    t1 = threading.Thread(target=run_commands, name=threading._newname('ConcurrentCommandRunner-%d'))
    t1.start()

    for proc, cmd in iter(result_queue.get, None):
        yield proc, cmd


def run_with_callback(commands, concurrency=None, sleep_seconds=0.5, command_finished=None, start_command=None):
    '''
    Run subprocess commands in parallel and pass the results of finished commands to a callback

    Parameters
    ----------
    commands: iterable
        The commands to execute.
    concurrency: int or None
        Maximum number of commands to run at any given time. If None,
        all commands are started simultaneously.
    sleep_seconds: float
        Seconds to sleep in-between checking the status of commands.
    command_finished: callable or None
        Function to call when a process finished. Receives the finished subprocess.Popen
        object and the command object from which it was created.
    start_command: callable or None
        Function used to start commands. Must return a subprocess.Popen object.

    Returns
    -------
    int
        The sum of the exit-codes of all commands.
    '''
    runner = ConcurrentCommandRunner(commands, concurrency, sleep_seconds)
    if start_command:
        runner.start_command = start_command
    if command_finished:
        runner.command_finished = command_finished
    return runner.run()


#-------------------------------------------------------------------------------

__all__ = ConcurrentCommandRunner, run, run_with_callback
