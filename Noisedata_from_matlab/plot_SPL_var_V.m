
%manual input J=1.6, AoA=7, varying V
function plot_SPL_var_V(mic_dat,opp_dat,delta)
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
figure('Name','Spectra')

for j = 1:length(inp_DPN)
    for i=1:7
        plot_number=i;
        if i == 4 || i == 5 || i==6 
    
        else   
            if i == 7
                plot_number = 4;
            end
            
            run = find(opp_dat.opp{1}.DPN == inp_DPN_0(j));
            BPF=opp_dat.opp{1}.RPS_M1(run)*6;
            %calculate frequency of equivalent atr72 aircraft
            %define some constants
            %model  and fullscale (FS) propeller diameter
            D_mod = 0.2032;
            D_FS = 3.93;
    
            %model  and fullscale (FS) flight speed
            U_mod = opp_dat.opp{1}.vInf(run);
            U_FS = 70;
            f_FS = mic_dat.MIC{1}.f{run}* (D_mod*U_FS)/(D_FS*U_mod);
            %plot
            subplot(2,2,plot_number), box on, hold on;
            lab=['V = ',num2str(round(opp_dat.opp{1}.vInf(run),2))];
            plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.SPL{run}(:,i),colors(j),'DisplayName',lab);
            %plot(f_FS,mic_dat.MIC{1}.SPL{run}(:,i),'DisplayName','full scale');
            %plot(mic_dat.MIC{1}.f{run}/opp_dat.opp{1}.RPS_M1(run),mic_dat.MIC{1}.PXX{run}(:,7),'DisplayName','Inflow mic');
            grid on
            legend
            xlim([0 13]);
            if i==7;
                ylim([40 70]);
            else
                ylim([40 120]);
            end
            xlabel('Frequency f/RPS [-]');
            ylabel('SPL [dB]');
            title(['Mic ',num2str(i)]);
            %ylim([0 120]);
            sgtitle(['Sound pressure level, J = ',num2str(round(opp_dat.opp{1}.J_M1(run),2)),', AoA = ',num2str(round(opp_dat.opp{1}.AoA(run),2)),'[deg]'])
        end
    end
end
end