
def foo():
    print(message)

if __name__ == "__main__":
    print('Running test...')
    message = 'I just leaked to global namespace'
    foo()
