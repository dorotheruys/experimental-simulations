%manual input J=1.6, AoA=7, varying V
function plot_PSD_var_V(mic_dat,opp_dat,delta)
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

figure('Name','Spectra')

for j = 1:length(inp_DPN)
    for i=1:6
        plot_number=i;
        if i == 4 || i == 5 
    
        else   
            if i == 6
                plot_number = 4;
            end
            
            run = find(opp_dat.opp{1}.DPN == inp_DPN_0(j));
            BPF=opp_dat.opp{1}.RPS_M1(run)*2*pi*6;
            %plot
            subplot(2,2,plot_number), box on, hold on;
            lab=['V = ',num2str(round(opp_dat.opp{1}.vInf(run),2))];
            plot(mic_dat.MIC{1}.f{run}/BPF,mic_dat.MIC{1}.PXX{run}(:,i),colors(j),'DisplayName',lab);
            %plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.PXX{run}(:,7),'DisplayName','Inflow mic');
            grid on
            legend
            xlim([0 13]);
            xlabel('Frequency f/RPS [-]');
            ylabel('PSD [-]');
            title(['Mic ',num2str(i)]);
            %ylim([0 120]);
            sgtitle(['Sound pressure level, J = ',num2str(round(opp_dat.opp{1}.J_M1(run),2)),', AoA = ',num2str(round(opp_dat.opp{1}.AoA(run),2)),'[deg]'])
        end
    end
end
end