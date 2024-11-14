def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    

fibonacci(10)

if __name__ == "__main__":

    print("called")
    # print(fibonacci(10))

