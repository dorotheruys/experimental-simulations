%input 3 datasets, tunnel velocity

function plot_PSD_var_J(mic_dat,opp_dat,delta)
%manual input v=40, AoA=7, varying J, different sets of elevator angle
inp_DPN_neg15=[4,8,13,24];
inp_DPN_0=[68,71,75,90];
inp_DPN_15=[36,42,46,55];
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
            BPF=opp_dat.opp{1}.RPS_M1(run)*2*pi;
            %plot
            subplot(2,2,plot_number), box on, hold on;
            lab=['J = ',num2str(round(opp_dat.opp{1}.J_M1(run),2))];

            %plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.PXX{run}(:,i),colors(j),'DisplayName',lab);
            plot(mic_dat.MIC{1}.f{run}/BPF,mic_dat.MIC{1}.PXX{run}(:,i),colors(j),'DisplayName',lab);
            %plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.PXX{run}(:,7),'DisplayName','Inflow mic');
            grid on
            legend
            xlim([0 13]);
            xlabel('Frequency f/BPF [-]');
            ylabel('PSD [-]');
            title(['Mic ',num2str(i)]);
            %ylim([0 120]);
            sgtitle(['Power spectral density, V = ',num2str(round(opp_dat.opp{1}.vInf(run),2)),'m/s, AoA = ',num2str(round(opp_dat.opp{1}.AoA(run),2)),'[deg]'])
        end
    end
end
end