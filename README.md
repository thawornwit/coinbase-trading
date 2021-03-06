#Description

A simple Python3 script that executes a basic rebalancing strategy for automated trading of bitcoins on Coinbase.

#Usage

* Set **API_KEY** and **API_SECRET** as environment variables, for instance in ~/.zshenv if you use zsh or in 
~/.bashrc if you use bash.

* To run the script type 

```
$ ./strategies.py

```

* For obvious reasons the program asks you in the beginning whether you want to execute real trades or
if you just want to carry out simulations. If you want it to execute real trades enter 'y'. Be warned 
that the author is not responsible for any financial losses incurred as a consequence.

* So far the only rebalancing strategy implemented is the 
[Constant Proportion Portfolio Insurance (CPPI)](http://en.wikipedia.org/wiki/Constant_proportion_portfolio_insurance)

* The program writes every rebalance event to a log file (by default tradelogs), one can view it in real time
by typing

```
$ tail -f tradelogs

```
