### INCREMENTAL LSTM-BASED DIALOG STATE TRACKER

🔗 Paper link: https://arxiv.org/pdf/1507.03471.pdf

### Introduction

A dialog state tracker is an important component in modern spoken dialog systems. It estimates the user's goals throughout the dialog by analyzing the automatic speech recognition (ASR) outputs for the user's utterances.

The **state-of-the-art** dialog state trackers achieve their top performance by learning from annotated data. However they still possess two undesirable properties:

* they can only track the dialog state turn-by-turn, as opposed to a more complicated word-by-word approach, which limits their interaction with users
* some of the trackers use an intermediate semantic representation and a spoken langue understanding (SLU) component. As the representation is manually crafted, it can cause loss of information, and an SLU, if used, is an aditional component of the dialog system that needs to be trained and tuned

The **main contribution** of this paper is a LSTM-based dialog state tracker called LecTrack. It naturally operates incrementally, word-by-word, and does not require an SLU. It learns from dialog sessions annotated by dialog state component labels at different time steps. The improvements consist of including the ASR confidence scores, abstracting scarcely represented values, including transcriptions in the training data, and model averaging.

### Task

The task of dialog state tracking is to monitor progress in the dialog and provide a compact representation of the dialog history in the form of a _dialog state_. Statistical dialog systems thus maintain a distribution over all possible states, called _belief state_. As the dialog progresses, the dialog state tracker updates this distribution given new observations as follows:

* a dialog state at time _t_ can be seen as a vector _s<sub>t</sub>_ &isin; _C<sub>1</sub>_ x ... x _C<sub>k</sub>_ of _k_ dialog state components (slots)

* each component _c<sub>i</sub>_ &isin; _C<sub>i</sub>_ = {_v<sub>i</sub>_, ..., _v<sub>n</sub>}_ takes one of the _n<sub>i</sub>_ values, and independency between components is assumed:
	_P(s<sub>t</sub> | v<sub>1</sub>, ..., v<sub>t</sub>) = &#8719;<sub>i</sub> p(c<sub>i</sub> | v<sub>i</sub>_, ..., _v<sub>t</sub>, &theta;)_

This paper dialog state tracker, gives the probability distribution only over on of the independent components _p(c<sub>i</sub> | v<sub>i</sub>_, ..., _v<sub>t</sub>)_. A prediction for more components together is made independently by running different models, specific for each component _i_

### LecTrack Model

The tracker maps a sequence of words in the dialog to a probability distribution over the values of a dialog state component _p_ and it does it by means of the following pipeline:

* an input neural network that maps the word _a_ and its ASR confidence score _r_ to a joint representation _u_:
	
	_u = NN(a,r)_

* the representation _u_ is used by the LSTM encoder along with the previous hidden state _q<sub>t-1</sub> = (c<sub>t-1</sub>, h<sub>t-1</sub>)_ to create a new hidden state _q<sub>t</sub>_:

	_q<sub>t</sub> = Enc(u, q<sub>t-1</sub>)_

* the classifier, represented by a single softmax layer, then maps the hidden state to a probability distribution over all possible values:

	_p<sub>t</sub> = C(h<sub>t</sub>)_

### Improvements

Different improvements have been introduced:

* **including ASR scores**: they decided to include the confidence score of the input hypothesis as an additional dimension to each input word embedding, and add one fully-connected non-linear layer between this input and the LSTM, so that the model can learn to transform the embeddgins according to the confidence score

* **including transcriptions in training data**: since the training data is noisy due to ASR errors, it is a common practice to expand the training set to reduce the noise. They thus decided to mix the ASR 1-best hypotheses with the true manually-transcribed user utterances to form an expanded traning set, which should reduce the amount of noise

* **model averaging**: in order to boost the performance of the models, simple model averaging strategy can be employed. They trained 10 different models from 10 different random initializations and average their predictions.

* **abstracting low-occuring values**: since the model has little chance of learning to properly predict state component values that do not occur frequently in the training data set, they thus decided to substitute the ones that occur less than 40 times in the training set by an abstract value. Occurences of the same value are replaced by some abstract token, and if a different value is encountered we create another abstract token. This modification makes the tracker able to track values that it has never seen in the training data, by manually putting them in the abstraction dictionary.
