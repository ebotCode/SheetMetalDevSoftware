class TabularTextDisplay:
    """
    This class formats a given set of data in tabular form
    """
    def __init__(self):
        pass 


    def formatAsTable(self,valuedict, firstcolumn = "N"):
        """
        Args:
            valuedict: a dictionary of numerical values. the keys are the column headers.
            firstcolumn : the key in valuedict that should appear as the first column when printing
        returns a list of strings. 
        each string in the list is a row in the table. 
        """
        columnheader = valuedict.keys()
        columnheader.sort()        
        # exctract the column headers
        if firstcolumn in valuedict:
            index = columnheader.index(firstcolumn)
            if index != 0:              
                columnheader[0],columnheader[index] = columnheader[index],columnheader[0]
                
        # Now, determine the width of each columns. (each column contains positive values.)
        #. first, get the maximum values in each column, and 
        ncolumn = len(columnheader)
        nrow = len(valuedict[columnheader[0]])
        all_max_value = [max(valuedict[item]) for item in columnheader]
        #. convert it to a string format with 4 decimal place. except for first column
        all_max_as_str = ['%.4f'%all_max_value[i] for i in range(ncolumn)]
        all_max_as_str[0] = '%d'%all_max_value[0] 
        column_widths = [len(item) for item in all_max_as_str]
        #. using the column width, prepare the formatstring for each column 
        header_format_str = "|".join(['{:^%d}'%(column_widths[i]+1) for i in range(ncolumn)])
        seperator_format_str = "|".join(['{:_^%d}'%(column_widths[i]+1) for i in range(ncolumn)])
        data_format_str_list   = ['{:%d}'%(column_widths[i]+1) for i in range(ncolumn)]
        data_format_str   = "|".join(data_format_str_list)
        #. prepare formatting string for integer and floats
        float_to_str_format = '{:.4f}'
        integer_to_str_format = '{}'#%(column_widths[0]+1)

        # print("all max = ",all_max_as_str)
        # print("all max as str = ",all_max_as_str)
        # print("see format list = ",data_format_str_list)
        #. Build the strings 
        data_rows = []
        final_row_string = ""
        for i in range(nrow):
            row = []
            for item in columnheader:
                if item == firstcolumn:
                    value_as_string = integer_to_str_format.format(valuedict[item][i])
                else:
                    value_as_string = float_to_str_format.format(valuedict[item][i])
                row.append(value_as_string)
            # print(" ".join(row))
            data_rows.append(data_format_str.format(*row))
        # make the header line seperator 
        row_sep = ["_" for i in range(ncolumn)]
        separator_row = seperator_format_str.format(*row_sep)
        # 
        header_row_names = header_format_str.format(*columnheader)#"Header"
        # print header_row_names
        header_rows = [header_row_names,separator_row]
        
        # data_row = ["Yes, Let's workd on this ","Yepee"]
        return (header_rows,data_rows)

    def formatHeader(self):
        pass 

    

