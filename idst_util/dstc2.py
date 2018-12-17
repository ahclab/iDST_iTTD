from idst_util import trivial
import os
import wget
import tarfile
import logging
logging.getLogger().setLevel(logging.INFO)

"""
Dialog State Tracker 2
> website: http://camdial.org/~mh521/dstc/
> files:
    > "dstc2_traindev.tar.gz" http://camdial.org/~mh521/dstc/downloads/dstc2_traindev.tar.gz
    > "dstc2_test.tar.gz" http://camdial.org/~mh521/dstc/downloads/dstc2_test.tar.gz
    > "dstc2_scripts.tar.gz" http://camdial.org/~mh521/dstc/downloads/dstc2_scripts.tar.gz
"""
#-----------------------------#

def print_dstc2():
    logging.info("+--------------------------------+")
    logging.info("| Dialog State Tracker 2 Utility |")
    logging.info("+--------------------------------+")

# DSTC2 default directory
dstc2_directory_name = "dstc2"

# DSTC2 dictories, files and links
dstc2_files = {("dstc2_traindev", "dstc2_traindev.tar.gz"): "http://camdial.org/~mh521/dstc/downloads/dstc2_traindev.tar.gz",
               ("dstc2_test", "dstc2_test.tar.gz"): "http://camdial.org/~mh521/dstc/downloads/dstc2_test.tar.gz",
               ("dstc2_scripts", "dstc2_scripts.tar.gz"): "http://camdial.org/~mh521/dstc/downloads/dstc2_scripts.tar.gz"}

def check(path = "."):
    print_dstc2()
    path = path if path[-1] != "/" else path[:-1]
    
    logging.info("Looking for {} directory in {}".format(dstc2_directory_name, path))
    dstc2_directory_name_found = os.path.isdir("{}/{}".format(path, dstc2_directory_name))
    
    if dstc2_directory_name_found:
        logging.info("{} was found!".format(dstc2_directory_name))
    else:
        logging.warning("{} was not found! Creating it...".format(dstc2_directory_name))
        os.mkdir("{}/{}".format(path, dstc2_directory_name))

    path = "{}/{}".format(path, dstc2_directory_name)
    
    for (directory_name, file_name), website_link in dstc2_files.items():
        logging.info("Looking for {} directory in {}".format(directory_name, path))
        directory_found = os.path.exists("{}/{}".format(path, directory_name))
        if directory_found:
            logging.info("{} was found!".format(directory_name))
            continue
        else:
            logging.warning("{} was not found!".format(directory_name))
            logging.info("Downloading {} from {}".format(file_name, website_link))
            wget.download(website_link, out = "{}/{}".format(path, file_name))
            logging.info("Extracting {}/{}".format(path, file_name))
            tar = tarfile.open("{}/{}".format(path, file_name), "r:gz")
            tar.extractall(path = "{}/{}".format(path, directory_name))
            tar.close()
            logging.info("Removing {}/{}".format(path, file_name))
            os.remove("{}/{}".format(path, file_name))
    logging.info("Done!")
