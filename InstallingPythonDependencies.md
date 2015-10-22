# Introduction #

There are several packages that the EMO20Q python code depends on:
  * NetworkX, a graph library
  * NLTK, a natural language processing toolkit, also used for probability distributions and naive Bayes.

This wikipage gives a brief guide about how to quickly install these libraries on linux

# NetworkX #

```
sudo easy_install networkX
```


# NLTK #

```
sudo easy_install pip
sudo pip install -U numpy # note 1
sudo pip install -U pyyaml nltk
```

note 1: this step failed at first for me b/c  I had to install the python development package through my linux distribution.  To fix it I installed python-devel:
```
sudo zypper in python-devel
```
The linux distribution you use may have a different command, e.g., rpm, yum, apt-get, emerge, etc., and the name might be slightly different, e.g., python-dev.  After fixing this, go back and try installing numpy again.  If this doesn't work, let us know.

Note: I realized that there is a movement from **easy\_install** to **pip**.  To be coherent, networkx could be installed through pip too, but I'm more used to easy\_install

# EMO20Q #

Now see if it works:
  * first change directory to the "python/" directory.
` cd python `
  * make sure that the emo20q subdirectory is on your PYTHONPATH environment variable:
` . setup.env `
  * try running the agent:
` ./emo20q/agents/gpdaquestioner.py --run `

If there are any problems, let us know.