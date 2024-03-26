

function plot_p_SPL(mic_dat,opp_dat,run)
figure('Name','Spectra')
%here all mics are plotted, i indicates which mic is plotted
% this plots sound pressure level
for i=1:6
    plot_number=i;
    if i == 4 || i == 5 

    else   
        if i == 6
            plot_number = 4;
        end
        %calcualte difference between mic and inflow mic
        diff=mic_dat.MIC{1}.SPL{run}(:,i)-mic_dat.MIC{1}.SPL{run}(:,7);

        %plot
        subplot(2,2,plot_number), box on, hold on;
        plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.SPL{run}(:,i),'b');
        plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.SPL{run}(:,7), 'r');
        plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),diff,'g');
        grid on
        legend('Mic','inflow mic','diff');
        xlim([0 13]);
        xlabel('Frequency f/RPS [-]');
        ylabel('SPL [dB]');
        title(['Mic ',num2str(i)]);
        %ylim([0 120]);
    end
end
end