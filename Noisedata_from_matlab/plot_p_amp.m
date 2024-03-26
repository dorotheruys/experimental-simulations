

function plot_p_amp(mic_dat,run)
figure('Name','pressure')
%here all mics are plotted, i indicates which mic is plotted
% this plots sound pressure level

%define some stuff for plotting
%sampling frequency
fs       = 12800; 

%make time array for plotting, (6,:) assumes data from all mic have same
%length
t = 0 : 1/fs : (length(mic_dat.MIC{1}.pMic{run}(6,:))-1)/fs;

for i=1:6
    plot_number=i;
    if i == 4 || i == 5 

    else   
        if i == 6
            plot_number = 4;
        end
        subplot(2,2,plot_number), box on, hold on;
        plot(t,mic_dat.MIC{1}.pMic{run}(i,:),'b');
        
        plot(t,mic_dat.MIC{1}.pMic{run}(7,:), 'r');
        grid on
        legend('Mic','inflow mic');
        ylabel('Pressure amplitude');
        xlabel('Time (s)');
        title(['Mic ',num2str(i)]);
    end
end
end