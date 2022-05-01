#!/usr/bin/env python3

class LoadWords():
  words: list = []
  answers: list = []

  def __init__(self) -> None:
    if not len(self.words):
      self.words = self.fread('resources/words.txt')
      self.words.sort()
    
    if not len(self.answers):
      self.answers = self.fread('resources/answers.txt')
      self.answers.sort()
      
    return None
  
  def __enter__(self):
    return self

  def __exit__(self, ctx_type, ctx_msg, ctx_format):
    return None

  def fread(self, file, split: str = '\n') -> list:
    with open(file) as f:
        return f.read().split(split)
