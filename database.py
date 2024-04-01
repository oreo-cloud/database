import pandas as pd
import itertools

datas = []
datas_name = []

def print_selection():
    print( "====Database practice====" )
    print( "0  : EXIT" )
    print( "1  : Load xlsx" )
    print( "=========================" )
    print( "2  : Select" )
    print( "3  : Project" )
    print( "4  : Rename" )
    print( "5  : Cartesian product" )
    print( "6  : Union" )
    print( "7  : Difference" )
    print( "=========================" )
    print( "8  : Delete table" )
    print( "9  : Print all database" )
    print( "10 : Print single database" )
    print( "11 : Save single file" )
    print( "12 : Help", end="\n\n" )

def print_help():
    print( "Welcom to Database testing system" )
    print( "1. (1: load xlsx): import a xlsx file, when entering file name please do not enter \".xslx\"" )
    print( "1. (2: select): import a xlsx file at most 2 files, if import the third file it will delete the first one" )

def save_or_not():
    save = input("Do you want to save the result ? ( Y (yes) / N (no) ) : ")
    if save != "Y" and save != "N" and save != "y" and save != "n":
        print("Invalid command", end="\n\n")
            
    if save == "Y" or save == "y":
        save = input("Please enter the new table name : ")
    else:
        save = None  
    
    return save

def write_file( name ):
    index = datas_name.index(name)
    datas[index].to_excel(name + '.xlsx', index=False)
    print("File saved!", end="\n\n")
    
def insert_data( data, name ):
    if name in datas_name:
        index = datas_name.index(name)
        datas[index] = data
    else:
        datas.append(data)  # 將 data 作為一個元素添加到 datas
        datas_name.append(name)  # 將 name 作為一個元素添加到 datas_name      
    
def load_data(filename):
    try:
        data = pd.read_excel(filename + '.xlsx')
        return data
    except:
        print("Error: File not exist or file format is not correct. Please try again.", end="\n\n")
        return None

def select_data_value(name, compare, attribute, value, save):
    index = datas_name.index(name)
    table = datas[index]

    if compare == ">":
        result = table[table[attribute] > value]
    elif compare == ">=":
        result = table[table[attribute] >= value]
    elif compare == "<=":
        result = table[table[attribute] <= value]
    elif compare == "=":
        result = table[table[attribute] == value]
    else:
        result = table[table[attribute] < value]

    if save != None:
        insert_data( result, new_name)
  
    return result

def select_data_column( name, compare, column1, column2, save ):
    index = datas_name.index(name)
    table = datas[index]

    if compare == ">":
        result = table[table[column1] > table[column2]]
    elif compare == ">=":
        result = table[table[column1] >= table[column2]]
    elif compare == "<=":
        result = table[table[column1] <= table[column2]]
    elif compare == "=":
        result = table[table[column1] == table[column2]]
    else:
        result = table[table[column1] < table[column2]]

    if save != None:
        insert_data( result, save)
  
    return result

def project_data(name, attributes, save):
    index = datas_name.index(name)
    table = datas[index]
    result = table[attributes].drop_duplicates()
    if save != None:
        insert_data(result, save)

    return result

def rename_data(name, new_name):
    table = datas[datas_name.index(name)]
    insert_data( table, new_name )

def cartesian_product(table1, table2, save):
    index1 = datas_name.index(table1)
    index2 = datas_name.index(table2)
    table1 = datas[index1]
    table2 = datas[index2]
    
    original_column_names = table1.columns.tolist() + table2.columns.tolist()
    
    result = []
    for i in range(len(table1)):
        for j in range(len(table2)):
            row1 = table1.iloc[i, :].tolist()
            row2 = table2.iloc[j, :].tolist()
            result.append(row1 + row2)
    
    result = pd.DataFrame(result, columns=original_column_names)

    if save is not None:
        insert_data(result, save)

    return result

def delete_data(name):
    index = datas_name.index(name)
    datas.pop(index)
    datas_name.pop(index)

if __name__ == "__main__":
    #initialize variables
    datas = []
    datas_name = []
    
    while ( True ):
        try:
            while True:
                print_selection()
                command = int(input("Enter a command : "))
                break
        except:
            continue
        
        if command == 0:
            print("Thank you for using the system. Goodbye!")
            break
        
        elif command == 1:
            filename = input("Enter the filename(without .xlsx): ")
            data= load_data(filename)
            
            if data is not None:
                insert_data( data, filename )
                print( "file loaded!", end="\n\n" )
            else:
                pass
            
        elif command == 2:
            name = input("Which table do you want to search ? : ")
            if name not in datas_name:
                print("Error: table not exist. Please try again.", end="\n\n")
                continue
            
            value = None
            compare = None
            attribute = None
            
            mode = int(input( "Do you want to campare with 1. column or 2. value : " ))
            if mode != 1 and mode != 2:
                print( "Invalid command", end="\n\n" )
                continue
                
            if mode == 1:
                #conpare with column
                print( "Please input a column name." )
                # find the column name, if not exist, print error message
                column1 = input("Which column do you choose ? :")
                if column1 not in datas[datas_name.index(name)].columns:
                    print("Error: Column not in the table. Please try again.", end="\n\n")
                    continue
                # find the column name, if not exist, print error message
                column2 = input( "Which column do you want to compare to ? :" )
                if column2 not in datas[datas_name.index(name)].columns:
                    print("Error: Column not in the table. Please try again.", end="\n\n")
                    continue
                
                print("Do you want to compare the data as greater than or less than the value?")
                compare = input("( > / < / >= / <= / = ) : ")
                if compare != ">" and compare != "<" and compare != ">=" and compare != "<=" and compare != "=":
                    print("Invalid command", end="\n\n")
                    continue
                
                save = save_or_not()
                result = select_data_column( name, compare, column1, column2, save )
                
            elif mode == 2:
                #compare with value
                attribute = input("Which attribute do you want to compare ? : ")
                if attribute in datas[datas_name.index(name)].columns:
                    type_of_attribute = datas[datas_name.index(name)][attribute].dtype
                else:
                    print("Error: Attribute not in the table. Please try again.", end="\n\n")
                    continue
                print("Do you want to compare the data as greater than or less than the value?")
                compare = input("( > / < / >= / <= / = ) : ")
                if compare == ">":
                    value = input("Greater than ? : ")
                elif compare == "<":
                    value = input("Less than ? : ")
                elif compare == ">=":
                    value = input("Greater than or equal to ? : ")
                elif compare == "<=":
                    value = input("Less than or equal to ? : ")
                elif compare == "=":
                    value = input("Equal to ? : ")
                else:
                    print("Invalid command", end="\n\n")
                    continue
                
                if type_of_attribute == "int64":
                    value = int(value)
                elif type_of_attribute == "float":
                    value = float(value)
                elif type_of_attribute == "object":
                    value = str(value)
                
                save = save_or_not()
                
                result = select_data_value( name, compare, attribute, value, save )
                
            print( "=======================================" )
            print(result)
            print( "=======================================", end="\n\n" ) 

        elif command == 3:
            finish = False
            attributes = []
            name = input("Which table do you want to project ? : ")
            if name not in datas_name:
                print("Error: table not exist. Please try again.", end="\n\n")
                continue
            table = datas[datas_name.index(name)]
            while not finish:
                print( "Which attribute do you want to project ?" )
                attribute = input( "( if you finish entering attribute, please use 0 to finish it ) :" )
                if attribute == "0":
                    finish = True
                    break
                if attribute in table.columns:
                    attributes.append(attribute)
                else:
                    print("Error: Attribute not in the table. Please try again.", end="\n\n")
                    break
                
            save = save_or_not()
                
            result = project_data(name, attributes, save)
            print( "=======================================" )
            print(result)
            print( "=======================================", end="\n\n" ) 
            
        elif command == 4:
            table = input("Which table do you want to rename ? : ")
            if table not in datas_name:
                print("Error: table not exist. Please try again.", end="\n\n")
                continue
            new_name = input("Enter the new name for the table: ")
            rename_data(table, new_name)
            
        elif command == 5:
            table1 = input("Which table do you want to Cartision ? : ")
            if table1 not in datas_name:
                print("Error: table not exist. Please try again.", end="\n\n")
                continue
            
            table2 = input("Which table do you want to Cartision with ? : ")
            if table2 not in datas_name:
                print("Error: table not exist. Please try again.", end="\n\n")
                continue
            
            save = save_or_not()
            result = cartesian_product( table1, table2, save )
            print( "=======================================" )
            print(result)
            print( "=======================================", end="\n\n" ) 
        
        elif command == 6:
            print("Union...")
            
        elif command == 7:
            print("Difference...")
            
        elif command == 8:
            name = input("Which table do you want to delete ? : ")
            if name not in datas_name:
                print("Error: table not exist. Please try again.", end="\n\n")
                continue
            delete_data(name)
            print("Table deleted!", end="\n\n")
            
        elif command == 9:
            print( "Print all database" )
            if ( datas == [] ):
                print( "No database", end="\n\n" )
            else:
                for i in range(len(datas_name)):
                    print( "==================================" )
                    print( "Name: ", end=" " )
                    print(datas_name[i], end="\n\n")
                    print(datas[i])
                    print( "==================================", end="\n\n" )
            
        elif command == 10:
            name = input("Which table do you want to print ? : ")
            if name not in datas_name:
                print("Error: table not exist. Please try again.", end="\n\n")
                continue
            print( "==================================" )
            print( "Name: ", end=" " )
            print(name, end="\n\n")
            print(datas[datas_name.index(name)])
            print( "==================================", end="\n\n" )
            
        elif command == 11:
            name = input("Which table do you want to save ? : ")
            if name not in datas_name:
                print("Error: table not exist. Please try again.", end="\n\n")
                continue
            write_file(name)
            
        elif command == 12:
            print_help()
            
        else:
            print("Invalid command")
        
        
        
        
        
    