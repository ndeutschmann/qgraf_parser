import re
import os
from shutil import copyfile
from sys import path
from ..generator import module_path
import logging
logger=logging.getLogger(__name__)



def sanitize_input_file_path(file_path):
    """Check if a file is available in the module path, otherwise in the python path"""
    #TODO instead of module path this shoud look in a subdirectory like 'resources'

    # Loop for the file in the module (qgraf_parser.generator) path
    if os.path.isfile(os.path.join(module_path,file_path)):
        return os.path.join(module_path,file_path)
    # Is the file accessible directly?
    elif os.path.isfile(file_path):
        return file_path
    else:
        error = FileNotFoundError("File "+file_path+" not found")
        logger.error(error)
        raise error


def generate_qgraf_data(*,
                        qgraf_template,
                        output_file,
                        style_file,
                        model_file,
                        incoming,
                        outgoing,
                        n_loops,
                        options,
                        optional_statements=(),
                        **kwargs):
    """Fill in the qgraf.dat template from a set

    Parameters
    ----------
    qgraf_template : str
        path to the template file to fill in
    output_file : str
        path to the qgraf output file
    style_file : str
        path to the qgraf style file
    model_file : str
        path to the qgraf model
    incoming : list of str
        list of names of particles in the initial state
    outgoing :
        list of names of particles in the final state
    n_loops: int
        number of loops
    options : list of str
        list of options for qgraf
    optional_statements : list of str
        list of optional statements for QGRAF

    Returns
    -------
    str
        The text content of the desired qgraf.dat file
    """

    # For now we do not support optional_statements
    if optional_statements!=():
        logger.error("We currently do not support optional statements for QGRAF")
        error = NotImplementedError("Optional statements not yet implemented in QGRAF handler")
        logger.error(error)
        raise error

    format_dict = {
        "output_file": output_file,
        "style_file": os.path.basename(style_file),
        "model_file": os.path.basename(model_file),
        "incoming": ", ".join(incoming),
        "outgoing": ", ".join(outgoing),
        "n_loops": n_loops,
        "options": ",".join(options),
        "optional_statements": ""
    }


    with open(sanitize_input_file_path(qgraf_template)) as template_file:
        return template_file.read().format(**format_dict)


def parse_process_string(process_string):
    """Parse a process string of the form
    p1 p2 ... pn > q1 ... qm [@ l]
    into QGRAF input options: `in`, `out`, and `loops`.

    Parameters
    ----------
    process_string :

    Returns
    -------
    dict
        {"incoming": str, "outgoing": str}
    """

    pattern_string = "^[a-zA-Z0-9 ]+>[a-zA-Z0-9 ]+(@[ ]*[0-9]+){0,1}[ ]*$"
    pattern = re.compile(pattern_string)
    try:
        assert pattern.match(process_string)
    except AssertionError as e:
        logger.error("The process string does not match the expected format:")
        logger.error("p1 p2 ... pn > q1 ... qm [@ l]")
        logger.error("Regex: "+pattern_string)
        logger.error("Received: "+process_string)
        logger.error(e)
        raise

    process_string_and_loops = process_string.split("@")
    pure_process_string = process_string_and_loops[0]
    n_loops=0
    if len(process_string_and_loops)==2:
        n_loops = int(process_string_and_loops[1].strip(" "))
    elif len(process_string_and_loops)!=1:
        logger.error("Unknown error with the input string")
        logger.error("Here is the expected format:")
        logger.error("p1 p2 ... pn > q1 ... qm [@ l]")
        logger.error("Regex: "+pattern_string)
        logger.error("Received: "+process_string)
        logger.error("The normal input filter has failed. Please contact the author")
        error = IOError("The process loop has passed the pattern checks but something is wrong")
        logger.error(error)
        raise error

    # The initial state and final state are separated by '>' and each is a sequence of alphanumeric particle names
    # separated by spaces.
    # We use split() to ignore multiple spaces as well as initial and trailing whitespace characters.
    ingoing,outgoing = [x.split() for x in pure_process_string.split(">")]
    return ingoing,outgoing,n_loops


def valid_particle_list(particles,model):
    """Check whether a list of particles is made up of particle in the model

    Parameters
    ----------
    particles : list of str
        list of particle names/symbols
    model : module
        Python module describing a model. It must have an attribute particles which is a
        qgraf_parser.models.common_tools.abstract_objects.ParticleDict object

    Returns
    -------
    bool
        Is this list a valid list of particles in the model?
    """

    return all([p in model.particles for p in particles])

def create_process_directory(process_dir):
    """
    TODO DOC
    TODO A Process directory should always be created in the generator submodule. There should be a safety check
    Parameters
    ----------
    process_dir :

    Returns
    -------

    """
    process_path = os.path.join(module_path, process_dir)
    if not os.path.exists(process_path):
        logger.info('Creating the process directory:')
        logger.info(process_path)
        os.makedirs(process_path)
        return process_path
    else:
        error = IOError("The chosen output path already exists")
        logger.error(error)
        logger.error(process_path)
        raise error


def dispatch_qgraf_inputs(*,
                          process_path,
                          style_file,
                          model_file,
                          **kwargs):
    """
    TODO DOC
    Parameters
    ----------
    process_path :
    style_file :
    model_file :
    kwargs :

    Returns
    -------

    """
    # If the filename is not in the path, look for it in the default location in the module
    style_file_src = sanitize_input_file_path(style_file)
    model_file_src = sanitize_input_file_path(model_file)

    # We will copy these files to the process directory
    style_file_tgt = os.path.join(process_path,os.path.basename(style_file))
    model_file_tgt = os.path.join(process_path,os.path.basename(model_file))
    logger.info("Copying the style file to the process directory")
    copyfile(style_file_src,style_file_tgt)
    logger.info("Copying the model file to the process directory")
    copyfile(model_file_src,model_file_tgt)
