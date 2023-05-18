# Helion

![](https://img.shields.io/badge/python-3.7-brightgreen.svg)

Helion is a data-driven framework that models the regularities of user-driven home automation, generates natural home automation scenarios, and provides stakeholders with tools to use the scenarios and obtain actionable outcomes.

## Getting Started

### Setup

#### 1. Download necessary files and store them in a location where you can easily access them

Our recommendation is to create and store these in `helion/libs/`, some of which we provide in this repo (marked as **provided**).

- [MITLM 0.4.2](https://github.com/mitlm/mitlm/releases/tag/v0.4.2) - MIT Language Modeling Toolkit (**provided**).
-  Please install [GForTran](https://gcc.gnu.org/wiki/GFortranBinaries#MacOS) if you get an error while building MITLM. On Mac, you can simply run `brew install gfortran`
- [Python Daemon](https://pypi.python.org/pypi/python-daemon/) - Library to implement a well-behaved Unix daemon process.
- [Brain Files](https://github.com/martingwhite/kramer) - The language model server script which reads/writes JSON documents to named pipes. (**provided**)  

#### 2. Untar MITLM

Execute the following command to un-tar the the MITLM and python-daemon packages:

`tar -xzf <package_name.tar.gz>`

#### 3. Add proper directories to your path

Execute the Following commands or add them to your .bash_profile (or relevant profile) to set up your `$PATH` and `$PYTHONPATH`.

**Be sure to replace the paths with local paths on your machine**

```sh
#for conda
export PYTHONPATH=$PYTHONPATH:/Users/<user>/miniconda3/
# for Python-Daemon
export PYTHONPATH=$PYTHONPATH:/Users/<user>/miniconda3/envs/python3.8/lib/python3.8/site-packages/daemon/
# for mitlm
export PATH=$PATH:/Users/<user>/Helion-on-Home-Assistant/helion/libs/mitlm-0.4.2/
# for braind
export PATH=$PATH:/Users/<user>/Helion-on-Home-Assistant/helion/libs/kramer/
```

#### 4. Build MITLM

Navigate to the `mitlm-0.4.2/` directory and execute the following commands:

```
./configure
make
```
After both of these commands have been executed, you should be able to see the estimate-ngram, evaluate-ngram, and interpolate-ngram executables in the mitlm-0.4.2/ directory.

#### 5. Instantiate the Brain:

Navigate to `helion/` directory. Instantiate the brain by running:

```sh
braind data/generated_data/training/training_model/helion.train data/generated_data/training/training_model/helion.vocab
```

#### For windows users, if the brain runs into `CalledProcessorError()`, there is a chance that files to be used are formatted in CRLF rather than LF. Because we are utilizing WSL, it is necessary to ensure that these files's line endings are formatted in LF.

To do this, open helion.vocab and helion.train located in helion/data/generated_data/training/training_model/ folder with your IDE. At the bottom of your IDE, you should see the format of the file (LF or CRLF). Click on the text and an option to select the format will appear likely at the top of the screen. Select LF.

Reinstantiate the brain by running the above mentioned command.

### Acknowledgements:

- [Kramer](https://github.com/martingwhite/kramer)
- [MITLM](https://github.com/mitlm/mitlm)
- [python-daemon](https://pypi.org/project/python-daemon/)
