"""The command-line interface for the QGRAF generator

The main feature is the implementation of the GeneratorCmd class
"""
from cmd import Cmd
import qgraf_parser.generate.qgraf_setup as qgraf_setup
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

        process_dir = args[0]
        process_path = os.path.join(qgraf_setup.module_path,process_dir)
        if not os.path.exists(process_path):
            os.makedirs(process_path)
        else:
            logger.error("The chosen output path already exists")
            logger.error(process_path)
            logger.error("Cancelling output")
            return

        #self.process_config['output_file'] = os.path.join(process_path,self.process_config['output_file'])
        try:
            qgraf_datfile_content = qgraf_setup.generate_qgraf_data(**self.process_config)
        except NotImplementedError as e:
            logger.error("You need to regenerate a process without optional statements")
            logger.error("Cancelling output")
            return
        logger.info("Creating process data file in:")
        logger.info(os.path.join(process_path,'qgraf.dat'))
        qgraf_datfile = open(os.path.join(process_path,'qgraf.dat'),'w+')
        qgraf_datfile.write(qgraf_datfile_content)
        qgraf_datfile.close()
        logger.info("Erasing the process config")
        self.process_config = None

