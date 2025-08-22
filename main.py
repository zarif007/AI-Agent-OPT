import sys
from agent.agent import answer

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"your question here\"")
        sys.exit(1)
    q = " ".join(sys.argv[1:])
    out = answer(q)
    print(out)

if __name__ == "__main__":
    main()
