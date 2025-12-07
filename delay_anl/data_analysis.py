import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from scipy.stats import lognorm
from scipy.stats import gamma
from scipy.stats import weibull_min

# data paths
PINGPONG_PATH = 'data/ping-pong/'
ONETOONE_PATH = 'data/one-to-one/'
ONETOMANY_PATH = 'data/one-to-many/'
PAYLOAD_PATH = 'data/payload/'
DISTURBANCE_PATH = 'data/disturbance/'

DATA_PATHS = [PINGPONG_PATH, ONETOONE_PATH, ONETOMANY_PATH, PAYLOAD_PATH, DISTURBANCE_PATH]
SCENARIOS = ['Reference Scenario', 'Scalability Test', 'Payload Test', 'Disturbance Test']

# sizes for labels (in KB)
SIZES = [0.25, 1, 4, 16, 64]

# MATLAB color palette for consistency with plots
COLORS = [
    '#0072BD',
    '#D95319',
    '#EDB120',
    '#7E2F8E',
    '#77AC30',
    '#4DBEEE',
    '#A2142F'
]

sns.set_palette(COLORS)

def importData (data_path):
    data = []
    if 'ping-pong' in data_path:
        data.append(pd.read_csv(data_path + 'sender_to_receiver.csv')*1e-6)
        data.append(pd.read_csv(data_path + 'receiver_to_sender.csv')*1e-6)
        data.append(pd.read_csv(data_path + 'round_trip.csv')*1e-6)
        
    elif 'one-to-one' in data_path:
        data.append(pd.read_csv(data_path + 'sender_to_receiver.csv')*1e-6)
        data.append(pd.read_csv(data_path + 'receiver_to_sender.csv')*1e-6)
        
    elif 'one-to-many' in data_path:
        n = 6
        for i in range(1, n):
            data.append(pd.read_csv(data_path + '1to' + str(n) + '/sender_to_receiver_' + str(i) + '.csv')*1e-6)
        for i in range(2,11):
            if i % 5 == 0:
                data.append(pd.read_csv(data_path + '1to' + str(i) + '/receivers_to_sender.csv')*1e-6)
        
    elif 'payload' in data_path:
        data.append(pd.read_csv(data_path + '50-joints/sender_to_receiver.csv')*1e-6)
        data.append(pd.read_csv(data_path + '50-joints/receiver_to_sender.csv')*1e-6)

        w = 40
        h = 35
        for i in range(3):
            data.append(pd.read_csv(data_path + str(w) + 'x' + str(h) + '/sender_to_receiver.csv')*1e-6)
            data.append(pd.read_csv(data_path + str(w) + 'x' + str(h) + '/receiver_to_sender.csv')*1e-6)
            w *= 2
            h *= 2
        
    elif 'disturbance' in data_path:
        data.append(pd.read_csv(data_path + 'sender_to_receiver.csv')*1e-6)
        data.append(pd.read_csv(data_path + 'receiver_to_sender.csv')*1e-6)
        
    return data

def pingpong_analysis(data):
    # figure initilization
    time_series, axs = plt.subplots(2, 1, figsize = (16, 9))
    
    # delay values extraction
    s2r_delay = data[0]['delay'].values
    r2s_delay = data[1]['delay'].values
    rtt_delay = data[2]['delay'].values
    
    # computing the time instants
    s2r_time = (data[0]['timestamp'] - data[0]['timestamp'].iloc[0]).values*1e-3
    r2s_time = (data[1]['timestamp'] - data[1]['timestamp'].iloc[0]).values*1e-3
    rtt_time = (data[2]['timestamp'] - data[2]['timestamp'].iloc[0]).values*1e-3
    
    # RTT
    axs[0].plot(rtt_time, rtt_delay, color = COLORS[0], linewidth = 3, label = r'$d_{RTT}$')
    axs[0].plot(rtt_time, s2r_delay + r2s_delay, color = COLORS[1], linewidth = 3, label = r'$d_{OWD,AB} + d_{OWD,BA}$')
    axs[0].set_xlabel('t [s]', fontsize = 24)
    axs[0].set_xlim(59.5, 60.5)
    axs[0].set_ylabel('delay [ms]', fontsize = 24)
    axs[0].set_ylim(0, 8)
    axs[0].set_title('Validation of the Clocks Sinchronyzation ', fontsize = 28)
    axs[0].legend(fontsize = 20)
    axs[0].tick_params(axis='both', labelsize=24)
    axs[0].grid(True)
    
    # OWD
    axs[1].plot(s2r_time, s2r_delay, color = COLORS[0], linewidth = 3, label = r'$d_{OWD,AB}$')
    axs[1].plot(r2s_time, r2s_delay, color = COLORS[1], linewidth = 3, label = r'$d_{OWD,BA}$')
    axs[1].set_xlabel('t [s]', fontsize = 24)
    axs[1].set_xlim(59.5, 60.5)
    axs[1].set_ylabel('delay [ms]', fontsize = 24)
    axs[1].set_ylim(0, 8)
    axs[1].set_title('Validation of the Channel Asymmetry', fontsize = 28)
    axs[1].legend(fontsize = 20)
    axs[1].tick_params(axis='both', labelsize=24)
    axs[1].grid(True)
    
    # global adjustments
    plt.suptitle('Preliminary Test: Timeseries', fontsize = 32)
    plt.tight_layout()
    
    return time_series

def histograms_plot(data, data_path, scenario):
    # figure initialization
    histogram, axs = plt.subplots(2, 1, figsize = (16, 9))

    # data extraction
    delay = []
    for d in data:
        delay.append(d['delay'].values)
    
    # histograms
    if not 'one-to-one' in data_path:
        l1 = ' (Reference)'
        l2 = ' (Reference)'
        if 'one-to-many' in data_path:  
            l1 = 'B' + l1
            l2 = '1:1' + l2
        elif 'payload' in data_path:
            l1 = '0.25 KB' + l1
            l2 = '0.25 KB' + l2
        elif 'disturbance' in data_path:
            l1 = 'Clear Network' + l1
            l2 = 'Clear Network' + l2

        sns.histplot(pd.read_csv(DATA_PATHS[1] + 'sender_to_receiver.csv')['delay'].values*1e-6, bins = 250, stat = 'count', label = l1, ax = axs[0])
        sns.histplot(pd.read_csv(DATA_PATHS[1] + 'receiver_to_sender.csv')['delay'].values*1e-6, bins = 250, stat = 'count', label = l2, ax = axs[1])
    
    # sender to receiver
    if 'one-to-many' in data_path:
        for i in range(0, len(delay) - 2): 
            sns.histplot(delay[i], bins = 250, stat = 'count', label = rf'$B_{i + 1}$', ax = axs[0])
    elif 'payload' in data_path:
        for i in range(len(delay)):
            sns.histplot(delay[i], bins = 250, stat = 'count', label = str(SIZES[(int)(i/2 + 1)]) + ' KB', ax = axs[i%2])
    elif 'disturbance' in data_path:
        sns.histplot(delay[0], bins = 250, stat = 'count', label = 'Network with Disturbance', ax = axs[0])
    else:
        sns.histplot(delay[0], bins = 250, stat = 'count', ax = axs[0])
    
    axs[0].set_xlabel(r'$d_{OWD,AB}$ [ms]', fontsize = 24)
    if 'payload' in data_path:
        axs[0].set_xlim(0.01, 16)
    else:
        axs[0].set_xlim(0.01, 4)
    axs[0].set_ylabel('# samples', fontsize = 24)
    axs[0].set_ylim(0, 6e3)
    axs[0].set_title(r'AB Path', fontsize = 28)
    axs[0].tick_params(axis='both', labelsize=24)
    if not 'one-to-one' in data_path:
        axs[0].legend(fontsize = 20)
    axs[0].grid(True)

    # receiver to sender
    if 'one-to-many' in data_path:
        j = 5
        for i in range(len(delay) - 2, len(delay)):
            sns.histplot(delay[i], bins = 250, stat = 'count', label = f'1:{j}', ax = axs[1])
            j += 5
    elif 'disturbance' in data_path:
        sns.histplot(delay[-1], bins = 250, stat = 'count', label = 'Network with Disturbance', ax = axs[1])
    elif not 'payload' in data_path:
        sns.histplot(delay[1], bins = 250, stat = 'count', ax = axs[1])
    
    axs[1].set_xlabel(r'$d_{OWD,BA}$ [ms]', fontsize = 24)
    if 'one-to-many' in data_path:
        axs[1].set_xlim(0.01, 8)
    elif 'payload' in data_path:
        axs[1].set_xlim(0.01, 16)
    else:
        axs[1].set_xlim(0.01, 4)
        
    axs[1].set_ylabel('# samples', fontsize = 24)
    if 'one-to-many' in data_path:
        axs[1].set_ylim(0, 12e3)
    else:
        axs[1].set_ylim(0, 6e3)

    axs[1].set_title(r'BA Path', fontsize = 28)
    axs[1].tick_params(axis='both', labelsize=24)
    if not 'one-to-one' in data_path:
        axs[1].legend(fontsize = 20)
    axs[1].grid(True)

    # final adjustments and return instruction
    plt.suptitle(scenario + ': Latency Samples Histograms', fontsize = 32)
    plt.tight_layout()
    
    return histogram

def pdf_analysis(data):
    # figure initialization
    fitting, axs = plt.subplots(2, 1, figsize = (16, 9))

    # delay values extraction
    delay, x = [], []
    for d in data:
        delay.append(d['delay'].values)
    
    # RV vector
    x = []
    for d in delay:
        x.append(np.linspace(0, d.max(), 500))
    
    # MLE fitting
    lognormal_pdf, gamma_pdf, weibull_pdf = [], [], []
    for i in range(len(delay)):
        mean, std = np.mean(delay[i]), np.std(delay[i])
        if i == 0:
            print('\n========== AB ==========')
        elif i == 1:
            print('========== BA ==========')
        print(f'mu         =  {mean:.2f}  [ms]')
        print(f'sigma      =  {std:.2f}  [ms]')
        
        s, loc, scale = lognorm.fit(delay[i])
        lognormal_pdf.append(lognorm.pdf(x[i], s = s, loc = loc, scale = scale))
        print(f'theta      =  {loc:.2f}  [ms]')
        print(f'mu_log     = {np.log(scale):.2f}')
        print(f'sigma_log  =  {s:.2f}')
        print('========================\n')
        a, loc, scale = gamma.fit(delay[i])
        gamma_pdf.append(gamma.pdf(x[i], a = a, loc = loc, scale = scale))
        
        c, loc, scale = weibull_min.fit(delay[i])
        weibull_pdf.append(weibull_min.pdf(x[i], c = c, loc = loc, scale = scale))
    
    # plotting the fitted PDFs
    # sender to receiver
    sns.histplot(delay[0], bins = 250, stat = 'density', label = 'Empirical', ax = axs[0])
    axs[0].plot(x[0], lognormal_pdf[0], color = COLORS[1], linestyle = '--', linewidth = 3, label = 'Lognormal')
    axs[0].plot(x[0], gamma_pdf[0], color = COLORS[2], linestyle = '--', linewidth = 3, label = 'Gamma')
    axs[0].plot(x[0], weibull_pdf[0], color = COLORS[3], linestyle = '--', linewidth = 3, label = 'Weibull')
    axs[0].set_xlabel(r'$d_{OWD,AB}$ [ms]', fontsize = 24)
    axs[0].set_xlim(0.01, 4)
    axs[0].set_ylabel('density', fontsize = 24)
    axs[0].set_ylim(0, 10)
    axs[0].set_title('AB Path', fontsize = 28)
    axs[0].legend(fontsize = 20)
    axs[0].tick_params(axis='both', labelsize=24)
    axs[0].grid(True)

    # receiver to Sender
    sns.histplot(delay[1], bins = 250, stat = 'density', label = 'Empirical', ax = axs[1])
    axs[1].plot(x[1], lognormal_pdf[1], color = COLORS[1], linestyle = '--', linewidth = 3, label = 'Lognormal')
    axs[1].plot(x[1], gamma_pdf[1], color = COLORS[2], linestyle = '--', linewidth = 3, label = 'Gamma')
    axs[1].plot(x[1], weibull_pdf[1], color = COLORS[3], linestyle = '--', linewidth = 3, label = 'Weibull')
    axs[1].set_xlabel(r'$d_{OWD,BA}$ [ms]', fontsize = 24)
    axs[1].set_xlim(0.01, 4) 
    axs[1].set_ylabel('density', fontsize = 24)
    axs[1].set_ylim(0, 10)
    axs[1].set_title('BA Path', fontsize = 28)
    axs[1].legend(fontsize = 20)
    axs[1].tick_params(axis='both', labelsize=24)
    axs[1].grid(True)

    # global adjustments
    plt.suptitle('Selected PDFs Fitting', fontsize = 32)
    plt.tight_layout()
    
    # Lognormals overlay
    overlay = plt.figure(figsize=(16,9)) 
    plt.plot(x[0], lognormal_pdf[0], color = COLORS[0], linewidth = 3, label = 'AB')
    plt.plot(x[1], lognormal_pdf[1], color = COLORS[1], linewidth = 3, label = 'BA')
    plt.xlabel(r'$d_{OWD}$ [ms]', fontsize = 24)
    plt.xlim(0.01, 4)
    plt.ylabel('density', fontsize = 24)
    plt.ylim(0, 4)
    plt.legend(fontsize = 20)
    plt.tick_params(axis='both', labelsize=24)
    plt.grid(True)
    
    plt.suptitle('Overlay of the Latency Distributions in the two Directions', fontsize = 32)
    plt.tight_layout()
    
    return fitting, overlay

def payload_analysis(data):
    delay = []
    for d in data:
        delay.append(d['delay'].values)
    
    # computing mean and std
    mean, std = [], []
    for d in delay:
        mean.append(np.mean(d))
        std.append(np.std(d))

    # extracting data for each direction
    mean_ab, mean_ba, std_ab, std_ba = [], [], [], []
    for i in range(len(mean)):
        if i % 2 == 0:
            mean_ab.append(mean[i])
            std_ab.append(std[i])
        else:
            mean_ba.append(mean[i])
            std_ba.append(std[i])
            
    mean_std_vs_payload, axs = plt.subplots(2, 1, figsize = (16, 9))

    # mean vs payload size
    axs[0].plot(SIZES, mean_ab, color = COLORS[0], linewidth = 3, marker = 's', markersize = 9, label = 'AB')
    axs[0].plot(SIZES, mean_ba, color = COLORS[1], linewidth = 3, marker = '^', markersize = 9, label = 'BA')
    axs[0].set_xscale('log')          
    axs[0].set_xlabel('payload [KB]', fontsize = 24)
    axs[0].set_ylabel(r'$\mu$ [ms]', fontsize = 24)
    axs[0].set_ylim(0, 15)
    axs[0].set_title('Mean vs. Payload Size', fontsize = 28)
    axs[0].tick_params(axis='both', labelsize=24)
    axs[0].legend(fontsize = 20)
    axs[0].grid(True)

    # std vs payload size
    axs[1].plot(SIZES, std_ab, color = COLORS[0], linewidth = 3, marker = 's', markersize = 9, label = 'AB')
    axs[1].plot(SIZES, std_ba, color = COLORS[1], linewidth = 3, marker = '^', markersize = 9, label = 'BA')
    axs[1].set_xscale('log', base = 10)
    axs[1].set_xlabel('payload [KB]', fontsize = 24)
    axs[1].set_ylabel(r'$\sigma$ [ms]', fontsize = 24)
    axs[1].set_ylim(0, 1)
    axs[1].set_title('Standard Deviation vs. Payload Size', fontsize = 28)
    axs[1].tick_params(axis='both', labelsize=24)
    axs[1].legend(fontsize = 20)
    axs[1].grid(True)

    # global adjustments
    plt.suptitle('Impact of Payload Size on Latency Mean and Standard Deviation', fontsize = 32)
    plt.tight_layout()
    
    return mean_std_vs_payload

def main():
    # ping-pong analysis
    data = importData(DATA_PATHS[0])
    pingpong_analysis(data)
    
    # histograms
    for i in range(1, len(DATA_PATHS)):
        data = importData(DATA_PATHS[i])
        histograms_plot(data, DATA_PATHS[i], SCENARIOS[i - 1])
        
    # PDF analysis
    data = importData(DATA_PATHS[1])
    pdf_analysis(data)
    
    # payload
    data = importData(DATA_PATHS[1]) + importData(DATA_PATHS[3])
    payload_analysis(data)
    
    plt.show()

main()
