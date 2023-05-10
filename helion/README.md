# Helion

![](https://img.shields.io/badge/python-3.7-brightgreen.svg)

Helion is a data-driven framework that models the regularities of user-driven home automation, generates natural home automation scenarios, and provides stakeholders with tools to use the scenarios and obtain actionable outcomes.

## Getting Started

### Setup:

#### 1. Download necessary files and store them in a location where you can easily access them:

( Our recommendation is to create and store these in /helion/libs )

- [MITLM 0.4.1](https://github.com/mitlm/mitlm/releases/tag/v0.4.1) - MIT Language Modeling Toolkit
- [Python Daemon](https://pypi.python.org/pypi/python-daemon/) - Library to implement a well-behaved Unix daemon process.
- [Brain Files](https://github.com/martingwhite/kramer) - The language model server script which reads/writes JSON documents to named pipes.

#### 2. Untar MITLM and Python Daemon:

Execute the following command to un-tar the the MITLM and python daemon packages:

`tar -xzf <package_name.tar.gz>`

#### 3. Add proper directories to your path:

Execute the Following commands or add them to your .bash_profile to set up your $PATH.
**Be sure to replace the paths with
local paths on your machine**

```
export PYTHONPATH=$PYTHONPATH:/Path/to/Python/Daemon/python-daemon-<replace_with_installed_version>/
export PYTHONPATH=$PYTHONPATH:/Path/to/Python/Daemon/python-daemon-<replace_with_installed_version>/daemon/
export PATH=$PATH:/Path/to/MITLM/mitlm-0.4.1/
export PATH=$PATH:/Path/to/Brain/Files/
```

#### 4. Build MITLM:

Navigate to the mitlm-0.4.1/ directory and execute the following commands:

```
./configure
make
```

#### Note: make may fail if you are using Big Sur OS on a mac.

The issue here is that the system is using the wrong version of gcc.
If it does, follow the following steps:

Execute the following command to downgrade your version of gcc:

```
brew install gcc@10
```

Make sure `/usr/local/bin` is before `/usr/bin` when you execute `echo $PATH`.
Execute these for g++, gcc and c++.

```
ln -sf /usr/local/bin/gcc-10 /usr/local/bin/gcc
ln -sf /usr/local/bin/g++-10 /usr/local/bin/g++
ln -sf /usr/local/bin/c++-10 /usr/local/bin/c++
```

`make` should now be able to be executed.

After both of these commands have been executed, you should be able to see the estimate-ngram, evaluate-ngram, and interpolate-ngram executables in the mitlm-0.4.1/ directory.

#### 5. Instantiate the Brain:

Navigate to helion/ directory. Instantiate the brain by running:

```
braind data/generated_data/training/training_model/helion.train data/generated_data/training/training_model/helion.vocab
```

#### Note: you may run into a `NameError: name 'FileNotFoundError' is not defined` error

There is an issue with the braind file that was downloaded through kramer-master.
Open the braind file with your code editor and find the line that causes this error (likely line 65).

Replace `FileNotFoundError` with `IOerror` so the line should now look like the following:

```
except (subprocess.CalledProcessError, IOError) as e:
```

Save the change and reinstantiate the brain with the same command as written above.

#### For windows users, if the brain runs into `CalledProcessorError()`, there is a chance that files to be used are formatted in CRLF rather than LF. Because we are utilizing WSL, it is necessary to ensure that these files's line endings are formatted in LF.

To do this, open helion.vocab and helion.train located in helion/data/generated_data/training/training_model/ folder with your IDE. At the bottom of your IDE, you should see the format of the file (LF or CRLF). Click on the text and an option to select the format will appear likely at the top of the screen. Select LF.

Reinstantiate the brain by running the above mentioned command.

### Acknowledgements:

- [Kramer](https://github.com/martingwhite/kramer)
- [MITLM](https://github.com/mitlm/mitlm)
- [python-daemon](https://pypi.org/project/python-daemon/)
