

function plot_p_PSD(mic_dat,opp_dat,run)
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
        

        %plot
        subplot(2,2,plot_number), box on, hold on;
        %plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.PXX{run}(:,i),'b','DisplayName','Mic');
        plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.SPL{run}(:,7), 'r','DisplayName','Inflow mic');
        grid on
        legend
        xlim([0 13]);
        xlabel('Frequency f/RPS [-]');
        ylabel('PSD [-]');
        title(['Mic ',num2str(i)]);
        %ylim([0 120]);
        sgtitle(['V = ',num2str(opp_dat.opp{1}.vInf(run)), ', J = ',num2str(opp_dat.opp{1}.J_M1(run))])
    end
end
end