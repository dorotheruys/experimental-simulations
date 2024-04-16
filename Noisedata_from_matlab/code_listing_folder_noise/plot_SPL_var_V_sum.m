%manual input J=1.6, AoA=7, varying V
function plot_SPL_var_V_sum(mic_dat,opp_dat,delta)
%manual input J=1.6, AoA=7, varying V, different sets of elevator angle
inp_DPN_neg15=[27,17,4];
inp_DPN_0=[85,83,68];
inp_DPN_15=[54,48,36];
if delta == 0
    inp_DPN = inp_DPN_0;
 
elseif delta == -15
    inp_DPN = inp_DPN_neg15;

elseif delta == 15
    inp_DPN = inp_DPN_15;
end

colors=['r','g','b','m'];
colors2=["#7E2F8E","#77AC30","#000000"];
fig=figure('Name','Spectra');

for j = 1:length(inp_DPN)
    
            
    run = find(opp_dat.opp{1}.DPN == inp_DPN_0(j));

    subplot(1,2,1), box on, hold on;
    lab=['V = ',num2str(round(opp_dat.opp{1}.vInf(run),2))];
            %plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.SPL{run}(:,i),colors(j),'DisplayName',lab);
    sum_spl= 10*log10( (10.^(mic_dat.MIC{1}.SPL{run}(:,1)/10) + 10.^(mic_dat.MIC{1}.SPL{run}(:,2)/10) + 10.^(mic_dat.MIC{1}.SPL{run}(:,3)/10) )/3 )  ;
      
    plot(mic_dat.MIC{1}.f{run},sum_spl,colors(j),'DisplayName',lab);
    axis tight
    grid on
    legend
    xscale log
    xlabel('Frequency f [Hz]');
    ylabel('SPL [dB]');
    title(['Mic ',num2str(1)]);
    fontsize(fig, 22, "points")

    subplot(1,2,2), box on, hold on;
    plot(mic_dat.MIC{1}.f{run},mic_dat.MIC{1}.SPL{run}(:,7),colors(j),'DisplayName',lab);
    axis tight
    grid on
    legend
   
    xscale log
    
    % xlim([0 13]);
    % if i==7;
    %     ylim([40 70]);
    % else
    %     ylim([40 120]);
    % end
    xlabel('Frequency f [Hz]');
    ylabel('SPL [dB]');
    title(['Mic ',num2str(1)]);
    fontsize(fig, 22, "points")
    %ylim([0 120]);
    %sgtitle(['Sound pressure level, J = ',num2str(round(opp_dat.opp{1}.J_M1(run),2)),', AoA = ',num2str(round(opp_dat.opp{1}.AoA(run),2)),'[deg]'])
end
end


