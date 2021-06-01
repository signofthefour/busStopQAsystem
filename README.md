# Bus Stop Q&A system

An classical implemented question answering for bus stop/station

---

## Installation

***Ensure that your pip version is greater than 3, if not, try pip3 instead of pip in the following script***

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

## Reference

I used the concept of parser design with **my own significant changes** of the parser from [this open-source repo](https://github.com/cursecatcher/py-malt-parser) for my parser with **new workflow** to adapt with no-training-step and more complexity of the required grammar of this project.
