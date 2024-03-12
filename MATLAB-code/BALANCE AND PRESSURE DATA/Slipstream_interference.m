function [e_ss] = Slipstream_interference(T, V, D_p, rho, C)
%SLIPSTREAM_INTERFERENCE Summary of this function goes here
%   Detailed explanation goes here
S_p = pi / 4 * D_p^2;
T_c = T / (rho * V^2 * S_p);
e_ss = - T_c / (2* sqrt(1+2*T_c))*S_p / C;
end

