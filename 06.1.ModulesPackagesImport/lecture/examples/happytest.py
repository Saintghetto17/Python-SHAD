import happy

def test():
    assert happy.bar() == happy.foo

if __name__ == "__main__":
    print('Running test')
    test()
    print('OK')    
