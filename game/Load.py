#!/usr/bin/env python3

class Load():

  word_path = 'data/words.txt'
  answer_path = 'data/answers.txt'

  words: list = []
  answers: list = []

  def __init__(self) -> None:
    if not len(self.words):
      self.words = self.fread(self.word_path)
      self.words.sort()
    
    if not len(self.answers):
      self.answers = self.fread(self.answer_path)
      self.answers.sort()
      
    return None
  
  def __enter__(self):
    return self

  def __exit__(self, ctx_type, ctx_msg, ctx_format):
    return None

  def fread(self, file, split: str = '\n') -> list:
    with open(file) as f:
        return f.read().split(split)
