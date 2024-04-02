MIC_file_0 = 'MIC_0.mat';
opp_file_0 = 'opp_0.mat';

MIC_0 = load(MIC_file_0);
opp_0 = load(opp_file_0);

p_cor=MIC_0.MIC{1}.pMic{1} (1,:)-MIC_0.MIC{1}.pMic{1} (7,:);
pfft=fft(p_cor);
y= fft(p_cor);

plot(MIC_0.MIC{1}.f{1} (1,:),y)