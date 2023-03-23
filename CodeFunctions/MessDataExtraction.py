import numpy as np
import re

def messExtract(filePath, T, P, keywords, pUnit='atm'):   

    keywords = np.append(keywords, "Temperature-Pressure")

    file = open(filePath,'r')
    content = file.readlines()
    file.close()

    #-------------------------------------------------------------------------------------------------------------------------------#
    # Lines to find High Pressure Data

    HighP_start = re.compile(r"Temperature-Species Rate Tables")
    HighP_end = re.compile(r"Capture/Escape Rate Coefficients")
    line_num = 0

    while line_num < len(content):
        line = str.strip(content[line_num])
        if HighP_start.search(line):
            # print(line, line_num)
            HighP_start_num = line_num
        if HighP_end.search(line):
            # print(line, line_num)
            HighP_end_num = line_num
            break
        line_num = line_num + 1


    HighP_content = content[HighP_start_num : HighP_end_num]


    rates = []
    for key_num in range(0, len(keywords) - 1):

        keyword_start = keywords[key_num]

        keyword_end = keywords[key_num + 1]
        # print(keyword_end)

        line_num = 0
        # start_num = 0
        for line_num in range(0, len(HighP_content)):
            line = str.strip(HighP_content[line_num]).split()
            for keyword in line:
                if keyword == keyword_start + '->' + keywords[0]:
                    start_num  =  line_num + 1
                    break
            if keyword == keyword_start + '->' + keywords[0]:
                break

        rates.append(HighP_content[start_num: start_num + len(T)])
            
    for i in range(0, len(rates)):
        for j in range(0, len(rates[i])):
            rates[i][j] = str.strip(rates[i][j]).split()
            # for k in range(0, len(rates[i][j])):
                # rates[i][j][k] = str.strip(rates[i][j][k]).split()

        # print(rates[1])

    # print(rates[0:2])

    rates = np.array(rates)
    rates[rates=='***'] = ['nan']
    rates = rates.astype(float)
    # print(rates[0])   

    # print(rates.shape)

    hpRates = np.transpose(rates, (0,2,1))


    #----------------------------------------------------------------------------------------------------------------------------------------#


    # Lines to find Temperature-Species Rate Tables

    temp_press_start = re.compile(r"Temperature-Species Rate Tables")
    temp_press_end = re.compile(r"Temperature-Pressure Rate Tables")
    line_num = 0

    while line_num < len(content):
        line = str.strip(content[line_num])
        if temp_press_start.search(line):
            # print(line, line_num)
            temp_press_start_num = line_num
        if temp_press_end.search(line):
            # print(line, line_num)
            temp_press_end_num = line_num
            break
        line_num = line_num + 1


    # print(temp_press_start_num, temp_press_end_num)

    temp_press_content = content[temp_press_start_num : temp_press_end_num + 1]


    # print(temp_press_content[-1])

    rates =[]
    start_num = 0
    for key_num in range(0, len(keywords) - 1):

        keyword_start = keywords[key_num]

        keyword_end = keywords[key_num + 1]
        # print(keyword_end)

        line_num = 0

        for line_num in range(0, len(temp_press_content)):
            line = str.strip(temp_press_content[line_num]).split()
            for keyword in line:
                if keyword == keyword_start + '->':
                    start_num  =  line_num - 2
                    break
            if keyword == keyword_start + '->':
                break

        for line_num in range(0, len(temp_press_content)):
            line = str.strip(temp_press_content[line_num]).split()
            for keyword in line:
                if keyword == keyword_end + '->':
                    end_num  =  line_num - 3
                    break
                elif keyword == "Temperature-Pressure":
                    end_num = line_num - 3
                    break
            if keyword == keyword_end + '->':
                break
            elif keyword == "Temperature-Pressure":
                break

        # print(start_num)
        # print(end_num)        
        # print(temp_press_content[start_num])
        # print(temp_press_content[end_num - 1])

        data = temp_press_content[start_num: end_num]
        # print(data)

        i = 0

        for p in P:
            # print(p)
            for i in range(0, len(data)):
                if re.compile('Pressure = ' + str(p) + ' '+ pUnit).search(str.strip(data[i])):
                    line_num = i
                    rates.append(data[i + 3: i + 3 + len(T)])
                    # print(str.strip(data[i])) 
        # print(rates[0])

        # df = pd.DataFrame(rates[1])

    for i in range(0, len(rates)):
        for j in range(0, len(rates[i])):
                rates[i][j] = str.strip(rates[i][j]).split()
            # for k in range(0, len(rates[i][j])):
                # rates[i][j][k] = str.strip(rates[i][j][k]).split()

        # print(rates[1])

    # print(rates[0:2])

    rates = np.array(rates)
    rates[rates=='***'] = ['nan']
    rates = rates.astype(float)
    # print(rates[0])   

    # print(rates.shape)

    tpRates = np.transpose(rates, (0,2,1))
    # print(rates[55])
    # print(rates.shape)

    # rates_M1M_parent = rates

    # print(rates_M1M_parent.shape)
    # rates =[]
    return hpRates, tpRates