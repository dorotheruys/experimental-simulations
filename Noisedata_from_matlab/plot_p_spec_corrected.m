function plot_p_spec_corrected(mic_dat,opp_dat,run)
figure('Name','Spectra')
lab = [];
%here all mics are plotted, i indicates which mic is plotted
% this plots sound pressure level
for j = 1:numel(run)

    for i=1:6
        plot_number=i;
        if i == 4 || i == 5 
    
        else   
            if i == 6
                plot_number = 4;
            end
            %calculate frequency of equivalent atr72 aircraft
            %define some constants
            %model  and fullscale (FS) propeller diameter
            D_mod = 0.2032;
            D_FS = 3.93;
    
            %model  and fullscale (FS) flight speed
            U_mod = opp_dat.opp{1}.vInf(run(j));
            U_FS = 116;
            
            %compute difference between mic and inflow mic to isolate prop
            %noise (model)
            diff_mod = mic_dat.MIC{1}.SPL{run(j)}(:,i)-mic_dat.MIC{1}.SPL{run(j)}(:,7);
    
            %shifted frequency of imaginary fullscale aircraft
            f_FS = mic_dat.MIC{1}.f{run(j)}/opp_dat.opp{1}.RPS_M1(run(j)) * (D_mod*U_FS)/(D_FS*U_mod);
   
            %plot
            
            subplot(2,2,plot_number), box on, hold on;
            plot(mic_dat.MIC{1}.f{run(j)}/opp_dat.opp{1}.RPS_M1(run(j)),diff_mod);
            plot(f_FS,diff_mod);
            grid on
            legend('minus inflow','shifted');
            %xlim([0 13]);
            xlabel('Frequency f/RPS [-]');
            ylabel('SPL [dB]');
            title(['Tunnel velocity =',num2str(round(U_mod,2)),'  J_{model}=',num2str(round(opp_dat.opp{1}.J_M1(run(j)),2))]);
            %ylim([40 120]);

         %end if statement
        end
     %end i for loop
    end
   
%end j for loop
end

%end function
end