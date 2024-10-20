# Overview
Learn to read simplified Chinese through random quizzes of characters corresponding to chosen HSK levels. This project depends on [drkameleon's complete-hsk-vocabulary data set](https://github.com/drkameleon/complete-hsk-vocabulary).

# Installation
```bash
git clone git@github.com:fistaco/hvs.git
cd hvs
git clone https://github.com/drkameleon/complete-hsk-vocabulary
pip install --user -r requirements.txt
```

# Usage
To start learning, simply run the following:
```bash
python hvs.py
```

You will then be prompted with a pinyin word or character accompanied by the corresponding character(s) in simplified Chinese. The tool will tell you you're correct or not based on whether the similarity between your translation and any of the definitions exceeds a hard-coded threshold. Regardless of whether you answer is deemed correct, the tool outputs all correct definitions. Depending on the definition, this similarity threshold can be in your favour or against it. Example:
```bash
$ python hvs.py
tiān  (天)
day
Correct
All translations:  ['day', 'sky', 'heaven']

shí  (十)
ten
Correct
All translations:  ['ten', '10']

tā  (他)
he
False (similarity score = 22)
All translations:  ['he; him (used for either sex when the sex is unknown or unimportant)', "(used before sb's name for emphasis)", '(used as a meaningless mock object)', '(literary) other']
```
