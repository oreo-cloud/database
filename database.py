import pandas as pd

def load_data(filename):
    data = pd.read_excel(filename)
    return data

if __name__ == "__main__":
    data = load_data("data.xlsx")
    print(data)
    