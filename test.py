import argparse
from pypen.preprocess import gen_letters
from pypen.convert import convert_txt_to_hdwn, convert_doc_to_hdwn

txt = open("input.txt", "r").read().strip()
# process text to remove punctuation, emojis etc.
proc_txt = ""
for letter in txt :
    if letter.isalpha() or letter in [' ','\n'] :
        proc_txt += letter
print(proc_txt)
gen_letters(source="letters", width=200, height=300)
convert_txt_to_hdwn(input=proc_txt, letters='proc_letters', lttr_size=30)