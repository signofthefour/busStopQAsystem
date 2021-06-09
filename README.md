# Bus Stop Q&A system

An classical implemented question answering for bus stop/station

---

## Installation

***Ensure that your pip version is 3, if not, try pip3 instead of pip in the following script***

```bash
pip install -r requirements.txt
```

## Contributions

### POS step

I normalize some special words which can appear in the command and use the package [pyvi](https://pypi.org/project/pyvi/) for POS process. Then create a Sentence object to hold the tokens with more informations to deal with creating dependency relations.

### Build a grammar analysis of the dependency grammar

I used the concept of parser design with **my own significant changes** of the parser from [this open-source repo](https://github.com/cursecatcher/py-malt-parser) for my parser with **new workflow** to adapt with no-training-step and more complex grammar of this project.

1. Use the generated Sentence object to create a new parser

2. Implement Parser base on the proposed in [Nirve et al., 2008](https://www.researchgate.net/publication/220355552_Algorithms_for_Deterministic_Incremental_Dependency_Parsing)

3. Create parser with bellow GRAMMAR:

```python
S -> WH-QUERY BUS-NP | WHTIME-QUERY BUS-NP

WH-QUERY -> BUS-N + QDET

BUS-NP -> BUS-CNP BUS-ROUTE | BUS-ROUTE | BUS-ROUTE BUS-TIME

BUS-CNP -> BUS-N BUS-NAME

BUS-ROUTE -> DEPART-V CITY-CNP | DEPART-V CITY-CNP ARRIVE-V CITY-CNP

CITY-CNP -> CITY-N CITY-NAME | CITY-NAME

BUS-TIME -> PTIME + TIME_MOD

### Terminate
WHTIME-QUERY -> 'thoi_gian'
BUS-N -> 'Xe_buyt'
QDET -> 'nao'
ARRIVE-V -> 'den' | 'toi'
DEPART-V -> 'tu'
CITY-N -> 'thanh_pho'
CITY-NAME -> 'Ho_Chi_Minh' | 'Hue' | 'Da_Nang'
PTIME -> 'luc'
TIME_MODE -> [0-23]['00'|'30'] 'giờ'
BUS-NAME -> 'B'[1-6]
```

***The result is immitiate the result of grammar parser with semantic of nltk package.***

4. After create a parser which utilize the dependency tree from the malt parser. I added semantic features into each Grammar parsing. My idea is to create 3 main feature:

    - BUS
    - ROUTE
    - TIME

These features can contribute further action in our context. With [these design](./Models/grammar.py), I can scale up for more questions. And because of this progress, I can easyly get logical form as you can see in result.

5. I create a Query class to handle the action of query: standardize (for create query to work with database), create API for work with database, manage and return answer.

6. Answer the question as in result.

## Reference and dependency

- [py-malt-patser](https://github.com/cursecatcher/py-malt-parser): for my parser with **new workflow** to adapt with no-training-step and more complexity of the required grammar of this project.

- [Nirve et al., 2008](https://www.researchgate.net/publication/220355552_Algorithms_for_Deterministic_Incremental_Dependency_Parsing)

- [pyvi](https://pypi.org/project/pyvi/)

- [Semantics](http://www.nltk.org/howto/semantics.html)
