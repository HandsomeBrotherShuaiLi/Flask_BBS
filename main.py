import argparse
from emotion import demo
from model import train_model, valid_model


def run_demo():
  modelpath="S:/pycharm/emotion_analysis/models"
  demo(modelpath, showBox=True)

# def run_model():
#   if args.train_or_valid == 'train':
#     train_model()
#   elif args.train_or_valid == 'valid':
#     valid_model()

def main():
  f=input("please input you choose/n")
  if f == "demo":
    run_demo()
  elif f == "model":
    a1=input("train?valid?")
    if a1=="train":
      train_model()
    else:
      valid_model()

  else :
    print("usage: python3 main.py <function>")

if __name__ == '__main__':
  main()