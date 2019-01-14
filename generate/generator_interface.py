"""The command-line interface for the QGRAF generator

The main feature is the implementation of the GeneratorCmd class
"""
from cmd import Cmd
import qgraf_parser.generate.qgraf_setup as qgraf_setup
import subprocess
import os

import logging
logger=logging.getLogger(__name__)

class GeneratorCmd(Cmd):
    """The command-line interface for the QGRAF generator of qgraf_parser
    """
    prompt = 'QGRAF>'
    intro = "Welcome! Type ? to list commands"

    def valid_config(self):
        """Verify if the GeneratorCmd configuration has the correct entries"""
        config = self.config
        if not isinstance(config,dict):
            logger.error("The GeneratorCmd configuration is not a dictionnary")
            return False
        necessary_keys = [
            'model_file',
            'style_file',
            'options',
            'qgraf_executable',
            'output_file',
            'qgraf_template'
        ]
        for key in necessary_keys:
            if not key in config:
                logger.error("The key "+key+" is missing from the GeneratorCmd configuration")
                return False

        return True



    def __init__(self,*args,config,**kwargs):
        logger.info("Creating a Generator Command Line")
        Cmd.__init__(self,*args,**kwargs)

        self.config = config
        try:
            assert self.valid_config()
        except AssertionError as e:
            logger.error("Incorrect configuration when instantiating a GeneratorCmd")
            logger.error(e)
            raise

        self.process_config = None
        self.active_process = None


    def default(self, arg):
        """Quick actions"""
        if arg == 'x' or inp == 'q':
            return self.do_exit()

    def do_exit(self,arg):
        """Exit the command line"""
        logger.info("Exiting the Generator Command Line")
        return True

    def do_generate(self,arg):
        """Generate a qgraf process as 'initial_state > final_state @ n_loops'"""
        logger.info("Trying to generate a process:")
        logger.info(arg)
        try:
            process = qgraf_setup.parse_process_string(arg)
        except AssertionError as e:
            logger.error("Incorrect process syntax, cancelling generation")
            return
        process_param = dict(zip(("incoming","outgoing","n_loops"),process))

        # Here need to do things to validate the process within the model

        process_config = {**self.config,**process_param}
        self.process_config=process_config

    def do_show_process(self,arg):
        """Show the information on the process"""
        if self.process_config:
            msg = self.process_config['ingoing'] + '>' +  self.process_config['outgoing'] + '@'+ self.process_config['n_loops']
            print(msg)
        else:
            print("No process to be shown")

    def do_output(self,arg):
        """Output the necessary information for a process"""
        args=arg.split()
        if len(args)!=1:
            logger.error("The command output requires exactly one argument")
            logger.error("Cancelling output")
            return

        if self.process_config == None:
            logger.error("You need to generate a process before outputting")
            logger.error("Cancelling output")
            return


        # Create the process directory
        try:
            self.process_config['process_path']=qgraf_setup.create_process_directory(args[0])
        except IOError:
            logger.error("Cancelling output")
            return
        # Copy the model and style file sources into to process directory
        qgraf_setup.dispatch_qgraf_inputs(**self.process_config)

        #Generate the contents of the qgraf.dat file
        try:
            qgraf_datfile_content = qgraf_setup.generate_qgraf_data(**self.process_config)
        except NotImplementedError as e:
            logger.error("You need to regenerate a process without optional statements")
            logger.error("Cancelling output")
            return
        logger.info("Creating process data file in:")
        logger.info(os.path.join(self.process_config['process_path'],'qgraf.dat'))
        qgraf_datfile = open(os.path.join(self.process_config['process_path'],'qgraf.dat'),'w+')
        qgraf_datfile.write(qgraf_datfile_content)
        qgraf_datfile.close()
        logger.info("You can now generate this process using the 'launch' command")
        self.active_process = self.process_config['process_path']
        logger.info("Erasing the process config")
        self.process_config = None


    def do_launch(self,args):
        """
        TODO DOC
        Parameters
        ----------
        args :

        Returns
        -------

        """
        #######################
        # Input format checks
        #######################
        if len(args.split())>1:
            logger.error("The launch command can be called with:")
            logger.error("- 0 argument (launch active process)")
            logger.error("- 1 argument (launch specific process)")
            return
        # If no argument, check for active_process
        elif len(args)==0:
            process_path = self.active_process
        else:
            #TODO somehow sanitize inputs
            process_path = os.path.join(qgraf_setup.module_path,args)
            if not os.path.isdir(process_path):
                logger.error("The process directory {} is could not be found".format(args))

        # Save the directory we started from
        original_directory = os.getcwd()

        # Move to the process directory and run QGRAF
        # TODO: safety
        logger.info("Moving to the process directory:")
        logger.info(process_path)
        os.chdir(process_path)

        logger.info("Running qgraf")
        # We redirect the error output to the standard output
        # The option 'universal_newlines' ensures that newlines stay properly formatted
        # when converting to string and output
        qgraf_output = subprocess.check_output('qgraf',stderr=subprocess.STDOUT,universal_newlines=True)
        qgraf_output = str(qgraf_output)
        if "error" in qgraf_output.lower():
            logger.error("QGRAF generation has failed!")
            logger.error("See qgraf.log file to check qgraf output")
        else:
            logger.info("QGRAF generation has succeeded")
            for line in qgraf_output.splitlines():
                if "total" in line:
                    logger.info("Found {} diagrams".format(line.split()[2]))

        qgraf_logfile = open('qgraf.log',"w+")
        qgraf_logfile.write(qgraf_output)
        qgraf_logfile.close()

        logger.info('Returning to the original directory')
        os.chdir(original_directory)

