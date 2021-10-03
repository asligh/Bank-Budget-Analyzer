from abc import ABCMeta
from decimal import Decimal, DivisionByZero
import os
import csv

class Program():

    ###################
    #                 # 
    #   PRIVATE VARS  #
    #                 # 
    ###################

    __MONTH_YEAR_IDX       = 0
    __AMT_IDX              = 1
    __RESOURCE_FOLDER_NAME = 'Resources'
    __FILE_NAME            = 'budget_data.csv'
    __total_months         = None
    __total_profit_loss    = None
    __average_change       = None     
    __monthly_perf_records = []
    __fin_data             = {}    
    __greatest_profit_increase    = {}
    __greatest_profit_decrease    = {}   

    ###################
    #                 # 
    #     GETTERS     #
    #                 # 
    ###################

    def get_resource_folder_name(self):
       return self.__RESOURCE_FOLDER_NAME    

    def get_file_name(self):
        return self.__FILE_NAME

    def get_resource_path(self):
        resource_folder_name = self.get_resource_folder_name()
        file_name = self.get_file_name()
        return os.path.join(resource_folder_name, file_name).replace("\\", "/")

    def get_total_months(self):
        return self.__total_months

    def get_fin_data(self):
        return self.__fin_data

    def get_total_profit_loss(self):
        return self.__total_profit_loss

    def get_month_year_idx(self):
        return self.__MONTH_YEAR_IDX

    def get_amt_idx(self):
        return self.__AMT_IDX  

    def get_greatest_profit_increase(self):
        return self.__greatest_profit_increase

    def get_greatest_profit_decrease(self):
        return self.__greatest_profit_decrease 
    
    def get_avg_change(self):
        return self.__average_change

    def get_monthly_perf_records(self):
        return self.__monthly_perf_records


    ###################
    #                 # 
    #     SETTERS     #
    #                 # 
    ###################

    def set_total_months(self,total_months):
        self.__total_months = total_months

    def set_total_profit_loss(self,total_profit_loss):
        self.__total_profit_loss = total_profit_loss

    def set_average_change(self,average_change):
        self.__average_change = average_change

    def set_greatest_prof_inc(self,greatest_profit_increase):
        self.__greatest_profit_increase = greatest_profit_increase

    def set_greatest_prof_inc(self,greatest_profit_decrease):
        self.__greatest_profit_decrease = greatest_profit_decrease 

    ###################
    #                 # 
    #   CONSTRUCTOR   #
    #                 # 
    ###################
    def __init__(self):
        None
  
    def read_data(self):
        
        fin_data          = self.get_fin_data()
        resource_path     = self.get_resource_path()
        total_months      = 0
        total_profit_loss = 0
        key               = None
        value             = None

        with open(resource_path) as csvfile:

            records = csv.reader(csvfile, delimiter=',')  ## CSV reader specifies delimiter and variable that holds contents

            monthly_perf_records = self.get_monthly_perf_records()

            greatest_inc = self.get_greatest_profit_increase()
            greatest_dec = self.get_greatest_profit_decrease()

            next(records) # move cursor past header row

            for record in records:
                key    = record[self.get_month_year_idx()]
                value  = Decimal(record[self.get_amt_idx()])

                fin_data.update({key:value})
                total_months +=1
                total_profit_loss += value

                if len(fin_data.keys()) > 1:

                    one_month_perf_change = value - Decimal(fin_data[ list(fin_data.keys())[-2]])   

                    if one_month_perf_change >= 0:

                        if len(greatest_inc.items()) == 0:
                            greatest_inc.update({key:value})
                        else:
                            previous_key = list(greatest_inc.keys())[0]

                            if Decimal(greatest_inc[previous_key]) < one_month_perf_change:
                                greatest_inc.clear()
                                greatest_inc.update({key:one_month_perf_change})

                    else:
                        if len(greatest_dec.items()) == 0:
                            greatest_dec.update({key:value})
                        else:
                            previous_key = list(greatest_dec.keys())[0]

                            if Decimal(greatest_dec[previous_key]) > one_month_perf_change:
                                greatest_dec.clear()
                                greatest_dec.update({key:one_month_perf_change})

                    monthly_perf_records.append(one_month_perf_change)

            self.set_total_months(total_months)
            self.set_total_profit_loss(total_profit_loss)
            self.set_average_change(sum(monthly_perf_records)/len(monthly_perf_records))

            print(f"greatest increase is {list(greatest_inc.keys())[0]} with a value of {greatest_inc[list(greatest_inc.keys())[0]]}")
            print(f"greatest decrease is {list(greatest_dec.keys())[0]} with a value of {greatest_dec[list(greatest_dec.keys())[0]]}")  

    def write_data(self):
        None

    def get_print_output(self):

        greatest_inc = self.get_greatest_profit_increase()
        greatest_dec = self.get_greatest_profit_decrease()

        print_str = "Financial Analysis \n" \
        + "---------------------------- \n" \
        + f"Total Months: {self.get_total_months()} \n" \
        + f"Total: ${self.get_total_profit_loss()} \n"  \
        + f"Average Change: ${round(self.get_avg_change(),2)} \n" \
        + f"Greatest Increase in Profits: {list(greatest_inc.keys())[0]} (${greatest_inc[list(greatest_inc.keys())[0]]}) \n" \
        + f"Greatest Decrease in Profits: {list(greatest_dec.keys())[0]} (${greatest_dec[list(greatest_dec.keys())[0]]})" 

        return print_str

    def write_data_to_terminal(self):
        print(self.get_print_output())

    def write_data_to_file(self):
        None

##End Class

def run_program():

    status = 0
    program = Program()
    
    try:
        program.read_data()
        program.write_data_to_terminal()
        program.write_data_to_file()

    except ZeroDivisionError as dbz:
        print(dbz.__str__)
        status = -1  
    
    except IOError as e:
        print(e.__str__)
        status = -1

    return status

result = run_program()