class LoadWords():
  def __init__(self) -> None:
    self.words = self.fread('resources/words.txt')
    self.answers = self.fread('resources/answers.txt')
    return None
  
  def __enter__(self):
    return self

  def __exit__(self, ctx_type, ctx_msg, ctx_format):
    return None

  def fread(self, file, split: str = '\n') -> list:
    with open(file) as f:
        return f.read().split(split)

  def words(self) -> list:
    return self.words

  def answers(self) -> list:    
    return self.answers