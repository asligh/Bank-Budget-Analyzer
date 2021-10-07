import os
import csv

#Instance-based solution
class Program():

    ###################
    #                 # 
    #   PRIVATE VARS  #
    #                 # 
    ###################

    __MONTH_YEAR_IDX       = 0
    __AMT_IDX              = 1
    __IN_FILE_NAME         = "budget_data.csv"
    __OUT_FILE_NAME        = "budget_data_analysis"
    __OUT_FILE_EXTENSION   = ".txt"   
    __IN_FOLDER_NAME       = "Resources"
    __OUT_FOLDER_NAME      = "analysis"   

    __total_months         = None
    __total_profit_loss    = None
    __average_change       = None     
    __perf_records         = []
    __data                 = {}    
    __greatest_profit_increase    = {}
    __greatest_profit_decrease    = {}   

    ###################
    #                 # 
    #     GETTERS     #
    #                 # 
    ###################

    def get_in_file_name(self):
        return self.__IN_FILE_NAME

    def get_out_file_name(self):
        return self.__OUT_FILE_NAME    
        
    def get_in_folder_name(self):
        return self.__IN_FOLDER_NAME  

    def get_out_folder_name(self):
        return self.__OUT_FOLDER_NAME   

    def get_out_file_extension(self):
        return self.__OUT_FILE_EXTENSION     

    def get_in_file_path(self):
        in_folder_name = self.get_in_folder_name()
        in_file_name   = self.get_in_file_name()
        return os.path.join(in_folder_name, in_file_name).replace("\\", "/")

    def get_out_file_path(self):
        out_folder_name    = self.get_out_folder_name()
        out_file_name      = self.get_out_file_name()
        out_file_extension = self.get_out_file_extension()
        return os.path.join(out_folder_name, out_file_name + out_file_extension).replace("\\", "/")      

    def get_total_months(self):
        return self.__total_months

    def get_data(self):
        return self.__data

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

    def get_perf_records(self):
        return self.__perf_records

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

    def read_data(self):
        
        data              = self.get_data()
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

            next(records) # move cursor past header row

            for record in records:
                key    = record[self.get_month_year_idx()]
                value  = float(record[self.get_amt_idx()])

                data.update({key:value})
                total_months +=1
                total_profit_loss += value

                if len(data.keys()) > 1:

                    one_month_perf_change = value - data[ list(data.keys())[-2]]  

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

    def get_data_analysis(self):

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

    def write_data_to_terminal(self):
        print(self.get_data_analysis())

    def write_data_to_file(self):
        out_file_path  = self.get_out_file_path()

        with open(out_file_path, "w") as out_file:
            out_file.write(self.get_data_analysis())

##End Class

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