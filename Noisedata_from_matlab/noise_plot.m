%call plotting functions for plots

%file input
MIC_file_neg15 = 'MIC_neg15_2.mat';
opp_file_neg15 = 'opp_neg15_2.mat';

MIC_file_0 = 'MIC_0.mat';
opp_file_0 = 'opp_0.mat';

MIC_file_15 = 'MIC_plus15.mat';
opp_file_15 = 'opp_plus15.mat';

%load data
MIC_neg15 = load(MIC_file_neg15);
opp_neg15 = load(opp_file_neg15);

MIC_0 = load(MIC_file_0);
opp_0 = load(opp_file_0);

MIC_15 = load(MIC_file_15);
opp_15 = load(opp_file_15);


%define run number here, ie which run to plot
run_number = 17;

%plot
% plot_p_PSD(MIC_0,opp_0,run_number)
% plot_SPL_var_J(MIC_0,opp_0,0)
% plot_PSD_var_J(MIC_0,opp_0,0)
plot_SPL_var_V(MIC_0,opp_0,0)
plot_PSD_var_V(MIC_0,opp_0,0)
% plot_p_SPL(MIC_0,opp_0,run_number)
% plot_p_PSD(MIC_0,opp_0,run_number)
% plot_p_SPL(MIC_0,opp_0,[24])
% plot_p_SPL(MIC_0,opp_0,[1])
% plot_p_PSD(MIC_0,opp_0,[24])
% plot_p_PSD(MIC_0,opp_0,[1])
%plot_p_amp(MIC_0,run_number)