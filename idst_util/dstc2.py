from idst_util import trivial
from tqdm import tqdm
import os
import copy
import wget
import tarfile
import json
import nltk
nltk.download("punkt")
import logging
logging.getLogger().setLevel(logging.INFO)

"""
Dialog State Tracker Challenge 2
> website: http://camdial.org/~mh521/dstc/
> files:
    > "dstc2_traindev.tar.gz" http://camdial.org/~mh521/dstc/downloads/dstc2_traindev.tar.gz
    > "dstc2_test.tar.gz" http://camdial.org/~mh521/dstc/downloads/dstc2_test.tar.gz
    > "dstc2_scripts.tar.gz" http://camdial.org/~mh521/dstc/downloads/dstc2_scripts.tar.gz
"""

# DSTC2 default directory
DSTC2_DIRECTORY_NAME = "dstc2"

# DSTC2 dictories, files and links
DSTC2_FILES = {("dstc2_traindev", "dstc2_traindev.tar.gz"): "http://camdial.org/~mh521/dstc/downloads/dstc2_traindev.tar.gz",
               ("dstc2_test", "dstc2_test.tar.gz"): "http://camdial.org/~mh521/dstc/downloads/dstc2_test.tar.gz",
               ("dstc2_scripts", "dstc2_scripts.tar.gz"): "http://camdial.org/~mh521/dstc/downloads/dstc2_scripts.tar.gz"}

"""
This function searches, in the provided path, for the following directories:
    > dstc2
    > dstc2/dstc2_traindev
    > dstc2/dstc2_test
    > dstc2/dstc2_scripts
If the provided path does not contain the dstc2 directory, it will be created.
Moreover the dstc2_traindev, dstc2_test and dstc2_scripts packages will be downloaded and extracted. 
"""
def check(path = "."):
    logging.info("+--------------------------------+")
    logging.info("|     Dialog State Tracker 2     |")
    logging.info("|         Data Checker           |")
    logging.info("+--------------------------------+")
    
    logging.info("Looking for {} directory in {}".format(DSTC2_DIRECTORY_NAME, path))
    dstc2_directory_name_found = os.path.isdir(os.path.join(path, DSTC2_DIRECTORY_NAME))
    
    if dstc2_directory_name_found:
        logging.info("{} was found!".format(DSTC2_DIRECTORY_NAME))
    else:
        logging.warning("{} was not found! Creating it...".format(DSTC2_DIRECTORY_NAME))
        os.mkdir(os.path.join(path, DSTC2_DIRECTORY_NAME))

    path = os.path.join(path, DSTC2_DIRECTORY_NAME)
    
    for (directory_name, file_name), website_link in DSTC2_FILES.items():
        logging.info("Looking for {} directory in {}".format(directory_name, path))
        directory_found = os.path.exists(os.path.join(path, directory_name))
        if directory_found:
            logging.info("{} was found!".format(directory_name))
        else:
            logging.warning("{} was not found!".format(directory_name))
            logging.info("Downloading {} from {}".format(file_name, website_link))
            wget.download(website_link, os.path.join(path, file_name))
            logging.info("Extracting {}/{}".format(path, file_name))
            tar = tarfile.open(os.path.join(path, file_name), "r:gz")
            tar.extractall(path = os.path.join(path, directory_name))
            tar.close()
            logging.info("Removing {}/{}".format(path, file_name))
            os.remove(os.path.join(path, file_name))
    logging.info("Done!")

def extract_raw_features(data_directory, flist, ontology, data_augmentation = False):
    X = []
    Y = []
    for dialog_path in tqdm(flist):
        dialog_directory = os.path.join(data_directory, dialog_path)
        log_json_path = os.path.join(dialog_directory, "log.json")
        label_json_path = os.path.join(dialog_directory, "label.json")
        log_json = {}
        label_json = {}
        with open(log_json_path, "r") as log_json_file, open(label_json_path, "r") as label_json_file:
            log_json = json.load(log_json_file)
            label_json = json.load(label_json_file)
        
        X_dialog = {}
        X_dialog["session-id"] = log_json["session-id"]
        X_dialog["turns"] = []
        Y_dialog = {}
        Y_dialog["session-id"] = log_json["session-id"]
        Y_dialog["turns"] = []
        
        # LecTreck: 3.2.2 Including Transcriptions in Training Data
        X_dialog_augmented = {}
        X_dialog_augmented["session-id"] = log_json["session-id"]
        X_dialog_augmented["turns"] = []
        Y_dialog_augmented = {}
        Y_dialog_augmented["session-id"] = log_json["session-id"]
        Y_dialog_augmented["turns"] = []
        
        for log_turn, label_turn in zip(log_json["turns"], label_json["turns"]):
            
            # X_turn
            X_dialog_turn = {}
            X_dialog_turn["system"] = []
            X_dialog_turn["user"] = []
            # X_turn: dialog-act
            for dialog_act in log_turn["output"]["dialog-acts"]:
                act = dialog_act["act"]
                slots = dialog_act["slots"]
                X_dialog_turn["system"].append((act, 0))
                if len(slots) != 0:
                    for slot in slots:
                        for slot_element in slot:
                            slot_element = str(slot_element) # this is for the count in test
                            for slot_value in nltk.word_tokenize(slot_element):
                                X_dialog_turn["system"].append((slot_value, 0))
            # X_turn: asr-hyps
            asr_hyps = log_turn["input"]["live"]["asr-hyps"]
            asr_hyp = asr_hyps[0]["asr-hyp"]
            asr_score = asr_hyps[0]["score"]
            for asr_token in nltk.word_tokenize(asr_hyp):
                X_dialog_turn["user"].append((asr_token, asr_score))
            X_dialog["turns"].append(X_dialog_turn)
            
            # Y_turn
            Y_dialog_turn = {}
            Y_dialog_turn["method"] = None
            Y_dialog_turn["requested"] = []
            Y_dialog_turn["goal"] = {}
            Y_dialog_turn["goal"]["food"] = None
            Y_dialog_turn["goal"]["pricerange"] = None
            Y_dialog_turn["goal"]["name"] = None
            Y_dialog_turn["goal"]["area"] = None
            # Y_turn: method-label
            Y_dialog_turn["method"] = label_turn["method-label"]
            # Y_turn: requested-slots
            Y_dialog_turn["requested"] = label_turn["requested-slots"]
            Y_dialog_turn["goal"]["food"] = label_turn["goal-labels"].get("food", None)
            Y_dialog_turn["goal"]["pricerange"] = label_turn["goal-labels"].get("pricerange", None)
            Y_dialog_turn["goal"]["name"] = label_turn["goal-labels"].get("name", None)
            Y_dialog_turn["goal"]["area"] = label_turn["goal-labels"].get("area", None)
            Y_dialog["turns"].append(Y_dialog_turn)
            
            assert len(X_dialog["turns"]) == len(Y_dialog["turns"])
            
            # LecTreck: 3.2.2 Including Transcriptions in Training Data 
            if data_augmentation:
                X_dialog_turn_augmented = copy.deepcopy(X_dialog_turn)
                Y_dialog_turn_augmented = copy.deepcopy(Y_dialog_turn)
                X_dialog_turn_augmented["user"] = []
                transcription = label_turn["transcription"]
                for transcription_token in nltk.word_tokenize(transcription):
                    X_dialog_turn_augmented["user"].append((transcription_token, 0))
                X_dialog_augmented["turns"].append(X_dialog_turn_augmented)
                Y_dialog_augmented["turns"].append(Y_dialog_turn_augmented)
            
            # LecTreck: 3.2.2 Including Transcriptions in Training Data
            if data_augmentation:
                assert len(X_dialog_augmented["turns"]) == len(Y_dialog_augmented["turns"])
                assert len(X_dialog["turns"]) == len(X_dialog_augmented["turns"])
            
        X.append(X_dialog)
        Y.append(Y_dialog)
        
        # LecTreck: 3.2.2 Including Transcriptions in Training Data
        if data_augmentation:
            X.append(X_dialog_augmented)
            Y.append(Y_dialog_augmented)
        
    return X, Y        


def retrieve_raw_datasets(train_data_augmentation = False):
    logging.info("+--------------------------------+")
    logging.info("|     Dialog State Tracker 2     |")
    logging.info("|       Dataset Retrieval        |")
    logging.info("+--------------------------------+")
    
    # TRAINDEV
    logging.info("Reading dstc2_train.flist, dstc2_dev.flist and ontology_dstc2.json")
    traindev_directory_path = os.path.join(DSTC2_DIRECTORY_NAME, "dstc2_traindev")
    traindev_data_directory = os.path.join(traindev_directory_path, "data")
    traindev_config_directory = os.path.join(traindev_directory_path, "scripts", "config")
    train_flist_path = os.path.join(traindev_config_directory, "dstc2_train.flist")
    dev_flist_path = os.path.join(traindev_config_directory, "dstc2_dev.flist")
    dstc2_ontology_path = os.path.join(traindev_config_directory, "ontology_dstc2.json")
    train_flist = []
    dev_flist = []
    dstc2_ontology = {}
    with open(train_flist_path, "r") as train_flist_file, open(dev_flist_path, "r") as dev_flist_file:
        train_flist = train_flist_file.read().split()
        dev_flist = dev_flist_file.read().split()
    assert len(train_flist) == 1612 #according to handbook
    logging.info("Asserted 1612 dialogs for dstc2_train.flist")
    assert len(dev_flist) == 506 #according to handbook
    logging.info("Asserted 506 dialogs for dstc2_dev.flist")
    with open(dstc2_ontology_path, "r") as dstc2_ontology_file:
        dstc2_ontology = json.load(dstc2_ontology_file)
    
    # TRAIN
    logging.info("Extracting raw train features")
    X_train, Y_train = extract_raw_features(data_directory = traindev_data_directory,
                                            flist = train_flist,
                                            ontology = dstc2_ontology,
                                            data_augmentation = train_data_augmentation)    
    
    # DEV
    logging.info("Extracting raw dev features")
    X_dev, Y_dev = extract_raw_features(data_directory = traindev_data_directory,
                                        ontology = dstc2_ontology,
                                        flist = dev_flist)
    
    # TEST
    logging.info("Reading dstc2_test.flist")
    test_directory_path = os.path.join(DSTC2_DIRECTORY_NAME, "dstc2_test")
    test_data_directory = os.path.join(test_directory_path, "data")
    test_config_directory = os.path.join(test_directory_path, "scripts", "config")
    test_flist_path = os.path.join(test_config_directory, "dstc2_test.flist")
    test_flist = []
    with open(test_flist_path, "r") as test_flist_file:
        test_flist = test_flist_file.read().split()
    assert len(test_flist) == 1117 #according to handbook
    logging.info("Asserted 1117 dialogs for dstc2_test.flist")
    logging.info("Extracting raw test features")
    X_test, Y_test = extract_raw_features(data_directory = test_data_directory,
                                          ontology = dstc2_ontology,
                                          flist = test_flist)
 
    return X_train, Y_train, X_dev, Y_dev, X_test, Y_test, dstc2_ontology