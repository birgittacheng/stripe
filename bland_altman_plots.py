"""Creates Bland-Altman plots plots for Algorithm for any view or view combination"""

import pickle
import matplotlib.pyplot as plt
import numpy as np

CARDIO_DICT_PATH = 'cardio_dict.pkl'
PREDICTED_DICT_PATH = 'predicted_dict.pkl'

VIEW_TO_TITLE = {'plax_ef':'PLAX only',
                'ap2_ef': 'AP2 only',
                'ap4_ef': 'AP4 only',
                ('ap2_ef','ap4_ef'): 'AP4 and AP2',
                ('ap4_ef', 'plax_ef'): 'AP4 and PLAX',
                ('ap2_ef', 'plax_ef'): 'AP2 and PLAX',
                ('ap2_ef', 'ap4_ef', 'plax_ef'): 'All views'}

def bland_altman_plot(mode):
    """Creates a Bland-Altman plot in the given mode. The mode can be any of the following: 
    
    ['plax_ef', 'ap2_ef', 'ap4_ef', ('ap2_ef','ap4_ef'), ('ap4_ef', 'plax_ef'), 
    ('ap2_ef', 'plax_ef'), ('ap2_ef', 'ap4_ef', 'plax_ef')]
    
    Code modified from stackoverflow user: 
    https://stackoverflow.com/questions/16399279/bland-altman-plot-in-python"""
    
    data1, data2 = create_lists_for_plotting(PREDICTED_DICT_PATH, CARDIO_DICT_PATH, mode)
    suptitle = VIEW_TO_TITLE[mode]

    data1     = np.asarray(data1)
    data2     = np.asarray(data2)
    mean      = np.mean([data1, data2], axis=0)
    diff      = data1 - data2                   # Difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference

    plt.scatter(mean, diff)
    plt.axhline(md,           color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
    
    lower = round(md - 1.96*sd, 2)
    upper = round(md + 1.96*sd, 2)
    
    print(min(mean))
    print(max(mean))
    print(max(diff))
    
    ax = plt.axes()
    ax.set(xlabel='Mean(Predicted EF(%),Reference EF(%))', ylabel='Predicted EF(%) - Reference EF(%)')
    
    plt.xlim(10, 80)
    plt.ylim(-40, 40)
    
    title = 'Bias = ' + str(round(md, 2)) + ', Limits of agreement = [' + str(lower) + ', ' + str(upper) + ']'
    
    plt.title(title)
    plt.suptitle(suptitle)
    plt.show()
    
    return

def create_ground_truth(cardio_dict_path):
    """Given a dictionary of cardiologist overreads, takes the average EF predicted for each study."""
    
    cardio_dict = pickle.load(open(cardio_dict_path, 'rb'))

    ground_truth_dict = {}

    for study in cardio_dict:
        total = 0.0
        
        for ef in cardio_dict[study].values():
            total += float(ef)
            
        mean = total/len(cardio_dict[study])
        ground_truth_dict[study] = mean

    return ground_truth_dict

def create_lists_for_plotting(auto_ef_dict_path, cardio_dict_path, view):
    """Creates two lists, one containing the algorithm predictions for the given view, 
    the other containing the ground truth for all studies, in the same order."""
    
    cardio_dict = create_ground_truth(cardio_dict_path)
    auto_ef_dict = pickle.load(open(auto_ef_dict_path, 'rb'))
    
    auto_ef_data = []
    cardio_data = []
    
    for study in auto_ef_dict:
        if view in auto_ef_dict[study]:
            auto_ef_data.append(auto_ef_dict[study][view])
            cardio_data.append(cardio_dict[study])
    
    return auto_ef_data, cardio_data

bland_altman_plot(('ap4_ef', 'plax_ef'))
