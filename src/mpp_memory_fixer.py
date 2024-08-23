#.................................................
#   MPP_MEMORY_FIXER.PY, v1.0.0, April 2024, Domenico Lanza.
#.................................................
#   This module is needed to temporarily fix a memory leak in the MPP library.
#.................................................

import mutationpp as mpp
import os

def create_mixture_file(MIXTURE_NAME):
    """This function is used to create a mixture file.

    Args:
        MIXTURE_NAME (str): The name of the mixture
    """
    # Variables
    f = None  # File object
    filename = None  # File name
    # Create a file
    filename = MIXTURE_NAME + ".xml"
    f = open(filename, "w")
    # Write the mixture
    f.write("<!-- Temporary mixture-->\n")
    f.write("<mixture state_model=\"EquilTP\">\n")
    f.write("\t<species>\n")
    f.write("\t\tN2 N2+ N N+ e-\n")
    f.write("\t</species>\n")
    f.write("\t\n")
    f.write("\t<element_compositions default=\"default\">\n")
    f.write("\t\t<composition name=\"default\"> N2:1.0, N2+:0.0, N:0.0, N+:0.0, e-:0.0 </composition>\n")
    f.write("\t</element_compositions>\n")
    f.write("</mixture>\n")
    f.close()
    
def delete_mixture_file(MIXTURE_NAME):  
    """This function is used to delete the mixture file.

    Args:
        MIXTURE_NAME (str): The name of the mixture
    """
    # Variables
    filename = None  # File name
    # Delete the file
    filename = MIXTURE_NAME + ".xml"
    try:
        os.remove(filename)
    except:
        pass

def fix_mpp_memory_leak():
    """This function is needed to temporarily fix a memory leak in the MPP library.
    """
    # Constants
    MIXTURE_NAME = "temporarily_mixture_file"
    # Variables
    mix = None  # Mixture object
    # I create the mixture file
    create_mixture_file(MIXTURE_NAME)
    # Create a Mixture object
    mix = mpp.Mixture(MIXTURE_NAME)