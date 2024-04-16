function plot_SPL_var_a_sum(mic_dat,opp_dat,delta,V)
%manual input v=40, j=1.6, different sets of elevator angle
inp_DPN_neg15=[4,8,13,24];
inp_DPN_0=[67,68,69,70];
inp_DPN_15=[36,42,46,55];
if delta == 0
    if V== 40
        inp_DPN = [67,68,69,70];
    elseif V==20
        %inp_DPN = [83,95];
        inp_DPN = [95];
    elseif V==10
        %inp_DPN = [85,96];
        inp_DPN = [96];
    end

elseif delta == -15
    if V== 40
        inp_DPN = [4,8,13,24];
    elseif V==20
        inp_DPN = [17,28];
    elseif V==10
        inp_DPN = [21,34];
    end

elseif delta == 15
    if V== 40
        inp_DPN = [36,42,46,55];
    elseif V==20
        inp_DPN = [48,62];
    elseif V==10
        inp_DPN = [54,65];
    end
end
colors=['r','b','g','m'];

fig=figure('Name','Spectra');

for j = 1:length(inp_DPN)

        run = find(opp_dat.opp{1}.DPN == inp_DPN(j));
        sum_spl=10*log10( (10.^(mic_dat.MIC{1}.SPL{run}(:,1)/10) + 10.^(mic_dat.MIC{1}.SPL{run}(:,2)/10) + 10.^(mic_dat.MIC{1}.SPL{run}(:,3)/10) )/3 )  ;
        %plot
        subplot(1,2,1), box on, hold on;
      
        lab=['AoA = ',num2str(round(opp_dat.opp{1}.AoA(run),2))];
    
        %plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.SPL{run}(:,i),colors(j),'DisplayName',lab);
        plot(mic_dat.MIC{1}.f{run},sum_spl,colors(j),'DisplayName',lab);
        xlabel('Frequency f [Hz]');
        axis tight
        ylabel('SPL [dB]');
        grid on
        legend
        xscale log

        subplot(1,2,2), box on, hold on;
        plot(mic_dat.MIC{1}.f{run},mic_dat.MIC{1}.SPL{run}(:,7),colors(j),'DisplayName',lab);
        axis tight
        grid on
        legend
        %xlim([0 14]);
        xscale log
        if i==7
            %ylim([40 70]);
        else
            %ylim([65 115]);
        end
        xlabel('Frequency f [Hz]');
        %xlabel('Frequency f/RPS [-]');
        ylabel('SPL [dB]');
        title(['Mic ',num2str(1)]);
        fontsize(fig, 22, "points")
        %ylim([0 120]);
        %sgtitle(['Sound pressure level, V = ',num2str(round(opp_dat.opp{1}.vInf(run),2)),'m/s, AoA = ',num2str(round(opp_dat.opp{1}.AoA(run),2)),'[deg]'])
    end
end
