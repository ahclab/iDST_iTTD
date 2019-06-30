# An Incremental Turn-Taking Model For Task-Oriented Dialog Systems

✍️ Andrei C. Coman<sup>1</sup>, Koichiro Yoshino<sup>2</sup>, Yukitoshi Murase<sup>2</sup>, Satoshi Nakamura<sup>2</sup>, Giuseppe Riccardi<sup>1</sup>  
🇮🇹 <sup>1</sup>Signals and Interactive Systems Lab, Department of Information Engineering and Computer Science, University of Trento, Italy  
🇯🇵 <sup>2</sup>Augmented Human Communication Laboratory, Graduate School of Information Science, Nara Institute of Science and Technology, Japan  
📍 INTERSPEECH 2019  
📝 https://arxiv.org/abs/1905.11806

### Abstract

In a human-machine dialog scenario, deciding the appropriate time for the machine to take the turn is an open research problem. In contrast, humans engaged in conversations are able to timely decide when to interrupt the speaker for competitive or non-competitive reasons. In state-of-the-art turn-by-turn dialog systems the decision on the next dialog action is taken at the end of the utterance. In this paper, we propose a token-by-token prediction of the dialog state from incremental transcriptions of the user utterance. To identify the point of maximal understanding in an ongoing utterance, we a) implement an incremental Dialog State Tracker which is updated on a token basis (iDST) b) re-label the Dialog State Tracking Challenge 2 (DSTC2) dataset and c) adapt it to the incremental turn-taking experimental scenario. The re-labeling consists of assigning a binary value to each token in the user utterance that allows to identify the appropriate point for taking the turn. Finally, we implement an incremental Turn Taking Decider (iTTD) that is trained on these new labels for the turn-taking decision. We show that the proposed model can achieve a better performance compared to a deterministic handcrafted turn-taking algorithm.

### Repository contents

* `Pipfile` and `Pipfile.lock` are libraries requirements containers for the `pipenv` virtual environment (https://github.com/pypa/pipenv)

* 📁 **idst_ittd_util**

	* `dstc2.py`: checks if DSTC2 dataset is in the root folder, otherwise it downloads it. This script performs also a raw features extraction.
	* `trivial.py`: logs some trivial strings

* 📁 **dstc2_scripts**: this folder contains the scripts necessary for the DSTC2 dataset. For instance `score.py` is used to score the output of the Dialog State Tracker.  
    **⚠️ NOTE**: Those scripts have been ported to `python3` from `python2` in order to be compliant with the python version used in the training scripts.  
    **⚠️ IMPORTANT**: Some of them have been modified in order to allow a direct function call from the training scripts. Please substitute the **dstc2_scripts** folder downloaded by the `dstc2.py` script with this folder.

* `[iDST_iTTD] data_analysis.ipynb`: data analysis script that provides some insights on the underlying data.

* `[iDST_iTTD] model_All.ipynb`: this script trains a single multi-target model. 

* `[iDST_iTTD] model_GMR.ipynb`: this script trains an ensemble of three models, namely: Goal (Pricerange, Area, Name, Food), Method and Requested.

* `[iDST_iTTD] model_PANFRM.ipynb`: this script trains an ensemble of six models, namely: Pricerange, Area, Name, Food, Requested and Method.