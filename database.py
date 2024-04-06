import pandas as pd
import os
import warnings

datas = []
datas_name = []

def print_selection():
    print( "======Database practice======" )
    print( "0  : EXIT" )
    print( "1  : Load xlsx" )
    print( "=============================" )
    print( "2  : Select" )
    print( "3  : Project" )
    print( "4  : Rename" )
    print( "5  : Cartesian product" )
    print( "6  : Union" )
    print( "7  : Set difference" )
    print( "=============================" )
    print( "8  : Set intersection" )
    print( "9  : Division" )
    print( "=============================" )
    print( "10 : Delete table" )
    print( "11 : Print all database" )
    print( "12 : Print single database" )
    print( "13 : Save single file" )
    print( "14 : Help", end="\n\n" )

def check_selection( command ):
    if command >= 0 and command <= 14:
        return True
    else:
        return False

def print_help():
    print( "Welcom to Database testing system" )
    print( "(0:  EXIT): quit system." )
    print( "(1:  Load xlsx): import a xlsx file, when entering file name please do not include \".xslx\"." )
    print( "================================================================================================" )
    print( "(2:  Select): You can select by column or compare with value." )
    print( "(3:  Project): You can project the table by selecting the attributes." )
    print( "(4:  Rename): You can rename the table." )
    print( "(5:  Cartesian product): You can do Cartesian product between two tables." )
    print( "(6:  Union): You can do Union between two tables." )
    print( "(7:  Set difference): You can set difference between two tables." )
    print( "================================================================================================" )
    print( "(8:  Set intersection): You can set intersection between two tables." )
    print( "(9:  Division): You can division between two tables." )
    print( "================================================================================================" )
    print( "(10: Delete table): You can choose the table you want to delete." )
    print( "(11: Print all database): print out all the table you store in system." )
    print( "(12: Print single database): print out the table you select." )
    print( "(13: Save single file): save the table you select, the name of file was customize." )
    print( end="\n\n" )

def save_or_not():
    # 詢問要不要儲存並記錄save，如果要儲存save會是使用者希望儲存的名字，不儲存save是None
    save = input("Do you want to save the result ? ( Y (yes) / N (no) ) : ")
    if save != "Y" and save != "N" and save != "y" and save != "n":
        raise Exception("Invalid command")
            
    if save == "Y" or save == "y":
        save = input("Please enter the new table name : ")
    else:
        save = None  
    
    return save

def write_file( name, filename ):
    # 使用者提供輸出檔的名字，將table輸出成excel(.xlsx)檔
    index = datas_name.index(name)
    if os.path.exists(filename):
        os.remove(filename)
        
    datas[index].to_excel(filename + '.xlsx', index=False)
    print(f"File \"{filename}.xlsx\" saved successfully!", end="\n\n")

def print_result(result):
    # 印出result的結果，如果沒有內容會輸出empty database
    print( "=======================================" )
    print(result)
    print( "=======================================", end="\n\n" ) 

def search_table(table):
    index = datas_name.index(table)
    result = datas[index]
    return result

def insert_data(data, name):
    # 將結果寫入datas與datas_name，重名的話會替代
    if name in datas_name:
        index = datas_name.index(name)
        datas[index] = data
    else:
        datas.append(data)  # 將 data 作為一個元素添加到 datas
        datas_name.append(name)  # 將 name 作為一個元素添加到 datas_name      
    
def load_data(filename):
    # 讀檔
    try:
        data = pd.read_excel(filename + '.xlsx')
        return data
    except:
        raise Exception(f"File \"{filename}.xlsx\" is not exist or file format is not correct")

def select_data_value( name, compare, attribute, value, save ):
    # select實作，與值比較
    index = datas_name.index(name)
    table = datas[index]

    # 與值比較
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
        insert_data( result, save)
  
    return result

def select_data_column( name, compare, column1, column2, save ):
    # select實作，與列互相比較
    table = search_table( name )

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

def project_data( name, attributes, save ):
    # project實作
    table = search_table( name ) # 找出對應的attribute
    result = table[attributes].drop_duplicates() # 將重複的資料刪除
    if save != None:
        insert_data(result, save)

    return result

def rename_data( name, new_name ):
    # 對table進行重新命名，直接更改datas_name
    table = search_table( name )
    insert_data( table, new_name )

def cartesian_product( table1, table2, save ):
    table1 = search_table( table1 )
    table2 = search_table( table2 )
    
    original_column_names = table1.columns.tolist() + table2.columns.tolist()
    
    result = []
    for i in range(len(table1)):
        for j in range(len(table2)):
            # 巢狀迴圈，將 table1 和 table2 的每一行組合起來
            row1 = table1.iloc[i, :].tolist()
            row2 = table2.iloc[j, :].tolist()
            # 將組合的結果添加到 result 中
            result.append(row1 + row2)
    
    result = pd.DataFrame(result, columns=original_column_names)

    if save is not None:
        insert_data(result, save)

    return result

def union( table1, table2, save ):
    table1 = search_table( table1 )
    table2 = search_table( table2 )
    result = []
    
    # 將 table1 和 table2 的所有行添加到 result 中
    for i in range(len(table1)):
        result.append(table1.iloc[i])
    for i in range(len(table2)):
        result.append(table2.iloc[i])
    result = pd.DataFrame(result)

    result = result.drop_duplicates()
    
    if save != None:
        insert_data( result, save )
    
    return result

def set_difference( table1, table2, save ):
    table1 = search_table( table1 )
    table2 = search_table( table2 )
    
    # 取交集
    mask = table1.isin(table2).all(axis=1)
    
    # 對交集取差集
    result = table1[~mask]
    
    if save != None:
        insert_data( result, save )
    
    return result

def set_intersection( table1, table2, save ):
    table1 = search_table( table1 )
    table2 = search_table( table2 )
    list1 = [row.tolist() for index, row in table1.iterrows()]
    list2 = [row.tolist() for index, row in table2.iterrows()]

    result = [row for row in list1 if row in list2]
    result = pd.DataFrame(result)
    
    if save is not None:
        insert_data(result, save)

    return result

def division(name1, name2, save):
    table1 = search_table(name1)
    table2 = search_table(name2)
    
    # 獲取 table1 和 table2 的列名
    column1 = table1.columns.tolist()
    column2 = table2.columns.tolist()

    # 檢查 table2 的所有列是否都在 table1 中
    if not all(elem in column1 for elem in column2):
        raise Exception(f"The column of \"{name2}\" is not in \"{name1}\"")

    # 創建一個空的 DataFrame 來存儲結果
    result = pd.DataFrame()

    # 對於 table1 中的每一行，檢查是否所有 table2 的列的值都在該行中
    for i, row in table1.iterrows():
        if all(row[column] in table2[column].values for column in column2):
            result = pd.concat([result, pd.DataFrame(row).T])

    # 重設結果的索引
    result.reset_index(drop=True, inplace=True)

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
    
    data = load_data("test")
    insert_data( data, "test" )
    data = load_data("test1")
    insert_data( data, "test1" )
    data = load_data("test2")
    insert_data( data, "test2" )
    print( "Insert test and test1 and test2" )
    
    
    while ( True ):
        try:
            while True:
                print_selection()
                command = int(input("Enter a command : "))
                if check_selection( command ):
                    break
                raise Exception("Invalid command")
        
            if command == 0:
                print("\033[92mThank you for using the system. Goodbye!\033[0m")
                break
            
            elif command == 1:
                filename = input("Enter the filename(without .xlsx): ")
                data = load_data(filename)

                if data is not None:
                    insert_data( data, filename )
                    print_result( data )
                    print( f"File \"{filename}.xlsx\" loaded!", end="\n\n" )
                else:
                    pass
                
            elif command == 2:
                name = input("Which table do you want to search ? : ")
                if name not in datas_name:
                    raise Exception(f"Table \"{name}\" not exist")
                
                value = None
                compare = None
                attribute = None

                mode = int(input( "Do you want to campare with 1. column or 2. value : " ))
                if mode != 1 and mode != 2:
                    raise Exception("Invalid command")

                if mode == 1:
                    #conpare with column
                    print( "Please input a column name." )
                    # find the column name, if not exist, print error message
                    column1 = input("Which column do you choose ? : ")
                    if column1 not in datas[datas_name.index(name)].columns:
                        raise Exception(f"Column : \"{column1}\" not in the table")

                    # find the column name, if not exist, print error message
                    column2 = input( "Which column do you want to compare to ? : " )
                    if column2 not in datas[datas_name.index(name)].columns:
                        raise Exception(f"Column : \"{column2}\" not in the table")
                    
                    print("Do you want to compare the data as greater than or less than the value?")
                    compare = input("( > / < / >= / <= / = ) : ")
                    if compare != ">" and compare != "<" and compare != ">=" and compare != "<=" and compare != "=":
                        raise Exception("Invalid command")
                    
                    save = save_or_not()
                    result = select_data_column( name, compare, column1, column2, save )

                elif mode == 2:
                    #compare with value
                    attribute = input("Which attribute do you want to compare ? : ")
                    if attribute in datas[datas_name.index(name)].columns:
                        type_of_attribute = datas[datas_name.index(name)][attribute].dtype
                    else:
                        raise Exception(f"Attribute \"{attribute}\" not in the table")

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
                        raise Exception("Invalid command")
                    
                    if type_of_attribute == "int64":
                        value = int(value)
                    elif type_of_attribute == "float":
                        value = float(value)
                    elif type_of_attribute == "object":
                        value = str(value)

                    save = save_or_not()

                    result = select_data_value( name, compare, attribute, value, save )

                print_result(result)

            elif command == 3:
                finish = False
                attributes = []
                name = input("Which table do you want to project ? : ")
                if name not in datas_name:
                    raise Exception(f"Table \"{name}\" not exist")

                table = datas[datas_name.index(name)]
                title = table.columns.tolist()
                while not finish:
                    if len( attributes ) >= len( table.columns ):
                        print("All attributes have been selected. It will finished automatically.", end="\n\n")
                        break
                    
                    print( "Which attribute do you want to project ?" )
                    print( f"The attributes you can use : {title}" )
                    attribute = input( "( if you finish entering attribute, please use 0 to finish it ) : " )
                    if attribute == "0":
                        finish = True
                        break
                    if attribute in table.columns:
                        attributes.append(attribute)
                        title.remove(attribute)
                    else:
                        #special case can not use raise exception to avoid the loop break
                        print(f"Error: Attribute : \"{attribute}\" not in the table. Please try again.")
                        continue
                    
                save = save_or_not()

                result = project_data(name, attributes, save)
                print_result(result)

            elif command == 4:
                table = input("Which table do you want to rename ? : ")
                if table not in datas_name:
                    raise Exception(f"Table \"{table}\" not exist")

                new_name = input("Enter the new name for the table: ")
                rename_data(table, new_name)
                print( f"{new_name} was created !", end="\n\n" )

            elif command == 5:
                table1 = input("Which table do you want to use for the Cartesian product ? : ")
                if table1 not in datas_name:
                    raise Exception(f"Table \"{table1}\" not exist")
                
                table2 = input(f"Which table do you want to use for the Cartesian product ( with table \"{table1}\" ) ? : ")
                if table2 not in datas_name:
                    raise Exception(f"Table \"{table2}\" not exist")
                
                save = save_or_not()
                result = cartesian_product( table1, table2, save )
                print_result(result)

            elif command == 6:
                table1 = input("Which table do you want to use for the Union ? : ")
                if table1 not in datas_name:
                    raise Exception(f"Table \"{table1}\" not exist")
                
                table2 = input(f"Which table do you want to use for the Union ( with table \"{table1}\" ) ? : ")
                if table2 not in datas_name:
                    raise Exception(f"Table \"{table2}\" not exist")
                
                save = save_or_not()
                result = union( table1, table2, save )
                print_result(result)

            elif command == 7:
                table1 = input("Which table do you want to use for the set difference ? : ")
                if table1 not in datas_name:
                    raise Exception(f"Table \"{table1}\" not exist")
                
                table2 = input(f"Which table do you want to use for the set difference ( with table \"{table1}\" ) ? : ")
                if table2 not in datas_name:
                    raise Exception(f"Table \"{table2}\" not exist")
                
                save = save_or_not()
                result = set_difference( table1, table2, save )
                print_result(result)

            elif command == 8:
                table1 = input("Which table do you want to use for the set intersection ? : ")
                if table1 not in datas_name:
                    raise Exception(f"Table \"{table1}\" not exist")
                
                table2 = input(f"Which table do you want to use for the set intersection ( with table \"{table1}\" ) ? : ")
                if table2 not in datas_name:
                    raise Exception(f"Table \"{table2}\" not exist")
                
                save = save_or_not()
                result = set_intersection( table1, table2, save )
                print_result(result)

            elif command == 9:
                table1 = input("Which table do you want to use for the division ? : ")
                if table1 not in datas_name:
                    raise Exception(f"Table \"{table1}\" not exist")
                
                table2 = input(f"Which table do you want to use for the set division ( with table \"{table1}\" ) ? : ")
                if table2 not in datas_name:
                    raise Exception(f"Table \"{table2}\" not exist")
                
                save = save_or_not()
                result = division( table1, table2, save )
                print_result(result)

            elif command == 10:
                name = input("Which table do you want to delete ? : ")
                if name not in datas_name:
                    raise Exception(f"Table \"{name}\" not exist")

                delete_data(name)
                print("Table deleted!", end="\n\n")

            elif command == 11:
                print( "Print all database" )
                if ( datas == [] ):
                    raise Exception("No database")
                else:
                    for i in range(len(datas_name)):
                        print( "==================================" )
                        print( "Name: ", end=" " )
                        print(datas_name[i], end="\n\n")
                        print(datas[i])
                        print( "==================================", end="\n\n" )

            elif command == 12:
                name = input("Which table do you want to print ? : ")
                if name not in datas_name:
                    raise Exception(f"Table \"{name}\" not exist")

                print( "==================================" )
                print( "Name: ", end=" " )
                print(name, end="\n\n")
                print(datas[datas_name.index(name)])
                print( "==================================", end="\n\n" )

            elif command == 13:
                name = input("Which table do you want to save ? : ")
                if name not in datas_name:
                    raise Exception(f"Table \"{name}\" not exist")
                
                print( f"\033[91m\033[1mWarning. If the file was exist in your directory it will be cover by new data.\033[0m\033[0m" )
                filename = input("Enter the filename you want (without .xlsx): ")

                write_file(name, filename)

            elif command == 14:
                print_help()

            else:
                print("Invalid command")
            
        except Exception as ex:
            # exception handling, the error message will be printed
            # the message shouldn't include .
            print( f"\033[91mError: {ex}. Please try again.\033[0m", end="\n\n" )
            continue





