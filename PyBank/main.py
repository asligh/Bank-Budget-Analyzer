import os
import csv


#Author: Ashley Sligh

#Date: 10/08/2021

#Purpose: Processes financial records and provides base-line end-user statistics

#Dependencies: Financial records flat input file

#Stored Procedures: None

#Referenced Tables: None


class Program():

    ###################
    #                 # 
    #   PRIVATE VARS  #
    #                 # 
    ###################

    __MONTH_YEAR_IDX       = 0                      #Stores the month/year index
    __AMT_IDX              = 1                      #Stores the amount index
    __IN_FILE_NAME         = "budget_data.csv"      #Stores the input file name
    __OUT_FILE_NAME        = "budget_data_analysis" #Stores the output file name
    __OUT_FILE_EXTENSION   = ".txt"                 #Stores the output file extension
    __IN_FOLDER_NAME       = "Resources"            #Stores the input folder name
    __OUT_FOLDER_NAME      = "analysis"             #Stores the output folder name

    __total_months         = None                   #Store total months
    __total_profit_loss    = None                   #Stores total profit/loss
    __average_change       = None                   #Stores average change of profit/loss across all months
    __perf_records         = []                     #Stores the raw financial performance rescords
    __fin_data                  = {}                #Stores the raw financial records
    __greatest_profit_increase  = {}                #Stores greatest profit increase
    __greatest_profit_decrease  = {}                #Stores greastest profit decrease

    ###################
    #                 # 
    #     GETTERS     #
    #                 # 
    ###################

    #Returns the input file name
    def get_in_file_name(self):
        return self.__IN_FILE_NAME

    #Returns the output file name
    def get_out_file_name(self):
        return self.__OUT_FILE_NAME    
        
    #Returns the input folder name       
    def get_in_folder_name(self):
        return self.__IN_FOLDER_NAME  

    #Returns the output folder name
    def get_out_folder_name(self):
        return self.__OUT_FOLDER_NAME   

    #Returns the output file extension
    def get_out_file_extension(self):
        return self.__OUT_FILE_EXTENSION     

    #Returns input file path
    def get_in_file_path(self):
        in_folder_name = self.get_in_folder_name()
        in_file_name   = self.get_in_file_name()
        return os.path.join(in_folder_name, in_file_name).replace("\\", "/")

    #Returns output file path
    def get_out_file_path(self):
        out_folder_name    = self.get_out_folder_name()
        out_file_name      = self.get_out_file_name()
        out_file_extension = self.get_out_file_extension()
        return os.path.join(out_folder_name, out_file_name + out_file_extension).replace("\\", "/")      

    #Returns total number of months
    def get_total_months(self):
        return self.__total_months

    #Returns financial data
    def get_fin_data(self):
        return self.__fin_data

    #Returns total profit/loss
    def get_total_profit_loss(self):
        return self.__total_profit_loss

    #Returns the month/year index
    def get_month_year_idx(self):
        return self.__MONTH_YEAR_IDX

    #Returns the amount index
    def get_amt_idx(self):
        return self.__AMT_IDX  

    #Returns the greatest profit increase
    def get_greatest_profit_increase(self):
        return self.__greatest_profit_increase

    #Returns the greatest profit decrease
    def get_greatest_profit_decrease(self):
        return self.__greatest_profit_decrease
    
    #Returns the average change
    def get_avg_change(self):
        return self.__average_change

    #Returns performance records
    def get_perf_records(self):
        return self.__perf_records

    ###################
    #                 # 
    #     SETTERS     #
    #                 # 
    ###################

    #Stores total months
    def set_total_months(self,total_months):
        self.__total_months = total_months

    #Stores total profit/loss
    def set_total_profit_loss(self,total_profit_loss):
        self.__total_profit_loss = total_profit_loss

    #Stores average change
    def set_average_change(self,average_change):
        self.__average_change = average_change

    #Stores greatest profit increase
    def set_greatest_prof_inc(self,greatest_profit_increase):
        self.__greatest_profit_increase = greatest_profit_increase

    #Stores greatest profit decrease
    def set_greatest_prof_decrease(self,greatest_profit_decrease):
        self.__greatest_profit_decrease = greatest_profit_decrease 

    #Reads input file data
    def read_data(self):
        
        fin_data          = self.get_fin_data()
        in_file_path      = self.get_in_file_path()
        total_months      = 0
        total_profit_loss = 0
        key               = None
        value             = None

        with open(in_file_path, 'r') as in_file:

            records = csv.reader(in_file, delimiter=',')

            monthly_perf_records = self.get_perf_records()

            greatest_inc = self.get_greatest_profit_increase()
            greatest_dec = self.get_greatest_profit_decrease()

            header_row = next(records) # store header row for future use

            for record in records:
                key    = record[self.get_month_year_idx()]
                value  = float(record[self.get_amt_idx()])

                fin_data.update({key:value})
                total_months +=1
                total_profit_loss += value

                if len(fin_data.keys()) > 1:

                    one_month_perf_change = value - fin_data[ list(fin_data.keys())[-2]]  

                    if one_month_perf_change >= 0:

                        if len(greatest_inc.items()) == 0:
                            greatest_inc.update({key:value})
                        else:
                            previous_key = list(greatest_inc.keys())[0]

                            if greatest_inc[previous_key] < one_month_perf_change:
                                greatest_inc.clear()
                                greatest_inc.update({key:one_month_perf_change})

                    else:
                        if len(greatest_dec.items()) == 0:
                            greatest_dec.update({key:value})
                        else:
                            previous_key = list(greatest_dec.keys())[0]

                            if greatest_dec[previous_key] > one_month_perf_change:
                                greatest_dec.clear()
                                greatest_dec.update({key:one_month_perf_change})

                    monthly_perf_records.append(one_month_perf_change)

            self.set_total_months(total_months)
            self.set_total_profit_loss(total_profit_loss)
            self.set_average_change(sum(monthly_perf_records)/len(monthly_perf_records))

    #Returns financial data analysis
    def get_data_analysis(self) -> str:

        greatest_inc = self.get_greatest_profit_increase()
        greatest_dec = self.get_greatest_profit_decrease()

        print_str = "Financial Analysis \n" \
        + "---------------------------- \n" \
        + f"Total Months: {self.get_total_months()} \n" \
        + f"Total: ${int(self.get_total_profit_loss())} \n"  \
        + f"Average Change: ${round(self.get_avg_change(),2)} \n" \
        + f"Greatest Increase in Profits: {list(greatest_inc.keys())[0]} (${int(greatest_inc[list(greatest_inc.keys())[0]])}) \n" \
        + f"Greatest Decrease in Profits: {list(greatest_dec.keys())[0]} (${int(greatest_dec[list(greatest_dec.keys())[0]])})" 

        return print_str

    #Prints financial analysis to terminal window for end-user purposes
    def write_data_to_terminal(self):
        print(self.get_data_analysis())

    #Writes financial data to file for end-user purposes
    def write_data_to_file(self):
        out_file_path  = self.get_out_file_path()

        with open(out_file_path, "w") as out_file:
            out_file.write(self.get_data_analysis())
#End Class

#Main program repsonsible for running application
def run_program():

    status = 0
    program = Program()
    
    try:
        program.read_data()
        program.write_data_to_terminal()
        program.write_data_to_file()

    except IOError as e:
        print(e.__str__())
        status = -1

    return status

result = run_program()