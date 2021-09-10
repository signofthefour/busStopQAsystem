# Bus Stop Q&A system

An implemented of question answering for bus stop/station with classical technique

---

## Installation

***Ensure that your pip version is 3, if not, try pip3 instead of pip in the following script***

```bash
pip install -r requirements.txt
```

Import your question in [here](./Input/question) where each question is store in a txt file and then:

```bash
python main.py --input_dir ./Input/question --output_dir ./Output
```

***In my local machine, the python cmd calls python version 3, you should use python verion 3 in your work/test***

## Folder structure

```txt
busStopQAsystem
 ┣ Input
 ┃ ┗ question
 ┃ ┃ ┣ question1.txt
 ┃ ┃ ┣ question2.txt
 ┃ ┃ ┣ question3.txt
 ┃ ┃ ┗ question4.txt
 ┣ Models
 ┃ ┣ __init__.py
 ┃ ┣ database.py
 ┃ ┣ enums.py
 ┃ ┣ grammar.py
 ┃ ┣ parser.py
 ┃ ┣ query.py
 ┃ ┣ sentence.py
 ┃ ┗ utils.py
 ┣ Output
 ┃ ┣ question1
 ┃ ┃ ┣ output_b.ans
 ┃ ┃ ┣ output_c.ans
 ┃ ┃ ┣ output_d.ans
 ┃ ┃ ┣ output_e.ans
 ┃ ┃ ┗ output_f.ans
 ┃ ┣ question2
 ┃ ┃ ┣ output_b.ans
 ┃ ┃ ┣ output_c.ans
 ┃ ┃ ┣ output_d.ans
 ┃ ┃ ┣ output_e.ans
 ┃ ┃ ┗ output_f.ans
 ┃ ┣ question3
 ┃ ┃ ┣ output_b.ans
 ┃ ┃ ┣ output_c.ans
 ┃ ┃ ┣ output_d.ans
 ┃ ┃ ┣ output_e.ans
 ┃ ┃ ┗ output_f.ans
 ┃ ┗ question4
 ┃ ┃ ┣ output_b.ans
 ┃ ┃ ┣ output_c.ans
 ┃ ┃ ┣ output_d.ans
 ┃ ┃ ┣ output_e.ans
 ┃ ┃ ┗ output_f.ans
 ┣ LICENSE
 ┣ README.md
 ┣ main.py
 ┗ requirements.txt
```

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

## Answers for question 1

1. Dependency relationship

```txt
1	        Xe_buýt		N              	3	nsubj
2	            nào		P              	1	det
3	            đến		E              	None	root
4	      thành_phố		N              	3	dobj
5	            Huế		Np             	4	compound
6	            lúc		N              	3	nmod
7	          20.00		M              	6	nummod
8	            giờ		Nu             	7	nmod
9	              ?		F              	3	punct
```

2. Grammar parsing tree

```txt
S[GAP<b1> SEM<(WHICHBUS(b1)) & (\s ROUTE(s, DST-CITY(NAME(HUE, c2)), b1, \dt.TIME(dt, 20.00))) & (\dt.TIME(dt, 20.00))>,VAR<b1>]
	(WHICH-QUERY[SEM<WHICHBUS(b1)>,VAR<b1>]
		(BUS-N[SEM<NAME(None, None)>,VAR<b1>])
		(QDET[SEM<NÀO>,VAR<?b>]))
	(BUS-NP[SEM<\s ROUTE(s, DST-CITY(NAME(HUE, c2)), b1, \dt.TIME(dt, 20.00)) & \dt.TIME(dt, 20.00)>,VAR<r>]
		(BUS-ROUTE[SEM<\s ROUTE(s, DST-CITY(NAME(HUE, c2)), b1, \dt.TIME(dt, 20.00))>,VAR<r>]
			(đến
			(BUS-DEST[SEM<\s b t.ROUTE(s, DST-CITY(NAME(HUE, c2)), b, t)>,VAR<r2>]
				(CITY-CNP[SEM<NAME(HUE, c2)>,VAR<c2>]
					(CITY-N[SEM<THANHPHO>,VAR<c3>])
					(CITY-NAME[SEM<HUE>,VAR<c2>]))))
		(BUS-TIME[SEM<\dt.TIME(dt, 20.00)>,VAR<t1>]
			(P-TIME[SEM<lúc>])
			(TIME-MOD[SEM<20.00>]))))
```

3. Logical form

```txt
WHICH-QUERY(WHICHBUS(b1) & ROUTE(s1, DST-CITY(HUE, c2), b1, TIME(dt1, 20.00)) & TIME(dt1, 20.00))
```

4. Semantic procedure form

```txt
PRINT-ALL ?b1(BUS ?b1) ATIME(?b1 HUE 20.00) DTIME(?b1 ?s ?dt)
```

5. Answer

```
Kết quả tra cứu tuyến xe yêu cầu:
	- Tuyến xe B3 đi từ Đà Nẵng vào lúc 16:00 giờ đến Huế vào lúc 20:00 giờ.
```

### All question are store in [Output](./Output)

1. [Question 1](./Output/question1)
2. [Question 2](./Output/question2)
3. [Question 3](./Output/question3)
4. [Question 4](./Output/question4)

## Reference and dependency

- [py-malt-patser](https://github.com/cursecatcher/py-malt-parser): for my parser with **new workflow** to adapt with no-training-step and more complexity of the required grammar of this project.

- [Nirve et al., 2008](https://www.researchgate.net/publication/220355552_Algorithms_for_Deterministic_Incremental_Dependency_Parsing)

- [pyvi](https://pypi.org/project/pyvi/)

- [Semantics](http://www.nltk.org/howto/semantics.html)

## Contributions

[Nguyen Tan Dat](fb.com/sotfdat)
